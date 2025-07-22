import os

from smolagents import OpenAIServerModel
from dotenv import load_dotenv


load_dotenv()


api_key = os.getenv("API_KEY")
llm_url = os.getenv("LLM_URL")
llm_model = os.getenv("LLM_MODEL")

deepseek_v3 = OpenAIServerModel(
    model_id=llm_model,
    api_base=llm_url,
    api_key=api_key,
)