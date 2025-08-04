#!/usr/bin/env python3
from smolagents import ToolCallingAgent

from ..utils import load_prompt, model, WORK_PATH
from ..tools.file_tool import FileSaveTool
from ..tools.bocha_websearch import BochaWebSearch


outline_generate_prompt = load_prompt("prompts/outline_generate.yaml")

outline_generate_agent = ToolCallingAgent(
    tools=[BochaWebSearch(), FileSaveTool(work_path=WORK_PATH)],
    model=model,
    name="outline_generate_agent",
    description="This is an agent that can generate PPT outline.",  
    prompt_templates=outline_generate_prompt,
    planning_interval=5,
    return_full_result=True,
)


if __name__ == "__main__":
    from phoenix.otel import register
    from openinference.instrumentation.smolagents import SmolagentsInstrumentor

    register()
    SmolagentsInstrumentor().instrument()

    title = "中北女人不值钱"
    outline = outline_generate_agent.run(title)
    print(outline)
