#!/usr/bin/env python3

import uvicorn
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env", override=True)

from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from .routers.auth import router as auth_router
from .routers.chat import router as chat_router
from .services.rate_limiter import limiter, rate_limit_exceeded_handler


app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

app.include_router(auth_router)
app.include_router(chat_router)


@app.get("/")
async def home():
    return {"message": "Success"}


@app.get("/health")
async def health():
    return {"status": "Running"}


if __name__ == "__main__":
    uvicorn.run("coding_tutor_agent.main:app", port=5000, reload=True)
