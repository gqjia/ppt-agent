import sys
import os
from phoenix.otel import register
from openinference.instrumentation.smolagents import SmolagentsInstrumentor

register()
SmolagentsInstrumentor().instrument()
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.agents.content_manager import content_generate_agent


outline_file = "test/outline_20250801112548/test_0/outline.json"
with open(outline_file, "r") as f:
    outline = f.read()
text = f"{outline}"
content_generate_agent.run(text)
