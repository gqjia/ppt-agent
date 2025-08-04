#!/usr/bin/env python3
from smolagents import ToolCallingAgent

from ..utils import load_prompt, model, WORK_PATH
from ..tools.file_tool import FileReadTool, FileSaveTool
from .slide_generate import slide_generate_agent


slide_manager_prompt = load_prompt("prompts/slide_manager.yaml")

slide_manager_agent = ToolCallingAgent(
    tools=[FileSaveTool(work_path=WORK_PATH)],
    model=model,
    name="slide_manager_agent",
    description="This is a manager agent that coordinates multiple slide generation tasks, validates content quality, and ensures all generated slides meet the required standards.",
    prompt_templates=slide_manager_prompt,
    managed_agents=[slide_generate_agent],
    planning_interval=5,
    return_full_result=True,
)


if __name__ == "__main__":
    from phoenix.otel import register
    from openinference.instrumentation.smolagents import SmolagentsInstrumentor

    register()
    SmolagentsInstrumentor().instrument()
    
    slide_manager_agent.run(task="中北女人不值钱")
    