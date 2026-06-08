#!/usr/bin/env python3

from fastapi import Request
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from fastapi.responses import JSONResponse


def get_user_from_request(request: Request) -> str:
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        api_key = auth.removeprefix("Bearer ").strip()
        if api_key:
            return api_key
    return get_remote_address(request)


limiter = Limiter(key_func=get_user_from_request)


def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. You are allowed 5 requests per hour."},
    )
