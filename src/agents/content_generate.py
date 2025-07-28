#!/usr/bin/env python3
import json
from smolagents import WebSearchTool, ToolCallingAgent
from phoenix.otel import register
from openinference.instrumentation.smolagents import SmolagentsInstrumentor

from ..utils import load_prompt, model
from ..tools.file_tool import FileReadTool, FileSaveTool


register()
SmolagentsInstrumentor().instrument()


section_generate_prompt = load_prompt("section_generate.yaml")
content_generate_prompt = load_prompt("content_generate.yaml")


section_generate_agent = ToolCallingAgent(
    tools=[WebSearchTool()],
    model=model,
    name="section_generate_agent",
    description="This is an agent that can generate PPT section content.",  
    prompt_templates=section_generate_prompt,
    planning_interval=3,
    return_full_result=True,
)

content_generate_agent = ToolCallingAgent(
    tools=[FileReadTool(), FileSaveTool()],
    model=model,
    name="content_generate_agent_manager",
    description="This is an agent that can generate PPT content based on outline JSON file.",  
    prompt_templates=content_generate_prompt,
    managed_agents=[section_generate_agent],
    return_full_result=True,
)
