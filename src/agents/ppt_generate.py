from smolagents import ToolCallingAgent
from phoenix.otel import register
from openinference.instrumentation.smolagents import SmolagentsInstrumentor

from .outline_generate import outline_generate_agent
from .content_manager import content_generate_agent
from .slide_manager import slide_manager_agent
from ..utils import load_prompt, model


register()
SmolagentsInstrumentor().instrument()


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
        slide_manager_agent
    ],
    planning_interval=3,
    return_full_result=True,
)
