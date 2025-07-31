import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.agents.content_manager import content_generate_agent


outline_file = "tmp/outline.json"
with open(outline_file, "r") as f:
    outline = f.read()
text = f"生成大纲地址：{outline_file}\n\n大纲内容：\n{outline}"
content_generate_agent.run(text)
