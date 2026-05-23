#!/usr/bin/env python3

from google.adk.agents import Agent
from ..prompt.python_instruction import prompt
from ..tools.save_user import update_session_tool
from ..tools.search_docs import search_docs
from ..callbacks import after_agent_callback

python_agent = Agent(
    name="python_tutor",
    model="gemini-2.5-flash",
    description="Specialist for Python programming: teaching concepts, debugging, and code execution",
    instruction=prompt,
    tools=[update_session_tool, search_docs],
    after_agent_callback=after_agent_callback
    )
