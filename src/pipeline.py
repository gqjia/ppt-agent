import os
import uuid
import json
import json_repair

from smolagents import ToolCallingAgent
from phoenix.otel import register
from openinference.instrumentation.smolagents import SmolagentsInstrumentor

from .utils import load_prompt, model
from .tools.file_tool import FileReadTool, FileSaveTool
from .tools.bocha_websearch import BochaWebSearch


register()
SmolagentsInstrumentor().instrument()


work_path = os.path.join(os.getcwd(), "tmp", f"{uuid.uuid4()}")
os.makedirs(work_path, exist_ok=True)


outline_generate_prompt = load_prompt("prompts/outline_generate.yaml")
section_generate_prompt = load_prompt("prompts/section_generate.yaml")
slide_generate_prompt = load_prompt("prompts/slide_generate.yaml")
slide_manager_prompt = load_prompt("prompts/slide_manager.yaml")


outline_generate_agent = ToolCallingAgent(
    tools=[BochaWebSearch()],
    model=model,
    name="outline_generate_agent",
    description="This is an agent that can generate PPT outline.",  
    prompt_templates=outline_generate_prompt,
    planning_interval=5,
    return_full_result=True,
)
section_generate_agent = ToolCallingAgent(
    tools=[BochaWebSearch()],
    model=model,
    name="section_generate_agent",
    description="This is an agent that can generate PPT section content.",  
    prompt_templates=section_generate_prompt,
    planning_interval=5,
    return_full_result=True,
)
slide_generate_agent = ToolCallingAgent(
    tools=[FileReadTool(work_path=work_path)],
    model=model,
    name="slide_generate_agent",
    description="This is an agent that generates beautiful HTML PPT pages based on provided Markdown content. It does not read files or save files, only generates HTML content.",
    prompt_templates=slide_generate_prompt,
    planning_interval=3,
    return_full_result=True,
)
slide_manager_agent = ToolCallingAgent(
    tools=[FileSaveTool(work_path=work_path)],
    model=model,
    name="slide_manager_agent",
    description="This is an agent that can manage PPT slides.",  
    prompt_templates=slide_manager_prompt,
    managed_agents=[slide_generate_agent],
    planning_interval=3,
    return_full_result=True,
)


def ppt_generate_pipeline(task: str):
    outline_result = outline_generate_agent.run(task=task)
    outline = json_repair.loads(outline_result.output)
    with open(os.path.join(work_path, "outline.json"), "w") as f:
        json.dump(outline, f, indent=4, ensure_ascii=False)

    content_files = []
    for i, section in enumerate(outline["sections"]):
        section_generate_task = json.dumps(section, ensure_ascii=False)
        section_content_result = section_generate_agent.run(task=section_generate_task)
        section_content = section_content_result.output
        with open(os.path.join(work_path, f"section_{i}.md"), "w") as f:
            f.write(section_content)
        content_files.append(f"section_{i}.md")

    ppt_result = slide_manager_agent.run("\n".join(content_files))
    print(ppt_result.output)


ppt_generate_pipeline("生成一个关于“DOTA2 雪如意比赛”的PPT")
