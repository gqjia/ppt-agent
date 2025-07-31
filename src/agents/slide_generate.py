#!/usr/bin/env python3
from smolagents import ToolCallingAgent
from phoenix.otel import register
from openinference.instrumentation.smolagents import SmolagentsInstrumentor

from ..utils import load_prompt, model


register()
SmolagentsInstrumentor().instrument()


slide_generate_prompt = load_prompt("slide_generate.yaml")

slide_generate_agent = ToolCallingAgent(
    tools=[],
    model=model,
    name="slide_generate_agent",
    description="This is an agent that generates beautiful HTML PPT pages based on provided Markdown content. It does not read files or save files, only generates HTML content.",
    prompt_templates=slide_generate_prompt,
    planning_interval=3,
    return_full_result=True,
)
