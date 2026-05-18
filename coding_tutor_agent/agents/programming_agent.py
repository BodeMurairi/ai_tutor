#!/usr/bin/env python3

from google.adk.agents import Agent
from ..prompt.other_programming_instruction import prompt
from ..tools.save_user import update_session_tool
from ..callbacks import after_agent_callback

programming_agent = Agent(
    name="coding_agent",
    model="gemini-2.5-flash",
    description="Specialist for all programming languages except Python: JavaScript, Java, C++, Rust, Go, and others",
    instruction=prompt,
    tools=[update_session_tool],
    after_agent_callback=after_agent_callback
)
