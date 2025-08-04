import datetime
import sys
import os
import asyncio
from smolagents import ToolCallingAgent
from phoenix.otel import register
from openinference.instrumentation.smolagents import SmolagentsInstrumentor

register()
SmolagentsInstrumentor().instrument()

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.utils import WORK_PATH, load_prompt, model
from src.tools.file_tool import FileSaveTool
from src.tools.bocha_websearch import BochaWebSearch
from src.agents.outline_generate import outline_generate_agent


task = """生成一个关于“DOTA2 雪如意比赛”的PPT大纲"""


result = outline_generate_agent.run(task=task)
print(result.output)
