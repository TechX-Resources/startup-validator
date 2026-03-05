# app/middleware

**Purpose:** FastAPI middleware for cross-cutting concerns — request/response logging, CORS, and future additions like auth or rate-limiting.

**Weeks:** 1–2 (request logging provided as reference), 5–6 (add auth or rate-limit middleware if needed).

## Files

| File | Description |
|------|-------------|
| `__init__.py` | Exports `RequestLoggingMiddleware` for use in `app/main.py` |
| `request_logger.py` | Logs every incoming request (method, path, body, timestamp) and outgoing response (status code, latency in ms) using the shared logger from `app/utils/` |

## How It Fits

Middleware runs **before** the route handler and **after** the response — it wraps every request without touching business logic. The logging middleware is fully implemented as a reference for how to build Starlette-based middleware.

```
Request → [RequestLoggingMiddleware] → [CORSMiddleware] → Route Handler → Response
                ↑ logs →/← entries                             ↑ your endpoint
```

## TODO (Students)

- **Week 5–6:** Consider adding authentication middleware if you wire a real LLM API key.
- **Stretch:** Add a rate-limiting middleware to protect the `/validate-idea` endpoint.
