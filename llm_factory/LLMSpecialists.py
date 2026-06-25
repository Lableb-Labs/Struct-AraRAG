from llm_factory.prompts import *
from llm_factory.LLMCaller import LLMCaller
import json


class LLMSpecialists():

    def __init__(self):
        super().__init__()



    def _call_llm_with_json_retry(self, messages, llm_config, max_retries=2):
        """
        Shared helper for JSON-based LLM calls with retry logic.
        """

        for attempt in range(1, max_retries + 1):
            response = LLMCaller(**llm_config).send_model_request(messages)

            if response.status_code != 200:
                return None

            response_text = response.json()["choices"][0]["message"]["content"]

            if response_text:
                response_text = response_text.replace("```json", "").replace("```", "")

            try:
                return json.loads(response_text)

            except json.JSONDecodeError as e:
                print(f"[Attempt {attempt}] JSON decode failed: {e}")

                if attempt < max_retries:
                    messages.append({"role": "assistant", "content": response_text})
                    messages.append({
                        "role": "user",
                        "content": "Return ONLY valid JSON. No explanation, no markdown."
                    })
                else:
                    return None

    def router(self, question, max_retries=2):
        messages = [
            {"role": "system", "content": system_router},
            {"role": "user", "content": user_router},
            {"role": "user", "content": f"The User Question: {question}."}
        ]

        llm_config = {
            "temperature": 0.1,
            "top_k": 0.3,
            "top_p": 0.6,
            "max_token_generation": 900
        }

        return self._call_llm_with_json_retry(messages, llm_config, max_retries)

    def question_answering(self, question, content, max_retries=2):
        messages = [
            {"role": "system", "content": system_question_answering},
            {
                "role": "user",
                "content": f"{user_question_answering}.\n"
                           f"The User Question: {question}.\n"
                           f"The Legislation: {content}"
            },
        ]

        llm_config = {
            "temperature": 0.1,
            "top_k": 0.4,
            "top_p": 0.6,
            "max_token_generation": 3000
        }

        return self._call_llm_with_json_retry(messages, llm_config, max_retries)


    def judge(self, system1, system2, ground_truth, max_retries=2):
        messages = [
            {"role": "system", "content": system_judge},
            {"role": "user", "content": user_judge},
            {
                "role": "user",
                "content": (
                    f"Router System Results: {system1}.\n"
                    f"Basic System Results: {system2}.\n"
                    f"Ground Truth: {ground_truth}"
                )
            },
        ]

        llm_config = {
            "temperature": 0.1,
            "top_k": 0.3,
            "top_p": 0.6,
            "max_token_generation": 900,
        }

        return self._call_llm_with_json_retry(
            messages=messages,
            llm_config=llm_config,
            max_retries=max_retries,
        )