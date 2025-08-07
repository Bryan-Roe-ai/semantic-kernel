#!/usr/bin/env python3
"""
import asyncio
Test module for error handling

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path
import os
import json
from datetime import datetime

# Add the module path to sys.path for importing
sys.path.insert(0, str(Path(__file__).parent.parent))

from error_handling import (
import logging
    ErrorResponse, ErrorSeverity, ErrorCategory, ErrorContext,
    AIWorkspaceException, ValidationError, AuthenticationError,
    AuthorizationError, ResourceNotFoundError, ServiceUnavailableError,
    ExternalAPIError, DatabaseError, NetworkError, TimeoutError,
    log_error, error_handler, async_error_handler, is_debug_mode,
    handle_critical_error, sanitize_error_for_client, setup_error_logging
)


class TestErrorResponse(unittest.TestCase):
    """Test cases for ErrorResponse class"""

    def test_not_found_response(self):
        """Test ErrorResponse.not_found method."""
        response = ErrorResponse.not_found("Resource not found")

        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], 404)
        self.assertEqual(response["error"]["type"], "NOT_FOUND")
        self.assertEqual(response["error"]["message"], "Resource not found")
        self.assertIn("timestamp", response["error"])

    def test_not_found_with_details(self):
        """Test ErrorResponse.not_found with details."""
        details = {"resource_id": "123", "resource_type": "user"}
        response = ErrorResponse.not_found("User not found", details)

        self.assertEqual(response["error"]["details"], details)

    def test_bad_request_response(self):
        """Test ErrorResponse.bad_request method."""
        response = ErrorResponse.bad_request("Invalid input")

        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], 400)
        self.assertEqual(response["error"]["type"], "BAD_REQUEST")
        self.assertEqual(response["error"]["message"], "Invalid input")

    def test_unauthorized_response(self):
        """Test ErrorResponse.unauthorized method."""
        response = ErrorResponse.unauthorized("Invalid credentials")

        self.assertEqual(response["error"]["code"], 401)
        self.assertEqual(response["error"]["type"], "UNAUTHORIZED")
        self.assertEqual(response["error"]["message"], "Invalid credentials")

    def test_forbidden_response(self):
        """Test ErrorResponse.forbidden method."""
        response = ErrorResponse.forbidden("Access denied")

        self.assertEqual(response["error"]["code"], 403)
        self.assertEqual(response["error"]["type"], "FORBIDDEN")
        self.assertEqual(response["error"]["message"], "Access denied")

    def test_server_error_response(self):
        """Test ErrorResponse.server_error method."""
        response = ErrorResponse.server_error("Database connection failed")

        self.assertEqual(response["error"]["code"], 500)
        self.assertEqual(response["error"]["type"], "INTERNAL_SERVER_ERROR")
        self.assertEqual(response["error"]["message"], "Database connection failed")

    def test_service_unavailable_response(self):
        """Test ErrorResponse.service_unavailable method."""
        response = ErrorResponse.service_unavailable("Maintenance in progress")

        self.assertEqual(response["error"]["code"], 503)
        self.assertEqual(response["error"]["type"], "SERVICE_UNAVAILABLE")
        self.assertEqual(response["error"]["message"], "Maintenance in progress")

    def test_timeout_error_response(self):
        """Test ErrorResponse.timeout_error method."""
        response = ErrorResponse.timeout_error("Request took too long")

        self.assertEqual(response["error"]["code"], 408)
        self.assertEqual(response["error"]["type"], "TIMEOUT")
        self.assertEqual(response["error"]["message"], "Request took too long")


class TestCustomExceptions(unittest.TestCase):
    """Test cases for custom exception classes"""

    def test_ai_workspace_exception(self):
        """Test AIWorkspaceException base class."""
        exception = AIWorkspaceException("Test error", "ERR_001", {"detail": "value"})

        self.assertEqual(str(exception), "Test error")
        self.assertEqual(exception.message, "Test error")
        self.assertEqual(exception.error_code, "ERR_001")
        self.assertEqual(exception.details, {"detail": "value"})
        self.assertIsInstance(exception.timestamp, datetime)

    def test_validation_error(self):
        """Test ValidationError exception."""
        exception = ValidationError("Invalid email format")

        self.assertIsInstance(exception, AIWorkspaceException)
        self.assertEqual(exception.message, "Invalid email format")

    def test_authentication_error(self):
        """Test AuthenticationError exception."""
        exception = AuthenticationError("Invalid token")

        self.assertIsInstance(exception, AIWorkspaceException)
        self.assertEqual(exception.message, "Invalid token")

    def test_authorization_error(self):
        """Test AuthorizationError exception."""
        exception = AuthorizationError("Insufficient permissions")

        self.assertIsInstance(exception, AIWorkspaceException)
        self.assertEqual(exception.message, "Insufficient permissions")

    def test_resource_not_found_error(self):
        """Test ResourceNotFoundError exception."""
        exception = ResourceNotFoundError("User not found")

        self.assertIsInstance(exception, AIWorkspaceException)
        self.assertEqual(exception.message, "User not found")


class TestErrorLogging(unittest.TestCase):
    """Test cases for error logging functionality"""

    @patch('error_handling.logging.getLogger')
    def test_log_error_basic(self, mock_get_logger):
        """Test basic error logging functionality."""
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger

        exception = Exception("Test exception")
        error_id = log_error(exception)

        self.assertIsInstance(error_id, str)
        self.assertTrue(len(error_id) > 0)
        mock_logger.warning.assert_called_once()

    @patch('error_handling.logging.getLogger')
    def test_log_error_critical(self, mock_get_logger):
        """Test critical error logging."""
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger

        exception = Exception("Critical error")
        error_id = log_error(
            exception,
            severity=ErrorSeverity.CRITICAL,
            category=ErrorCategory.DATABASE_ERROR
        )

        self.assertIsInstance(error_id, str)
        mock_logger.critical.assert_called()

    @patch('error_handling.logging.getLogger')
    def test_log_error_with_context(self, mock_get_logger):
        """Test error logging with context."""
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger

        exception = Exception("Error with context")
        context = {"user_id": "123", "operation": "create_user"}

        error_id = log_error(
            exception,
            context=context,
            user_id="123",
            request_id="req-456",
            component="user_service"
        )

        self.assertIsInstance(error_id, str)
        mock_logger.warning.assert_called_once()


class TestErrorHandlers(unittest.TestCase):
    """Test cases for error handler decorators"""

    def test_error_handler_decorator_success(self):
        """Test error_handler decorator with successful function."""

        @error_handler
        def successful_function():
            return "success"

        result = successful_function()
        self.assertEqual(result, "success")

    @patch('error_handling.log_error')
    def test_error_handler_decorator_exception(self, mock_log_error):
        """Test error_handler decorator with exception."""
        mock_log_error.return_value = "error-123"

        @error_handler
        def failing_function():
            raise Exception("Test exception")

        with self.assertRaises(AIWorkspaceException) as context:
            failing_function()

        self.assertIn("Unexpected error in failing_function", str(context.exception))
        mock_log_error.assert_called_once()

    def test_error_handler_preserves_custom_exceptions(self):
        """Test that error_handler preserves custom exceptions."""

        @error_handler
        def function_with_custom_exception():
            raise ValidationError("Invalid input")

        with self.assertRaises(ValidationError):
            function_with_custom_exception()

    @patch('error_handling.log_error')
    async def test_async_error_handler_decorator(self, mock_log_error):
        """Test async_error_handler decorator."""
        mock_log_error.return_value = "error-456"

        @async_error_handler
        async def failing_async_function():
            raise Exception("Async test exception")

        with self.assertRaises(AIWorkspaceException):
            await failing_async_function()

        mock_log_error.assert_called_once()


class TestUtilityFunctions(unittest.TestCase):
    """Test cases for utility functions"""

    @patch.dict(os.environ, {'DEBUG': 'true'})
    def test_is_debug_mode_true(self):
        """Test is_debug_mode returns True when DEBUG is set."""
        self.assertTrue(is_debug_mode())

    @patch.dict(os.environ, {'DEBUG': 'false'})
    def test_is_debug_mode_false(self):
        """Test is_debug_mode returns False when DEBUG is false."""
        self.assertFalse(is_debug_mode())

    @patch.dict(os.environ, {}, clear=True)
    def test_is_debug_mode_default(self):
        """Test is_debug_mode returns False by default."""
        self.assertFalse(is_debug_mode())

    @patch('error_handling.log_error')
    def test_handle_critical_error(self, mock_log_error):
        """Test handle_critical_error function."""
        mock_log_error.return_value = "critical-error-123"

        exception = Exception("Critical system failure")
        context = {"system": "database", "operation": "backup"}

        error_id = handle_critical_error(exception, context)

        self.assertEqual(error_id, "critical-error-123")
        mock_log_error.assert_called_once_with(
            exception,
            severity=ErrorSeverity.CRITICAL,
            category=ErrorCategory.INTERNAL_SERVER_ERROR,
            context=context
        )


class TestErrorSanitization(unittest.TestCase):
    """Test cases for error sanitization"""

    def test_sanitize_validation_error(self):
        """Test sanitization of ValidationError."""
        exception = ValidationError("Invalid email", details={"field": "email"})
        result = sanitize_error_for_client(exception, include_details=True)

        self.assertEqual(result["error"]["code"], 400)
        self.assertEqual(result["error"]["message"], "Invalid email")
        self.assertEqual(result["error"]["details"], {"field": "email"})

    def test_sanitize_authentication_error(self):
        """Test sanitization of AuthenticationError."""
        exception = AuthenticationError("Invalid credentials")
        result = sanitize_error_for_client(exception, include_details=False)

        self.assertEqual(result["error"]["code"], 401)
        self.assertEqual(result["error"]["message"], "Invalid credentials")
        self.assertIsNone(result["error"]["details"])

    def test_sanitize_authorization_error(self):
        """Test sanitization of AuthorizationError."""
        exception = AuthorizationError("Access denied")
        result = sanitize_error_for_client(exception)

        self.assertEqual(result["error"]["code"], 403)
        self.assertEqual(result["error"]["message"], "Access denied")

    def test_sanitize_resource_not_found_error(self):
        """Test sanitization of ResourceNotFoundError."""
        exception = ResourceNotFoundError("User not found")
        result = sanitize_error_for_client(exception)

        self.assertEqual(result["error"]["code"], 404)
        self.assertEqual(result["error"]["message"], "User not found")

    def test_sanitize_service_unavailable_error(self):
        """Test sanitization of ServiceUnavailableError."""
        exception = ServiceUnavailableError("Service down for maintenance")
        result = sanitize_error_for_client(exception)

        self.assertEqual(result["error"]["code"], 503)
        self.assertEqual(result["error"]["message"], "Service down for maintenance")

    def test_sanitize_timeout_error(self):
        """Test sanitization of TimeoutError."""
        exception = TimeoutError("Request timeout")
        result = sanitize_error_for_client(exception)

        self.assertEqual(result["error"]["code"], 408)
        self.assertEqual(result["error"]["message"], "Request timeout")

    def test_sanitize_generic_exception(self):
        """Test sanitization of generic exceptions."""
        exception = Exception("Unexpected error")
        result = sanitize_error_for_client(exception)

        self.assertEqual(result["error"]["code"], 500)
        self.assertEqual(result["error"]["message"], "An unexpected error occurred")


class TestErrorContext(unittest.TestCase):
    """Test cases for ErrorContext dataclass"""

    def test_error_context_creation(self):
        """Test ErrorContext creation."""
        timestamp = datetime.utcnow()
        context = ErrorContext(
            error_id="error-123",
            timestamp=timestamp,
            severity=ErrorSeverity.HIGH,
            category=ErrorCategory.DATABASE_ERROR,
            message="Database connection failed",
            details={"host": "localhost", "port": 5432},
            user_id="user-456",
            request_id="req-789",
            component="database_service"
        )

        self.assertEqual(context.error_id, "error-123")
        self.assertEqual(context.timestamp, timestamp)
        self.assertEqual(context.severity, ErrorSeverity.HIGH)
        self.assertEqual(context.category, ErrorCategory.DATABASE_ERROR)
        self.assertEqual(context.message, "Database connection failed")
        self.assertEqual(context.details, {"host": "localhost", "port": 5432})
        self.assertEqual(context.user_id, "user-456")
        self.assertEqual(context.request_id, "req-789")
        self.assertEqual(context.component, "database_service")


class TestEnums(unittest.TestCase):
    """Test cases for enum classes"""

    def test_error_severity_enum(self):
        """Test ErrorSeverity enum values."""
        self.assertEqual(ErrorSeverity.LOW.value, "low")
        self.assertEqual(ErrorSeverity.MEDIUM.value, "medium")
        self.assertEqual(ErrorSeverity.HIGH.value, "high")
        self.assertEqual(ErrorSeverity.CRITICAL.value, "critical")

    def test_error_category_enum(self):
        """Test ErrorCategory enum values."""
        self.assertEqual(ErrorCategory.VALIDATION.value, "validation")
        self.assertEqual(ErrorCategory.AUTHENTICATION.value, "authentication")
        self.assertEqual(ErrorCategory.AUTHORIZATION.value, "authorization")
        self.assertEqual(ErrorCategory.RESOURCE_NOT_FOUND.value, "resource_not_found")
        self.assertEqual(ErrorCategory.SERVICE_UNAVAILABLE.value, "service_unavailable")
        self.assertEqual(ErrorCategory.INTERNAL_SERVER_ERROR.value, "internal_server_error")


if __name__ == '__main__':
    unittest.main()
    unittest.main()
