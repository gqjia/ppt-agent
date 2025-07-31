import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.agents.slide_manager import slide_manager_agent


task = """生成的章节内容文件路径列表：
tmp/section_1.md
tmp/section_2.md
tmp/section_3.md
tmp/section_4.md
tmp/section_5.md"""

slide_manager_agent.run(task=task)
