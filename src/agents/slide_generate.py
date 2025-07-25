#!/usr/bin/env python3
from smolagents import WebSearchTool, ToolCallingAgent
from phoenix.otel import register
from openinference.instrumentation.smolagents import SmolagentsInstrumentor

from ..utils import load_prompt, model


register()
SmolagentsInstrumentor().instrument()


slid_generate_prompt = load_prompt("slide_generate.yaml")

slide_generate_agent = ToolCallingAgent(
    tools=[WebSearchTool()],
    model=model,
    name="slide_generate_agent",
    description="This is an agent that can generate beautiful HTML PPT pages based on outline and content.",
    prompt_templates=slid_generate_prompt,
    planning_interval=3,
    return_full_result=True,
)
