#!/usr/bin/env python3
from smolagents import ToolCallingAgent
from phoenix.otel import register
from openinference.instrumentation.smolagents import SmolagentsInstrumentor

from ..utils import load_prompt, model
from ..tools.bocha_websearch import BochaWebSearch


register()
SmolagentsInstrumentor().instrument()

section_generate_prompt = load_prompt("section_generate.yaml")

section_generate_agent = ToolCallingAgent(
    tools=[BochaWebSearch()],
    model=model,
    name="section_generate_agent",
    description="This is an agent that can generate PPT section content.",  
    prompt_templates=section_generate_prompt,
    planning_interval=3,
    return_full_result=True,
)