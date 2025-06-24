#!/usr/bin/env python3
"""
Mongodb Atlas Settings module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from typing import ClassVar

from pydantic import SecretStr

from semantic_kernel.connectors.memory.mongodb_atlas.utils import (
    DEFAULT_DB_NAME,
    DEFAULT_SEARCH_INDEX_NAME,
)
from semantic_kernel.connectors.memory.mongodb_atlas.const import DEFAULT_DB_NAME, DEFAULT_SEARCH_INDEX_NAME
from semantic_kernel.kernel_pydantic import KernelBaseSettings
from semantic_kernel.utils.feature_stage_decorator import experimental


@experimental
class MongoDBAtlasSettings(KernelBaseSettings):
    """MongoDB Atlas model settings.

    Args:
    - connection_string: str - MongoDB Atlas connection string
        (Env var MONGODB_ATLAS_CONNECTION_STRING)
    - database_name: str - MongoDB Atlas database name, defaults to 'default'
        (Env var MONGODB_ATLAS_DATABASE_NAME)
    - index_name: str - MongoDB Atlas search index name, defaults to 'default'
        (Env var MONGODB_ATLAS_INDEX_NAME)
    """

    env_prefix: ClassVar[str] = "MONGODB_ATLAS_"

    connection_string: SecretStr
    database_name: str = DEFAULT_DB_NAME
    index_name: str = DEFAULT_SEARCH_INDEX_NAME
