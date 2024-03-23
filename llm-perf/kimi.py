from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service

from http.cookies import SimpleCookie
import json
import requests
from base import BaseLLMTest
import time
import logging
import datetime
from tqdm import tqdm
import pandas as pd
import settings

logger = logging.getLogger(__name__)


class Kimi(BaseLLMTest):
    def __init__(self, headless: bool, cookie: str, token:str, chat_id:str) -> None:
        super().__init__(headless, cookie, token)
        self.chat_id = chat_id
        self.home_url = "https://kimi.moonshot.cn/"

    def _get_answer(self, query) -> str:
        url = f'https://kimi.moonshot.cn/api/chat/{self.chat_id}/completion/stream'
        r = requests.post(
            url,
            json={"messages":[{"role":"user","content":query}],"refs":[],"use_search":True},
            cookies=self.parse_raw_cookies(self.raw_cookie),
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15',
                'Authorization': f"Bearer {self.token}",
                "Connection": "keep-alive",
            },
            stream=True
        )
        answer = ''
        for line in r.iter_lines():
            if not line:
                continue
            line = line.decode()
            #logger.info(f"receive '{line}'")
            if line.startswith("data:") is False:
                logger.warning(f"not found data: in {line}")
                continue
            try:
                item = json.loads(line[5:])
            except Exception as e:
                logger.warning(f"parse {line} exception: {e}")
                continue
            if 'event' in item and item['event'] == 'cmpl':
                answer += item['text']
        
        logger.info(f"prompt {query}, answer {answer}")
        return answer

    def test_with_selenium(self) -> bool:
        self.load_test_prompts()

        driver = self.driver
        driver.get(self.home_url)
        self.add_cookie(self.raw_cookie, '.kimi.moonshot.cn')
        time.sleep(3)
        driver.refresh()
        #self.wait_to_enter()
        logger.info("refreshed")
        self.check_cookie(self.raw_cookie)
        
        # login
        if not self.safe_click(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/div[1]/div/div/div', 'Login'):
            return False

        # first input
        if not self.safe_input(By.XPATH, '//*[@id="root"]/div/div[2]/div[3]/div/div[2]/div/div[3]/div[1]/div/div/div[1]/div', '第一次创建对话', '你好'):
            return False
        
        if not self.safe_click(By.XPATH, '//*[@id="send-button"]', '发送'):
            return False
        
        time.sleep(5)
        chat_id = driver.current_url.split("/")[-1]
        # get container last data index
        # //*[@id="root"]/div/div[2]/div[3]/div/div[2]/div/div[1]/div/div/div/div[2]
        container_xpath = '//*[@id="root"]/div/div[2]/div[3]/div/div[2]/div/div[1]/div/div/div/div[2]'
        container = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, container_xpath))
        )
        last_data_index = len(container.find_elements(By.CSS_SELECTOR, "div"))
        
        for item  in self.test_prompts:
            # input prompt
            if not self.safe_input(By.XPATH, '//*[@id="root"]/div/div[2]/div[3]/div/div[2]/div/div[2]/div[1]/div/div/div[1]/div', '输入prompt', item.prompt):
                continue

            if not self.safe_click(By.XPATH, '//*[@id="send-button"]', 'send'):
                continue

            start = time.time()
            # get answer
            copy_xpath = '//*[@id="chat-actions"]/div/div[1]/button[1]/span[2]'
            copy_btn = WebDriverWait(driver, 120).until(
                EC.visibility_of_element_located((By.XPATH, copy_xpath))
            )
            stop = time.time()
            answer_xpath = f'//*[@id="chat-segment-{chat_id}"]/div[2]/div[1]/div/div[1]'
            answer_elem = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, answer_xpath))
            )
            answer_text = answer_elem.text
            item.chat_answer = answer_text
            item.chat_spend_seconds = stop - start

        self.save_report('kimi')

            
            


            
        

        
        