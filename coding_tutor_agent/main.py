#!/usr/bin/env python3

import uvicorn
from uuid import uuid4

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .schema.session import ChatRequest, ChatResponse
from .adk_runner import runner, session_service, APP_NAME
from google.genai.types import Content, Part

app = FastAPI()


@app.get("/")
async def home():
    return {"message": "Success"}


@app.post("/chat", response_model=ChatResponse)
async def ask_question(request: ChatRequest):
    session_id = request.session_id or str(uuid4())
    user_id = session_id

    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id
    )

    if not session:
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id
        )

    response_text = ""
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=Content(role="user", parts=[Part.from_text(text=request.message)])
    ):
        if event.is_final_response() and event.content and event.content.parts:
            response_text = event.content.parts[0].text

    return ChatResponse(response=response_text, session_id=session_id)


if __name__ == "__main__":
    uvicorn.run("coding_tutor_agent.main:app", port=5000, reload=True)
