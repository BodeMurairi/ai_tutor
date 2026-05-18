#!/usr/bin/env python3

from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search
from .prompt.instruction import prompt

root_agent = Agent(
    name='coding_tutor_agent',
    model='gemini-2.5-flash',
    description='You are Mr.Brown, a coding tutor with the goal of teaching user programming',
    instruction=prompt,
    tools=[google_search]
)
