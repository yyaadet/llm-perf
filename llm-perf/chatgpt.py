import uuid
import requests
from requests.exceptions import ChunkedEncodingError

import rpa
import logging
import json
import tqdm
import time

from openai import OpenAI

from base import BaseLLMTest


logger = logging.getLogger(__name__)


class ChatGPT(BaseLLMTest):

    def __init__(self, headless: bool, raw_cookie: str, token: str) -> None:
        super().__init__(headless, raw_cookie, token)
        rpa.init()

    def _get_answer(self, query) -> str:
        clean_query = query.replace("\n", "[enter]")
        rpa.url("https://poe.com")
        rpa.click('//*[@id="__next"]/div/div[1]/div/main/div/div/div/div[1]/div[1]/button[2]')
        rpa.type('//*[@id="__next"]/div/div[1]/div/main/div/div/div/div[1]/div[2]/div/div[1]/textarea', clean_query)
        rpa.click('//*[@id="__next"]/div/div[1]/div/main/div/div/div/div[1]/div[2]/div/button[2]')
        start = time.time()
        wait_time = 0.1
        logger.info("start to wait")
        for i in range(int(1/wait_time)):
            if rpa.exist('//*[@id="__next"]/div/div[1]/div/main/div/div/div/div[2]/div[3]/section[1]/button[1]'):
                break
            rpa.wait(wait_time)
        logger.info("stop to wait")

        if rpa.exist('//*[@id="__next"]/div/div[1]/div/main/div/div/div/div[2]/div[3]/div[2]/div[2]') is False:
            answer = ''
        else:
            answer = rpa.read('//*[@id="__next"]/div/div[1]/div/main/div/div/div/div[2]/div[3]/div[2]/div[2]')
        end = time.time()
        self.last_spend_seconds = end - start
        logger.info(f"prompt {query}, answer {answer}")
        return answer
        