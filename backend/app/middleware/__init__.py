"""Middleware for logging, authentication, error handling"""
import logging
import time
import json
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import structlog

logger = logging.getLogger(__name__)
structlog_logger = structlog.get_logger()


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log all requests and responses"""
    
    async def dispatch(self, request: Request, call_next):
        # Skip logging for health checks
        if request.url.path == "/health":
            return await call_next(request)
        
        start_time = time.time()
        
        # Log request
        structlog_logger.info(
            "http_request",
            method=request.method,
            path=request.url.path,
            query_params=dict(request.query_params),
            client=request.client.host if request.client else None,
        )
        
        response = await call_next(request)
        
        # Log response
        process_time = time.time() - start_time
        structlog_logger.info(
            "http_response",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            process_time=f"{process_time:.3f}s"
        )
        
        return response


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Handle and log errors"""
    
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except HTTPException as e:
            structlog_logger.error(
                "http_exception",
                status_code=e.status_code,
                detail=e.detail,
                path=request.url.path
            )
            raise
        except Exception as e:
            structlog_logger.error(
                "unhandled_exception",
                error=str(e),
                path=request.url.path,
                method=request.method,
                exc_info=True
            )
            raise


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple rate limiting"""
    
    def __init__(self, app, requests_per_minute: int = 100):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests = {}
    
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        current_minute = int(time.time() / 60)
        
        key = f"{client_ip}:{current_minute}"
        self.requests[key] = self.requests.get(key, 0) + 1
        
        if self.requests[key] > self.requests_per_minute:
            return Response(
                content=json.dumps({"detail": "Rate limit exceeded"}),
                status_code=429
            )
        
        # Clean old entries
        cutoff_minute = current_minute - 5
        for k in list(self.requests.keys()):
            if int(k.split(":")[1]) < cutoff_minute:
                del self.requests[k]
        
        return await call_next(request)
