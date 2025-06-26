#!/usr/bin/env python3
"""
import asyncio
import re
Volatile Data Store module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from datetime import datetime
from typing import Dict, List, Optional

from semantic_kernel.memory.memory_record import MemoryRecord
from semantic_kernel.memory.storage.data_entry import DataEntry
from semantic_kernel.memory.storage.data_store_base import DataStoreBase


class VolatileDataStore(DataStoreBase):
    _store: Dict[str, Dict[str, DataEntry]]

    def __init__(self) -> None:
        self._store = {}

    async def get_collections_async(self) -> List[str]:
        return list(self._store.keys())

    async def get_all_async(self, collection: str) -> List[DataEntry]:
        if collection not in self._store:
            return []

        return list(self._store[collection].values())

    async def get_async(self, collection: str, key: str) -> Optional[DataEntry]:
        if collection not in self._store:
            return None
        if key not in self._store[collection]:
            return None

        return self._store[collection][key]

    async def put_async(self, collection: str, value: DataEntry) -> DataEntry:
        if collection not in self._store:
            self._store[collection] = {}

        self._store[collection][value.key] = value

        return value

    async def remove_async(self, collection: str, key: str) -> None:
        if collection not in self._store:
            return
        if key not in self._store[collection]:
            return

        del self._store[collection][key]

    async def get_value_async(self, collection: str, key: str) -> MemoryRecord:
        entry = await self.get_async(collection, key)

        if entry is None:
            # TODO: equivalent here?
            raise Exception(f"Key '{key}' not found in collection '{collection}'")

        return entry.value

    async def put_value_async(
        self, collection: str, key: str, value: MemoryRecord
    ) -> None:
        await self.put_async(collection, DataEntry(key, value, datetime.now()))
