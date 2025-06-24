#!/usr/bin/env python3
"""
Entra Id Authentication module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

import logging

from azure.core.exceptions import ClientAuthenticationError
from azure.identity import DefaultAzureCredential

from semantic_kernel.exceptions.service_exceptions import ServiceInvalidAuthError

logger: logging.Logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)

logging.basicConfig(level=logging.DEBUG)

def get_entra_auth_token(token_endpoint: str) -> str | None:
    """Retrieve a Microsoft Entra Auth Token for a given token endpoint.

    The token endpoint may be specified as an environment variable, via the .env
    file or as an argument. If the token endpoint is not provided, the default is None.

    Args:
        token_endpoint: The token endpoint to use to retrieve the authentication token.

    Returns:
        The Azure token or None if the token could not be retrieved.
    """
    if not token_endpoint:
        raise ServiceInvalidAuthError(
            "A token endpoint must be provided either in settings, as an environment variable, or as an argument."
        )

    credential = DefaultAzureCredential()

    try:
        auth_token = credential.get_token(token_endpoint)
    except ClientAuthenticationError:
        logger.error(f"Failed to retrieve Azure token for the specified endpoint: `{token_endpoint}`.")
        return None

    logger.info(f"Successfully retrieved Azure token for the specified endpoint: `{token_endpoint}`.")

    logger.info(f"Successfully retrieved Azure token for the specified endpoint: `{token_endpoint}`.")

    return auth_token.token if auth_token else None
