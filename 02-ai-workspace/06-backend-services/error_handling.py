"""
Comprehensive error handling module for AI workspace backend services.
Implements consistent error responses, logging, and exception handling patterns.
"""

import logging
import traceback
import sys
import os
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import json


class ErrorSeverity(Enum):
    """Error severity levels for classification and handling."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Error categories for better organization and handling."""
    VALIDATION = "validation"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    RESOURCE_NOT_FOUND = "resource_not_found"
    SERVICE_UNAVAILABLE = "service_unavailable"
    INTERNAL_SERVER_ERROR = "internal_server_error"
    EXTERNAL_API_ERROR = "external_api_error"
    DATABASE_ERROR = "database_error"
    NETWORK_ERROR = "network_error"
    TIMEOUT_ERROR = "timeout_error"


@dataclass
class ErrorContext:
    """Context information for error tracking and debugging."""
    error_id: str
    timestamp: datetime
    severity: ErrorSeverity
    category: ErrorCategory
    message: str
    details: Dict[str, Any]
    stack_trace: Optional[str] = None
    user_id: Optional[str] = None
    request_id: Optional[str] = None
    component: Optional[str] = None


class ErrorResponse:
    """Standardized error response generator for API endpoints."""
    
    @staticmethod
    def not_found(message: str = "Resource not found", details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate a 404 Not Found error response."""
        return {
            "error": {
                "code": 404,
                "type": "NOT_FOUND",
                "message": message,
                "details": details or {},
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    
    @staticmethod
    def bad_request(message: str = "Bad request", details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate a 400 Bad Request error response."""
        return {
            "error": {
                "code": 400,
                "type": "BAD_REQUEST",
                "message": message,
                "details": details or {},
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    
    @staticmethod
    def unauthorized(message: str = "Unauthorized access", details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate a 401 Unauthorized error response."""
        return {
            "error": {
                "code": 401,
                "type": "UNAUTHORIZED",
                "message": message,
                "details": details or {},
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    
    @staticmethod
    def forbidden(message: str = "Access forbidden", details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate a 403 Forbidden error response."""
        return {
            "error": {
                "code": 403,
                "type": "FORBIDDEN",
                "message": message,
                "details": details or {},
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    
    @staticmethod
    def server_error(message: str = "Internal server error", details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate a 500 Internal Server Error response."""
        return {
            "error": {
                "code": 500,
                "type": "INTERNAL_SERVER_ERROR",
                "message": message,
                "details": details or {},
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    
    @staticmethod
    def service_unavailable(message: str = "Service temporarily unavailable", details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate a 503 Service Unavailable error response."""
        return {
            "error": {
                "code": 503,
                "type": "SERVICE_UNAVAILABLE",
                "message": message,
                "details": details or {},
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    
    @staticmethod
    def timeout_error(message: str = "Request timeout", details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate a 408 Request Timeout error response."""
        return {
            "error": {
                "code": 408,
                "type": "TIMEOUT",
                "message": message,
                "details": details or {},
                "timestamp": datetime.utcnow().isoformat()
            }
        }


class AIWorkspaceException(Exception):
    """Base exception class for AI workspace errors."""
    
    def __init__(self, message: str, error_code: str = None, details: Dict[str, Any] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        self.timestamp = datetime.utcnow()


class ValidationError(AIWorkspaceException):
    """Exception raised for validation errors."""
    pass


class AuthenticationError(AIWorkspaceException):
    """Exception raised for authentication errors."""
    pass


class AuthorizationError(AIWorkspaceException):
    """Exception raised for authorization errors."""
    pass


class ResourceNotFoundError(AIWorkspaceException):
    """Exception raised when a requested resource is not found."""
    pass


class ServiceUnavailableError(AIWorkspaceException):
    """Exception raised when a service is temporarily unavailable."""
    pass


class ExternalAPIError(AIWorkspaceException):
    """Exception raised for external API errors."""
    pass


class DatabaseError(AIWorkspaceException):
    """Exception raised for database-related errors."""
    pass


class NetworkError(AIWorkspaceException):
    """Exception raised for network-related errors."""
    pass


class TimeoutError(AIWorkspaceException):
    """Exception raised for timeout errors."""
    pass


# Configure logging
def setup_error_logging(log_level: str = "INFO", log_file: Optional[str] = None):
    """Set up error logging configuration."""
    logging_config = {
        'level': getattr(logging, log_level.upper()),
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S'
    }
    
    if log_file:
        logging_config['filename'] = log_file
    
    logging.basicConfig(**logging_config)


def log_error(
    exception: Exception,
    severity: ErrorSeverity = ErrorSeverity.MEDIUM,
    category: ErrorCategory = ErrorCategory.INTERNAL_SERVER_ERROR,
    context: Optional[Dict[str, Any]] = None,
    user_id: Optional[str] = None,
    request_id: Optional[str] = None,
    component: Optional[str] = None
) -> str:
    """
    Log an error with structured information and return error ID.
    
    Args:
        exception: The exception to log
        severity: Error severity level
        category: Error category
        context: Additional context information
        user_id: User identifier if available
        request_id: Request identifier if available
        component: Component name where error occurred
        
    Returns:
        str: Unique error ID for tracking
    """
    import uuid
    
    error_id = str(uuid.uuid4())
    timestamp = datetime.utcnow()
    
    # Create error context
    error_context = ErrorContext(
        error_id=error_id,
        timestamp=timestamp,
        severity=severity,
        category=category,
        message=str(exception),
        details=context or {},
        stack_trace=traceback.format_exc(),
        user_id=user_id,
        request_id=request_id,
        component=component
    )
    
    # Get logger
    logger = logging.getLogger(__name__)
    
    # Log based on severity
    log_data = {
        'error_id': error_id,
        'severity': severity.value,
        'category': category.value,
        'message': error_context.message,
        'details': error_context.details,
        'user_id': user_id,
        'request_id': request_id,
        'component': component,
        'timestamp': timestamp.isoformat()
    }
    
    if severity == ErrorSeverity.CRITICAL:
        logger.critical(f"CRITICAL ERROR: {json.dumps(log_data, indent=2)}")
        logger.critical(f"Stack trace:\n{error_context.stack_trace}")
    elif severity == ErrorSeverity.HIGH:
        logger.error(f"HIGH SEVERITY ERROR: {json.dumps(log_data, indent=2)}")
        logger.error(f"Stack trace:\n{error_context.stack_trace}")
    elif severity == ErrorSeverity.MEDIUM:
        logger.warning(f"MEDIUM SEVERITY ERROR: {json.dumps(log_data, indent=2)}")
        if is_debug_mode():
            logger.warning(f"Stack trace:\n{error_context.stack_trace}")
    else:
        logger.info(f"LOW SEVERITY ERROR: {json.dumps(log_data, indent=2)}")
        if is_debug_mode():
            logger.info(f"Stack trace:\n{error_context.stack_trace}")
    
    return error_id


def error_handler(func):
    """
    Decorator for handling exceptions in functions and methods.
    
    Usage:
        @error_handler
        def my_function():
            # Function code here
            pass
    """
    import functools
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AIWorkspaceException:
            # Re-raise custom exceptions as-is
            raise
        except Exception as e:
            # Log unexpected exceptions and convert to appropriate custom exception
            error_id = log_error(
                e,
                severity=ErrorSeverity.HIGH,
                category=ErrorCategory.INTERNAL_SERVER_ERROR,
                component=func.__name__
            )
            
            # Convert to custom exception
            raise AIWorkspaceException(
                f"Unexpected error in {func.__name__}",
                error_code=error_id,
                details={'original_error': str(e)}
            ) from e
    
    return wrapper


def async_error_handler(func):
    """
    Decorator for handling exceptions in async functions and methods.
    
    Usage:
        @async_error_handler
        async def my_async_function():
            # Async function code here
            pass
    """
    import functools
    
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except AIWorkspaceException:
            # Re-raise custom exceptions as-is
            raise
        except Exception as e:
            # Log unexpected exceptions and convert to appropriate custom exception
            error_id = log_error(
                e,
                severity=ErrorSeverity.HIGH,
                category=ErrorCategory.INTERNAL_SERVER_ERROR,
                component=func.__name__
            )
            
            # Convert to custom exception
            raise AIWorkspaceException(
                f"Unexpected error in {func.__name__}",
                error_code=error_id,
                details={'original_error': str(e)}
            ) from e
    
    return wrapper


def is_debug_mode() -> bool:
    """Check if debug mode is enabled."""
    return os.getenv('DEBUG', 'false').lower() in ('true', '1', 'yes', 'on')


def handle_critical_error(exception: Exception, context: Optional[Dict[str, Any]] = None) -> str:
    """
    Handle critical errors that require immediate attention.
    
    Args:
        exception: The critical exception
        context: Additional context information
        
    Returns:
        str: Error ID for tracking
    """
    error_id = log_error(
        exception,
        severity=ErrorSeverity.CRITICAL,
        category=ErrorCategory.INTERNAL_SERVER_ERROR,
        context=context
    )
    
    # Additional actions for critical errors could be added here:
    # - Send alerts to monitoring systems
    # - Notify administrators
    # - Trigger automated recovery procedures
    
    return error_id


def sanitize_error_for_client(exception: Exception, include_details: bool = None) -> Dict[str, Any]:
    """
    Sanitize error information for client consumption.
    
    Args:
        exception: The exception to sanitize
        include_details: Whether to include detailed error information
        
    Returns:
        Dict containing sanitized error information
    """
    if include_details is None:
        include_details = is_debug_mode()
    
    if isinstance(exception, ValidationError):
        return ErrorResponse.bad_request(
            message=exception.message,
            details=exception.details if include_details else None
        )
    elif isinstance(exception, AuthenticationError):
        return ErrorResponse.unauthorized(
            message=exception.message,
            details=exception.details if include_details else None
        )
    elif isinstance(exception, AuthorizationError):
        return ErrorResponse.forbidden(
            message=exception.message,
            details=exception.details if include_details else None
        )
    elif isinstance(exception, ResourceNotFoundError):
        return ErrorResponse.not_found(
            message=exception.message,
            details=exception.details if include_details else None
        )
    elif isinstance(exception, ServiceUnavailableError):
        return ErrorResponse.service_unavailable(
            message=exception.message,
            details=exception.details if include_details else None
        )
    elif isinstance(exception, TimeoutError):
        return ErrorResponse.timeout_error(
            message=exception.message,
            details=exception.details if include_details else None
        )
    else:
        return ErrorResponse.server_error(
            message="An unexpected error occurred",
            details={'error_code': getattr(exception, 'error_code', None)} if include_details else None
        )


# Initialize logging on module import
setup_error_logging()