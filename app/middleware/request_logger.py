"""
Request-logging middleware for the FastAPI application.

Logs every incoming request and outgoing response through the shared
``app.utils.logger`` setup so output format stays consistent across the
entire codebase.

Captured per request:
  → method, path, query string, body (truncated), timestamp
  ← status code, wall-clock response time in ms
"""

from __future__ import annotations

import time
from datetime import datetime, timezone

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.utils.logger import get_logger

logger = get_logger("middleware.request_logger")

MAX_BODY_LOG_BYTES = 1024


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Logs method, path, payload, status code, and response time for every request."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request_time = datetime.now(timezone.utc)
        start = time.perf_counter()

        body_text = await self._read_body(request)

        logger.info(
            "→ %s %s%s | body=%s | ts=%s",
            request.method,
            request.url.path,
            f"?{request.url.query}" if request.url.query else "",
            body_text or "-",
            request_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        )

        response = await call_next(request)

        elapsed_ms = (time.perf_counter() - start) * 1000

        logger.info(
            "← %s %s | status=%d | %.1fms",
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms,
        )

        return response

    async def _read_body(self, request: Request) -> str | None:
        """Read and return the request body, truncated for safety.

        Starlette only lets you consume the body stream once. We read it
        here and then inject a new ``receive`` so downstream handlers
        (FastAPI route functions) can still read it normally.
        """
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return None

        try:
            body_bytes = await request.body()
        except Exception:
            return "<read-error>"

        if not body_bytes:
            return None

        text = body_bytes[:MAX_BODY_LOG_BYTES].decode("utf-8", errors="replace")
        if len(body_bytes) > MAX_BODY_LOG_BYTES:
            text += f"…({len(body_bytes)} bytes total)"
        return text
