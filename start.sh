#!/usr/bin/env bash

source venv/bin/activate
uvicorn coding_tutor_agent.main:app --port 5000 --reload
