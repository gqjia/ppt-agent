#!/usr/bin/env python3
from smolagents import ToolCallingAgent
from phoenix.otel import register
from openinference.instrumentation.smolagents import SmolagentsInstrumentor

from ..utils import load_prompt, model
from ..tools.file_tool import FileReadTool, FileSaveTool
from .section_generate import section_generate_agent


register()
SmolagentsInstrumentor().instrument()


content_generate_prompt = load_prompt("content_generate.yaml")

content_generate_agent = ToolCallingAgent(
    tools=[FileReadTool(), FileSaveTool(default_output_dir="tmp/")],
    model=model,
    name="content_generate_agent_manager",
    description="This is an agent that can generate PPT content based on outline JSON file and save each section as markdown files.",  
    prompt_templates=content_generate_prompt,
    managed_agents=[section_generate_agent],
    return_full_result=True,
)
