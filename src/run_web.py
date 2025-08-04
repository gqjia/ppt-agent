# from smolagents import GradioUI
from phoenix.otel import register
from openinference.instrumentation.smolagents import SmolagentsInstrumentor

from .agents.ppt_generate import ppt_generate_agent
from .webui import PPTGeneratorUI


register()
SmolagentsInstrumentor().instrument()


ui = PPTGeneratorUI(agent=ppt_generate_agent)
ui.launch(pwa=True)
