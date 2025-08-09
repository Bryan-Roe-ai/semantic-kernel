#!/usr/bin/env python3
"""Unified MemoryRecord implementation.

This file consolidated multiple corrupted/duplicated versions into a
single class. Goals:
* Preserve backward compatibility for existing imports/factory usage.
* Avoid hard dependency on numpy (embeddings typed as Any).
* Provide minimal helper factories (reference_record/local_record).

Public surface intentionally small; internal underscore attributes
retained because existing memory store connectors reference them.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

EmbeddingType = Any  # Flexible: list[float], numpy.ndarray, etc.

__all__ = ["MemoryRecord", "EmbeddingType"]


class MemoryRecord:
    """Represents a semantic memory entry.

    Parameters mirror historical variants; prefer using factories.
    """

    def __init__(
        self,
        *,
        record_id: Optional[str] = None,
        # Alternate legacy signature fields (if provided together)
        id: Optional[str] = None,  # noqa: A003 - legacy alias
        text: Optional[str] = None,
        description: Optional[str] = None,
        additional_metadata: Optional[str] = None,
        embedding: Optional[EmbeddingType] = None,
        is_reference: bool = False,
        external_source_name: Optional[str] = None,
        key: Optional[str] = None,
        timestamp: Optional[datetime] = None,
    ) -> None:
        # Choose id precedence: explicit record_id > legacy id
        chosen_id = record_id or id
        if chosen_id is None:
            raise ValueError("record_id (or id) must be provided")

        self._id = chosen_id
        self._text = text
        self._description = description
        self._additional_metadata = additional_metadata
        self._embedding = embedding
        self._is_reference = is_reference
        self._external_source_name = external_source_name
        self._key = key
        self._timestamp = timestamp

    # ---------- Factory helpers ---------- #
    @staticmethod
    def reference_record(
        external_id: str,
        source_name: str,
        description: Optional[str],
        additional_metadata: Optional[str],
        embedding: EmbeddingType,
    ) -> "MemoryRecord":
        return MemoryRecord(
            record_id=external_id,
            description=description,
            additional_metadata=additional_metadata,
            embedding=embedding,
            is_reference=True,
            external_source_name=source_name,
        )

    @staticmethod
    def local_record(
        record_id: str,
        text: str,
        description: Optional[str],
        additional_metadata: Optional[str],
        embedding: EmbeddingType,
        timestamp: Optional[datetime] = None,
    ) -> "MemoryRecord":
        return MemoryRecord(
            record_id=record_id,
            text=text,
            description=description,
            additional_metadata=additional_metadata,
            embedding=embedding,
            timestamp=timestamp,
            is_reference=False,
        )

    # ---------- Properties ---------- #
    @property
    def id(self) -> str:  # noqa: D401
        return self._id

    @property
    def text(self) -> Optional[str]:  # noqa: D401
        return self._text

    @property
    def description(self) -> Optional[str]:  # noqa: D401
        return self._description

    @property
    def additional_metadata(self) -> Optional[str]:  # noqa: D401
        return self._additional_metadata

    @property
    def embedding(self) -> Optional[EmbeddingType]:  # noqa: D401
        return self._embedding

    @property
    def timestamp(self) -> Optional[datetime]:  # noqa: D401
        return self._timestamp

    # ---------- Convenience ---------- #
    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self._id,
            "text": self._text,
            "description": self._description,
            "additional_metadata": self._additional_metadata,
            "is_reference": self._is_reference,
            "external_source_name": self._external_source_name,
            "timestamp": (self._timestamp.isoformat() if self._timestamp else None),
        }

    def update_embedding(self, embedding: EmbeddingType) -> None:
        self._embedding = embedding

    def __repr__(self) -> str:  # pragma: no cover
        return (
            "MemoryRecord("  # noqa: E501
            f"id={self._id!r}, text={self._text!r}, "
            f"is_reference={self._is_reference}, "
            f"source={self._external_source_name!r})"
        )
