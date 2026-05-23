#!/usr/bin/env python3

from google.adk.agents.llm_agent import Agent
from .prompt.root_instruction import root_instruction
from .tools.save_user import save_user
from .callbacks import before_agent_callback

from .agents.python_tutor import python_agent
from .agents.programming_agent import programming_agent

root_agent = Agent(
    name='coding_tutor_agent',
    model='gemini-2.5-flash',
    sub_agents=[python_agent, programming_agent],
    description='You are Mr.Brown, the orchestrator with the role of directing the user to the correct tutor',
    instruction=root_instruction,
    tools=[save_user],
    before_agent_callback=before_agent_callback
    )
