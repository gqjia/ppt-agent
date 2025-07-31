#!/usr/bin/env python3
from smolagents import ToolCallingAgent
from phoenix.otel import register
from openinference.instrumentation.smolagents import SmolagentsInstrumentor

from ..utils import load_prompt, model
from ..tools.file_tool import FileReadTool, FileSaveTool
from .slide_generate import slide_generate_agent


register()
SmolagentsInstrumentor().instrument()


slide_manager_prompt = load_prompt("slide_manager.yaml")

slide_manager_agent = ToolCallingAgent(
    tools=[FileReadTool(), FileSaveTool(default_output_dir="tmp/")],
    model=model,
    name="slide_manager_agent",
    description="This is a manager agent that coordinates multiple slide generation tasks, validates content quality, and ensures all generated slides meet the required standards.",
    prompt_templates=slide_manager_prompt,
    managed_agents=[slide_generate_agent],
    planning_interval=5,
    return_full_result=True,
)