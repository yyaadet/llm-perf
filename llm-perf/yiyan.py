'''百度文心一言 3.5
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
import rpa

import settings



logger = logging.getLogger(__name__)


class Yiyan(BaseLLMTest):

    def __init__(self, headless: bool, raw_cookie: str, token: str, username:str, password) -> None:
        super().__init__(headless, raw_cookie, token)
        rpa.init()
        self.username = username
        self.password = password
    
    def _get_answer(self, query) -> str:
        clean_query = query.replace("\n", "[enter]")
        rpa.url("https://yiyan.baidu.com/")

        if rpa.exist('//*[@id="root"]/div[1]/div[2]/div/div[2]/div/div') and rpa.read('//*[@id="root"]/div[1]/div[2]/div/div[2]/div/div') == '立即登录':
            # to login
            rpa.type('//*[@id="TANGRAM__PSP_11__userName"]', self.username)
            rpa.type('//*[@id="TANGRAM__PSP_11__password"]', self.password)
            rpa.click('//*[@id="TANGRAM__PSP_11__submit"]')
            time.sleep(3)
            
        # //*[@id="eb_model_footer"]/div/div[3]/div/div[1]/div[2]
        rpa.click('//*[@id="eb_model_footer"]/div/div[3]/div/div[1]/div[2]')
        rpa.type('//*[@id="eb_model_footer"]/div/div[3]/div/div[1]/div[2]', clean_query)
        rpa.click('//*[@id="eb_model_footer"]/div/div[3]/div/div[2]/span')

        start = time.time()
        wait_time = 0.01
        logger.info("start to wait")
        for i in range(int(30/wait_time)):
            if rpa.exist('//*[@id="DIALOGUE_CARD_LIST_ID"]/div/div[3]/div/div[2]/div[2]/div[2]/div[2]/span[1]'):
                break
            rpa.wait(wait_time)
        end = time.time()
        logger.info(f"stop to wait, count {i}, spend {end - start} seconds")

        if rpa.exist('//*[@id="DIALOGUE_CARD_LIST_ID"]/div/div[3]/div/div[2]/div[2]/div[2]/div[2]/span[1]') is False:
            answer = ''
        else:
            answer = rpa.read('//*[@id="DIALOGUE_CARD_LIST_ID"]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]')
        self.last_spend_seconds = end - start
        logger.info(f"prompt {query}, answer {answer}")
        return answer
        