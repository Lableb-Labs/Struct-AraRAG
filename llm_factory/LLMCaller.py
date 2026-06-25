
import requests
from llm_factory.config import *


class LLMCaller():
    def __init__(self, temperature, max_token_generation, top_k, top_p):
        self.model_end_point = llm_url
        self.temperature = temperature
        self.max_token_generation = max_token_generation
        self.top_k = top_k
        self.top_p = top_p
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {llm_key}"
        }



    def send_model_request(self, messages):
        request_body = {
            "messages": messages,
            "temperature": self.temperature,
            "top_p": self.top_k,
            "max_tokens": self.max_token_generation
        }
        response = requests.post(self.model_end_point, json=request_body, headers=self.headers)
        return response