import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.agents.ppt_generate import ppt_generate_agent


task = """生成一个关于“苏超比赛”的PPT"""

ppt_generate_agent.run(task=task)
