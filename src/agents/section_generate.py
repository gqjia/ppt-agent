#!/usr/bin/env python3
from smolagents import ToolCallingAgent

from ..utils import load_prompt, model
from ..tools.bocha_websearch import BochaWebSearch


section_generate_prompt = load_prompt("prompts/section_generate.yaml")

section_generate_agent = ToolCallingAgent(
    tools=[BochaWebSearch()],
    model=model,
    name="section_generate_agent",
    description="This is an agent that can generate PPT section content.",  
    prompt_templates=section_generate_prompt,
    planning_interval=5,
    return_full_result=True,
)