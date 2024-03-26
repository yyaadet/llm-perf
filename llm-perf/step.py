'''阶跃星辰, 跃问 
'''
import uuid
import requests
from requests.exceptions import ChunkedEncodingError

import logging
import json
import tqdm
import time

from base import BaseLLMTest


logger = logging.getLogger(__name__)


class Step(BaseLLMTest):

    def __init__(self, headless: bool, raw_cookie: str, token: str, chat_id:str, app_id:str) -> None:
        super().__init__(headless, raw_cookie, token)
        self.chat_id = chat_id
        self.app_id = app_id
        self.session = requests.Session()
        self.request_count = 0

    def _get_answer(self, query):
        url = 'https://stepchat.cn/api/proto.chat.v1.ChatMessageService/SendMessageStream'
        content = json.dumps({"chatId":"83836053328785408","messageInfo":{"text":query}}, ensure_ascii=False)
        content = bytes(content, "utf-8")
        length = len(content).to_bytes(5)
        body = length + content
        logger.info(f"body '{body}'")
        r = self.session.post(
            url,
            data=body,
            cookies=self.parse_raw_cookies(self.raw_cookie),
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15',
                "Connection": "keep-alive",
                'Accept-Encoding': 'gzip',
                'Content-Type': 'application/connect+json',
                'oasis-appid': self.app_id,
                'oasis-platform': 'web',
                'oasis-webid': '325f81e2c7fb4889cdfadb1ec0b5b3f5ea19af92'
            },
            stream=True,
            timeout=60
        )
        self.request_count += 1

        if self.request_count % 50 == 0:
            self.update_token()
        
        answer = ''
        try:
            data = b''
            for chunk in r.iter_content(1024):
                data += chunk
            
            lines = []
            offset = 0
            while offset < len(data):
                length = int.from_bytes(data[offset:offset+5])
                offset += 5

                line = data[offset:offset+length]
                offset += length

                lines.append(line)
            
            logger.info(f"data is {data}, lines {lines}")

            for line in lines:
                if not line:
                    continue
                line = line.decode()
                start_idx = line.find("{")
                if start_idx < 0:
                    continue

                try:
                    item = json.loads(line[start_idx:])
                except Exception as e:
                    logger.warning(f"parse {line} exception: {e}")
                    continue

                '''
                if 'error' in item and 'code' in item['error'] and 'message' in item['error']:
                    if item['error'] == 'token is expired':
                        self.update_token()
                '''

                if 'textEvent' not in item:
                    continue

                if 'text' not in item['textEvent']:
                    continue

                answer += item['textEvent']['text']
        except ChunkedEncodingError as e:
            logger.warning(f"failed to get answer for {query}: {e}")
        
        logger.info(f"prompt {query}, answer {answer}")
        return answer
    
    def update_token(self):
        url = 'https://stepchat.cn/passport/proto.api.passport.v1.PassportService/RefreshToken'
        cookies = self.parse_raw_cookies(self.raw_cookie)
        r = self.session.post(
            url,
            json={},
            cookies=cookies,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15',
                "Connection": "keep-alive",
                'Accept-Encoding': 'gzip',
                'Content-Type': 'application/json',
                'oasis-appid': self.app_id,
                'oasis-platform': 'web',
                'oasis-webid': '325f81e2c7fb4889cdfadb1ec0b5b3f5ea19af92'
            },
            stream=False,
            timeout=60
        )
        set_cookies = self.parse_raw_cookies(r.headers['Set-Cookie'])
        old_cookies = cookies.copy()
        cookies['Oasis-Token'] = set_cookies['Oasis-Token']
        self.raw_cookie = ";".join([f"{k}={v}" for k, v in cookies])
        logger.info(f"update token, old cookies {old_cookies}, new cookies {cookies}, raw {self.raw_cookie}")