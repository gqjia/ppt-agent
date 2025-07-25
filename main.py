from smolagents import GradioUI
from src.agents.ppt_generate import ppt_generate_agent


if __name__ == "__main__":
    ui = GradioUI(ppt_generate_agent)
    ui.launch(pwa=True)
    # ppt_generate_agent.run(task="生成一个关于AI的PPT")
