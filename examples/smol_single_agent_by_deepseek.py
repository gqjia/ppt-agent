#!/usr/bin/env python3
import os

from dotenv import load_dotenv
from smolagents.agents import ToolCallingAgent
from smolagents.models import OpenAIModel
from smolagents.tools import tool


load_dotenv()
MODEL_API_KEY = os.getenv('MODEL_API_KEY')
MODEL_ENDPOINT = os.getenv('MODEL_ENDPOINT')
MODEL_NAME = os.getenv('MODEL_NAME', 'gpt-4o-mini')
if not MODEL_API_KEY or not MODEL_ENDPOINT:
    raise ValueError("请在 .env 文件中设置 MODEL_API_KEY 和 MODEL_ENDPOINT 环境变量")


@tool
def get_current_weather(location: str, unit: str = "celsius") -> str:
    """获取指定地点的当前天气
    
    Args:
        location: 要查询天气的地点名称
        unit: 温度单位，默认为摄氏度 (celsius)，可以是华氏度 (fahrenheit)
    
    Returns:
        当前天气的描述字符串
    """
    return f"当前 {location} 的天气是晴天，温度为 25 {unit}"


def create_weather_agent():
    model = OpenAIModel(
        model_id=MODEL_NAME,
        api_base=MODEL_ENDPOINT,
        api_key=MODEL_API_KEY
    )
    agent = ToolCallingAgent(
        tools=[get_current_weather],
        model=model
    )
    return agent


if __name__ == "__main__":
    weather_agent = create_weather_agent()
    query = "请告诉我北京的当前天气，单位用摄氏度"
    print(f"查询: {query}")
    response = weather_agent.run(query)
    print(f"响应: {response}") 
