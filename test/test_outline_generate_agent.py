import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.agents.outline_generate import outline_generate_agent


outline_generate_agent.run(task="生成一个关于“DOTA2 雪如意比赛”的PPT大纲")
