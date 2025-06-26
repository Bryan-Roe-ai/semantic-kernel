#!/usr/bin/env python3
"""
Error Handling module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import sys
import logging
import traceback
from typing import Dict, Any, Optional, Callable
from functools import wraps
from fastapi import Request, Response
from starlette.responses import JSONResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('error.log', mode='a')
    ]
)

logger = logging.getLogger("ai_chat")

class ErrorResponse:
    """Standard error response formats"""

    @staticmethod
    def not_found(message: str = "Resource not found") -> Dict[str, Any]:
        """Standard 404 error response"""
        return {"error": message, "status": "not_found"}

    @staticmethod
    def bad_request(message: str = "Invalid request") -> Dict[str, Any]:
        """Standard 400 error response"""
        return {"error": message, "status": "bad_request"}

    @staticmethod
    def server_error(message: str = "Internal server error",
                     details: Optional[str] = None) -> Dict[str, Any]:
        """Standard 500 error response"""
        response = {"error": message, "status": "server_error"}
        if details:
            response["details"] = details
        return response

    @staticmethod
    def service_unavailable(service: str, message: str) -> Dict[str, Any]:
        """Standard 503 error response for unavailable services"""
        return {
            "error": message,
            "status": "service_unavailable",
            "service": service
        }

def log_error(error: Exception, context: str = ""):
    """Log an exception with context information"""
    error_type = type(error).__name__
    error_message = str(error)
    error_trace = traceback.format_exc()

    logger.error(
        f"Error in {context}: {error_type} - {error_message}\n"
        f"Traceback:\n{error_trace}"
    )

def error_handler(func: Callable) -> Callable:
    """Decorator for API endpoint error handling"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
        except Exception as e:
            endpoint_name = func.__name__
            log_error(e, endpoint_name)

            # Return appropriate error response
            if isinstance(e, FileNotFoundError):
                return JSONResponse(
                    status_code=404,
                    content=ErrorResponse.not_found(str(e))
                )
            elif isinstance(e, (ValueError, KeyError, TypeError)):
                return JSONResponse(
                    status_code=400,
                    content=ErrorResponse.bad_request(str(e))
                )
            else:
                # For security, don't expose internal error details in production
                return JSONResponse(
                    status_code=500,
                    content=ErrorResponse.server_error(
                        "An unexpected error occurred",
                        details=str(e) if is_debug_mode() else None
                    )
                )
    return wrapper

def is_debug_mode() -> bool:
    """Check if application is running in debug mode"""
    # Could be extended to read from config or environment variable
    return True  # For now, always return debug info for easier development

# Import asyncio here to avoid circular imports
import asyncio
