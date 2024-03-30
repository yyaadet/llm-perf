import datetime
import os
from selenium import webdriver
from selenium.webdriver import Chrome, Firefox
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

import sys
import pandas as pd
import json
from tqdm import tqdm
import traceback
import time
from http.cookies import SimpleCookie
import logging
import settings
from test_prompt import TestPrompt


logger = logging.getLogger(__name__)


class BaseLLMTest(object):

    def __init__(self, headless: bool, raw_cookie: str, token: str) -> None:
        self.headless = headless
        self.raw_cookie = raw_cookie
        self.token = token 
        self.driver = None
        self.last_spend_seconds = None
        #self.driver = self.intial_chrome_driver()
        #self.driver = self.initial_firefox_driver()
        self.test_prompts: list[TestPrompt] = []

    def intial_chrome_driver(self) -> Chrome:
        options = ChromeOptions()
        if self.headless:
            options.add_argument("--headless=new")
        #self.chrome_options.add_argument(f"--window-size={1280},{720}")
        options.add_argument("--ignore-certificate-errors")  # 忽略证书错误
        options.add_argument("--disable-web-security")
        options.add_argument("--dns-prefetch-disable")
        if self.token:
            options.add_argument(f"--header='Authorization: Bearer {self.token}'")
        options.add_argument("--disable-gpu")
        prefs = {'profile.default_content_setting_values': {'notifications': 2}}
        prefs['profile.default_content_setting_values']['images'] = 2
        options.add_experimental_option('prefs', prefs)
        options.binary_location = str(settings.CHROME)
        options.add_argument(f'user-data-dir={settings.CHROME_USER_DATA}')

        # 添加实验性选项，用于排除指定的开关选项
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        
        service = ChromeService(settings.CHROME_DRIVER, log_output="chrome.log")
        driver = webdriver.Chrome(options, service)
        
        driver.implicitly_wait(60)
        driver.set_page_load_timeout(120)
        return driver
    
    def initial_firefox_driver(self) -> Firefox:
        options = FirefoxOptions()
        options.binary_location = str(settings.FIREFOX)
        service = FirefoxService(str(settings.FIREFOX_DRIVER))
        driver = Firefox(options, service)
        return driver

    def load_test_prompts(self):
        with open(settings.CEVAL_TEST_PROMPT) as f:
            for line in f:
                item = json.loads(line)
                p = TestPrompt(
                    prompt=item['prompt'], 
                    answer=item['answer'], 
                    full_answer=item['full_answer'],
                    category=item['category'], 
                    subject=item['subject']
                )
                self.test_prompts.append(p)

        return self.test_prompts
    
    def test_with_requests(self) -> bool:
        self.load_test_prompts()
        self._load_report()
        
        for i, item  in enumerate(tqdm(self.test_prompts)):
            if item.chat_answer:
                continue
            start = time.time()
            answer = self._get_answer(item.prompt)
            stop = time.time()
            if not answer:
                break

            item.chat_answer = answer
            if self.last_spend_seconds is not None:
                item.chat_spend_seconds = self.last_spend_seconds
            else:
                item.chat_spend_seconds = stop - start
            if i % 10 == 0 and i > 0:
                self.update_metrics()
                self.save_report()

        self.update_metrics()
        self.save_report()           

    def _get_answer(self, query) -> str:
        raise NotImplementedError()
    
    def test_with_selenium(self):
        raise NotImplementedError()
    
    def add_cookie(self, raw:str, domain:str):
        logger.info(f"current cookies {self.driver.get_cookies()}")
        simple_cookie = SimpleCookie()
        simple_cookie.load(raw)
        for k, v in simple_cookie.items():
            cookie = self.driver.get_cookie(k)
            if not cookie:
                cookie = {
                    'name': k,
                    'value': v,
                    'httpOnly': False,
                    'path': '/',
                    'sameSite': 'Lax',
                    'secure': False,
                    'domain': domain,
                }
            cookie['value'] = v.value
            self.driver.delete_cookie(k)
            self.driver.add_cookie(cookie)
            logger.info(f"set cookie: {k} = {v.value}, {cookie}")

        self.driver.implicitly_wait(30)
        self.check_cookie(raw)

    def check_cookie(self, raw:str):
        simple_cookie = SimpleCookie()
        simple_cookie.load(raw)
        for k, v in simple_cookie.items():
            current_cookie = self.driver.get_cookie(k)
            logger.info(f"name = {k}, current {current_cookie['value']}, expected {v.value}, is same {current_cookie['value'] == v.value}")
            assert current_cookie['value'] == v.value

    def safe_click(self, by, value, name, wait_timeout=30, sleep_timeout=2) -> bool:
        status = False
        try:
            checkbox = WebDriverWait(self.driver, wait_timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            checkbox.click()
            logger.info(f"clicked '{name}', '{value}")
            status = True
        except Exception as e:
            logger.warning(f"click '{name}' '{value}' exception: {e}, {traceback.format_exc(10)}")
        
        time.sleep(sleep_timeout)
        return status
    
    def safe_input(self, by, value, name, user_value, wait_timeout=30, sleep_timeout=1) -> bool:
        status = False
        try:
            elem = WebDriverWait(self.driver, wait_timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            elem.send_keys(user_value)
            logger.info(f"input '{name}', {value}, user value {user_value}")
            status = True
        except Exception as e:
            logger.warning(f"input {name} '{value}', user value {user_value}, exception: {e}, {traceback.format_exc(10)}")
        
        time.sleep(sleep_timeout)
        return status
    
    def wait_to_enter(self):
        y = input("please enter to continue, type y or n: ")
        if y == "n":
            sys.exit()

    def save_report(self):
        # save test prompts
        path = self.get_report_path()
        df = pd.DataFrame(self.test_prompts)
        df.to_csv(path, index=False)

    def get_report_path(self):
        name = self.__class__.__name__.lower()
        filename = f"{name}_{datetime.datetime.now().strftime('%Y_%m_%d')}.csv"
        path = settings.REPORT_DIR / filename
        return str(path)
    
    def _load_report(self):
        assert len(self.test_prompts) > 0
        n_answered = 0
        path = self.get_report_path()
        if os.path.exists(path) is False:
            return
        df = pd.read_csv(path)
        for i, row in df.iterrows():
            if pd.isna(row['chat_answer']) is False:
                self.test_prompts[i].chat_answer = row['chat_answer']
                self.test_prompts[i].chat_spend_seconds = row['chat_spend_seconds']
                n_answered += 1

        logger.info(f"n answered {n_answered}")

    @classmethod
    def parse_raw_cookies(cls, raw_cookie) -> dict:
        simple_cookie = SimpleCookie()
        simple_cookie.load(raw_cookie)
        return {k:v.value for k, v in simple_cookie.items()}
    
    def update_metrics(self):
        for item in self.test_prompts:
            if not item.chat_answer:
                continue
            item.input_length = len(item.prompt)
            item.output_length = len(item.chat_answer)
            item.similarity = 0.0
            item.output_speed = len(item.chat_answer) / item.chat_spend_seconds
            item.is_right = self._check_answer(item.chat_answer, item.full_answer)

    def _check_answer(self, factual:str, expected:str) -> bool:
        '''maybe need to overwrite'''
        flags = [
            '正确答案是',
            '正确选项是',
            '答案是',
            '综上所述',
        ]
        for flag in flags:
            offset = factual.find(flag)
            if offset < 0:
                continue
            if factual.find(expected, offset, offset + len(flag) + len(expected) + 10) >= 0:
                return True
            
        # not found any flag
        if factual.strip().find(expected) == 0:
            return True
            
        return False
