'''Minimax https://hailuoai.com/
'''
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
import rpa


logger = logging.getLogger(__name__)


class Minimax(BaseLLMTest):
    def __init__(self, headless: bool, cookie: str, token:str, phone:str) -> None:
        super().__init__(headless, cookie, token)
        rpa.init()
        self.phone = phone

    def _get_answer(self, query):
        clean_query = query.replace("\n", "[enter]")
        rpa.url("https://hailuoai.com/")

        # is login?
        login_xpath = '//*[@id="root"]/div/div/main/div[1]/div[3]/div[3]'
        if rpa.exist(login_xpath) and rpa.read(login_xpath) == '登录':
            rpa.click(login_xpath)
            # to login
            rpa.type('//*[@id="phone"]', self.phone)
            rpa.click('//*[@id="root"]/div/section/div/div/div/div[3]/form/div[2]/div[2]/button')
            time.sleep(30)

        rpa.click('//*[@id="chat-input"]')
        rpa.type('//*[@id="chat-input"]', clean_query)
        rpa.click('//*[@id="input-send-icon"]')

        start = time.time()
        wait_time = 0.01
        logger.info("start to wait")
        for i in range(int(30/wait_time)):
            if rpa.exist('//*[@id="chat-card-list"]/div[2]/div/div[2]/div[2]/div[1]/div[1]/span[2]'):
                break
            rpa.wait(wait_time)
        end = time.time()
        logger.info(f"stop to wait, count {i}, spend {end - start} seconds")

        if rpa.exist('//*[@id="chat-card-list"]/div[2]/div/div[2]/div[2]/div[1]/div[1]/span[2]') is False:
            answer = ''
        else:
            answer = rpa.read('//*[@id="chat-card-list"]/div[2]/div/div[2]/div[1]')
        self.last_spend_seconds = end - start
        logger.info(f"prompt {query}, answer {answer}")
        return answer
