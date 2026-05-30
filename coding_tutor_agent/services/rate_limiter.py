#!/usr/bin/env python3

import jwt
from fastapi import Request
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from fastapi.responses import JSONResponse

from ..config.config import JWT_SECRET


def get_user_from_request(request: Request) -> str:
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        token = auth.removeprefix("Bearer ")
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            return payload.get("sub", get_remote_address(request))
        except jwt.InvalidTokenError:
            pass
    return get_remote_address(request)


limiter = Limiter(key_func=get_user_from_request)


def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    return JSONResponse(
        status_code=429,
        content={"detail": f"Rate limit exceeded. You are allowed 5 requests per hour."},
    )
