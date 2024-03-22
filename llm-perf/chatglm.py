'''ChatGLM test
'''

from base import BaseLLMTest



class ChatGLM(BaseLLMTest):
    
    def __init__(self, headless: bool) -> None:
        super().__init__(headless)

    