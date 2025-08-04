#!/usr/bin/env python3
from smolagents import ToolCallingAgent

from ..utils import load_prompt, model, WORK_PATH
from ..tools.file_tool import FileSaveTool
from .section_generate import section_generate_agent


content_generate_prompt = load_prompt("prompts/content_generate.yaml")

content_generate_agent = ToolCallingAgent(
    tools=[FileSaveTool(work_path=WORK_PATH)],
    model=model,
    name="content_generate_agent_manager",
    description="This is an agent that can generate PPT content based on outline JSON file and save each section as markdown files.",  
    prompt_templates=content_generate_prompt,
    managed_agents=[section_generate_agent],
    return_full_result=True,
)


if __name__ == "__main__":
    from phoenix.otel import register
    from openinference.instrumentation.smolagents import SmolagentsInstrumentor

    register()
    SmolagentsInstrumentor().instrument()

    outline_file_path = "tmp_0731/outline.json"
    with open(outline_file_path, "r") as f:
        outline = f.read()
    content_generate_agent.run(task=outline)
