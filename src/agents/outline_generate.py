#!/usr/bin/env python3
from smolagents import ToolCallingAgent
# from smolagents import WebSearchTool
from phoenix.otel import register
from openinference.instrumentation.smolagents import SmolagentsInstrumentor

from ..utils import load_prompt, model
from ..tools.file_tool import FileSaveTool
from ..tools.bocha_websearch import BochaWebSearch


register()
SmolagentsInstrumentor().instrument()


outline_generate_prompt = load_prompt("outline_generate.yaml")

outline_generate_agent = ToolCallingAgent(
    tools=[BochaWebSearch(), FileSaveTool(default_output_dir="tmp/")],
    model=model,
    name="outline_generate_agent",
    description="This is an agent that can generate PPT outline.",  
    prompt_templates=outline_generate_prompt,
    planning_interval=3,
    return_full_result=True,
)
