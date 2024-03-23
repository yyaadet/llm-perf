'''ChatGLM4 test
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


class GLM4(BaseLLMTest):

    def __init__(self, headless: bool, raw_cookie: str, token: str, assistant_id:str, conversion_id:str) -> None:
        super().__init__(headless, raw_cookie, token)
        self.assistant_id = assistant_id
        self.conversion_id = conversion_id
        self.session = requests.Session()

    def _get_answer(self, query):
        url = 'https://chatglm.cn/chatglm/backend-api/assistant/stream'
        body = {
            "assistant_id": self.assistant_id,
            "conversation_id": self.conversion_id,
            "meta_data": {
                "is_test": False,
                "input_question_type": "xxxx",
                "channel": "",
                "draft_id": ""
            },
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": query
                        }
                    ]
                }
            ]
        }
        r = self.session.post(
            url,
            json=body,
            cookies=self.parse_raw_cookies(self.raw_cookie),
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15',
                'Authorization': f"Bearer {self.token}",
                "Connection": "keep-alive",
                'Accept-Encoding': 'gzip',
            },
            stream=True,
            timeout=60
        )
        
        answer = ''
        try:
            for line in r.iter_lines():
                if not line:
                    continue
                line = line.decode()
                if line == 'event:message':
                    continue
                if line.startswith("data:") is False:
                    logger.warning(f"not found data: in {line}")
                    continue
                try:
                    item = json.loads(line[5:])
                except Exception as e:
                    logger.warning(f"parse {line} exception: {e}")
                    continue

                if item['status'] != 'finish':
                    continue
                logger.info(f"message: {item}")
                for part in item['parts']:
                    if part['role'] == 'assistant':
                        for content in part['content']:
                            if content['type'] == 'text':
                                answer += content['text']
                            elif content['type'] == 'code':
                                answer += content['code']
        except ChunkedEncodingError as e:
            logger.warning(f"failed to get answer for {query}: {e}")
        
        logger.info(f"prompt {query}, answer {answer}")
        return answer
