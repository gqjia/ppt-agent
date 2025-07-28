import os
import time

from smolagents import GradioUI
from loguru import logger
from src.agents.ppt_generate import ppt_generate_agent


logger.remove()
os.makedirs("logs/", exist_ok=True)
logger.add(
    f"logs/ppt_agent_at_{time.strftime('%Y-%m-%d_%H-%M-%S')}.log",
    rotation="500 MB",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
)


if __name__ == "__main__":
    # ui = GradioUI(ppt_generate_agent)
    # ui.launch(pwa=True)
    ppt_generate_agent.run(task="生成一个关于“苏超比赛”的PPT")
