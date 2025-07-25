from smolagents import ToolCallingAgent

from .outline_generate import outline_generate_agent
from .content_generate import content_generate_agent
from .slide_generate import slide_generate_agent
from ..utils import load_prompt, model


ppt_generate_prompt = load_prompt("ppt_generate.yaml")


ppt_generate_agent = ToolCallingAgent(
    tools=[],
    model=model,
    name="ppt_generate_agent",
    description="This is an agent that can generate PPT.",  
    prompt_templates=ppt_generate_prompt,
    managed_agents=[
        outline_generate_agent, 
        content_generate_agent, 
        slide_generate_agent
    ],
    planning_interval=3,
    return_full_result=True,
)
