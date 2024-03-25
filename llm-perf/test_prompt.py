from dataclasses import dataclass


@dataclass
class TestPrompt:
    prompt: str = ''
    answer: str = ''
    full_answer: str = ''
    category: str = ''
    subject: str = ''
    chat_answer: str = ""
    chat_spend_seconds: float = 0.0

    # metrics
    similarity: float = 0.0
    input_length: int = 0
    output_length: int = 0
    output_speed: float = 0.0
    is_right: bool = False

