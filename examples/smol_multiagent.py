import os

from smolagents import (
    CodeAgent,
    ToolCallingAgent,
    VisitWebpageTool,
    WebSearchTool,
    OpenAIModel,
    GradioUI,
)
from dotenv import load_dotenv


load_dotenv()
MODEL_API_KEY = os.getenv('MODEL_API_KEY')
MODEL_ENDPOINT = os.getenv('MODEL_ENDPOINT')
MODEL_NAME = os.getenv('MODEL_NAME', 'gpt-4o-mini')


model = OpenAIModel(
    model_id=MODEL_NAME,
    api_key=MODEL_API_KEY,
    api_base=MODEL_ENDPOINT
)


search_agent = ToolCallingAgent(
    tools=[WebSearchTool(), VisitWebpageTool()],
    model=model,
    name="search_agent",
    description="This is an agent that can do web search.",
    return_full_result=True,
)

chinese_agent = ToolCallingAgent(
    tools=[],
    model=model,
    name="chinese_agent",
    description="你是一个中文翻译助手，请将输入的文本翻译成中文。",
    return_full_result=True,
)


manager_agent = CodeAgent(
    tools=[],
    model=model,
    managed_agents=[search_agent, chinese_agent],
    additional_authorized_imports=[
        'time', 'math', 'statistics', 'datetime', 'itertools', 're', 
        'unicodedata', 'queue', 'collections', 'random', 'stat', 'ast'
    ],
    return_full_result=True,
)


run_result = manager_agent.run(
    "中国 2023 年 GDP 是多少？"
)
print("Here is the token usage for the manager agent", run_result.token_usage)
print("Here are the timing informations for the manager agent:", run_result.timing)

GradioUI(manager_agent, file_upload_folder="./data").launch(pwa=True)
