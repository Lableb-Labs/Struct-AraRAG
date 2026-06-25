import os

from dotenv import load_dotenv
load_dotenv(
    dotenv_path='.env',
)

llm_url = os.getenv("LLM_URL")
llm_key = os.getenv("LLM_KEY")
