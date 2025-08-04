import sys
import os
from phoenix.otel import register
from openinference.instrumentation.smolagents import SmolagentsInstrumentor

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.agents.ppt_generate import ppt_generate_agent
from src.utils import WORK_PATH


register()
SmolagentsInstrumentor().instrument()


task = "生成一个关于“DOTA2 雪如意比赛”的PPT"
ppt_generate_agent.run(task=task)
