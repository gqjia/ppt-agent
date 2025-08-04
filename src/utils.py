import os
import yaml
import uuid

from jinja2 import StrictUndefined, Template
from smolagents import PromptTemplates, OpenAIModel
from dotenv import load_dotenv
from loguru import logger


load_dotenv()
MODEL_API_KEY = os.getenv('MODEL_API_KEY')
MODEL_ENDPOINT = os.getenv('MODEL_ENDPOINT')
MODEL_NAME = os.getenv('MODEL_NAME')


model = OpenAIModel(
    model_id=MODEL_NAME,
    api_key=MODEL_API_KEY,
    api_base=MODEL_ENDPOINT
)


WORK_PATH = f"tmp/{uuid.uuid4()}"
# os.makedirs(WORK_PATH, exist_ok=True)


def load_prompt(prompt_file: str) -> PromptTemplates:
    yaml_path = os.path.join(os.path.dirname(__file__), prompt_file)
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.error(f"警告：未找到提示模板文件 {yaml_path}，将使用默认模板")
        return None
    except yaml.YAMLError as e:
        logger.error(f"警告：解析 YAML 文件时出错 {e}，将使用默认模板")
        return None
