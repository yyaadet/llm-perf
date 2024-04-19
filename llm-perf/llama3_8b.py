'''ollama test llama3 8B
'''

from ollama import Client
from httpx import BasicAuth
client = Client(host='https://notebook.casdao.com:41227', auth=BasicAuth("tom", "7i9CMFydMM3R"))


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


class LLaMA3_8B(BaseLLMTest):
    def __init__(self, headless: bool, cookie: str, token:str) -> None:
        super().__init__(headless, cookie, token)

    def _get_answer(self, query) -> str:
        resp = client.chat(model="llama3:8b", messages=[
            {
                'role': 'user',
                'content': "用中文回答如下的问题"
            },
            {
                'role': 'user',
                'content': query
            }
        ], stream=True)
        answer = ''
        for chunk in resp:
            answer += chunk['message']['content']

        logger.info(f"prompt {query}, answer {answer}")
        return answer