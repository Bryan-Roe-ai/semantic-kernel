#!/usr/bin/env python3
"""Persistent Memory Store using pickle for storage.

SECURITY NOTE:
    ``pickle`` deserialization can execute arbitrary code if the file is
    tampered with. This implementation adds several defense-in-depth
    measures (permission checks, integrity hashing, optional environment
    variable toggle) but MUST NOT be used with untrusted files. For
    untrusted data, implement a JSON / msgpack based store instead.
    Set SK_DISABLE_PICKLE_PERSISTENCE=1 to disable loading existing pickle
    files (the store will start empty) and only allow writing a new one.
"""

import os
import pickle
import logging
import hashlib
from typing import List


from semantic_kernel.memory.memory_record import MemoryRecord
from semantic_kernel.memory.volatile_memory_store import VolatileMemoryStore

logger: logging.Logger = logging.getLogger(__name__)


class PersistentMemoryStore(VolatileMemoryStore):
    """A memory store that persists data to disk."""

    def __init__(self, file_path: str = "semantic_memory.pkl") -> None:
        super().__init__()
        self._file_path = file_path
        self._hash_path = f"{self._file_path}.sha256"
        # Ensure dirty flag exists early for linters/static analysis
        self._dirty = False
        if os.path.exists(self._file_path):
            self._store = self._safe_load()
        else:
            self._store = {}

    # ------------------------- Internal helpers ------------------------- #
    def _file_is_safe(self) -> bool:
        """Basic safety checks: file ownership & permissions.

        Returns False if the file is group/world writable to reduce risk of
        malicious overwrite (TOCTOU still possible, but harder).
        """
        try:
            st = os.stat(self._file_path)
            # If group or others have write permission, treat as unsafe
            if st.st_mode & 0o022:  # group (0o020) or others (0o002) write
                logger.warning(
                    (
                        "Refusing to unpickle '%s' because it is "
                        "group/world writable."
                    ),
                    self._file_path,
                )
                return False
            # Only allow if owned by current user (when applicable)
            if (
                hasattr(st, "st_uid") and st.st_uid != os.getuid()
            ):  # pragma: no cover - platform specific
                logger.warning(
                    ("Refusing to unpickle '%s' (owner uid %s != " "process uid %s)."),
                    self._file_path,
                    st.st_uid,
                    os.getuid(),
                )
                return False
        except OSError as exc:  # pragma: no cover - rare error path
            logger.warning(
                "Could not stat pickle file '%s': %s",
                self._file_path,
                exc,
            )
            return False
        return True

    def _verify_hash(self, data: bytes) -> bool:
        if not os.path.exists(self._hash_path):
            logger.debug(
                "No stored hash for %s – skipping verification.",
                self._file_path,
            )
            return True
        try:
            with open(self._hash_path, "rt", encoding="utf-8") as hf:
                expected = hf.read().strip()
            actual = hashlib.sha256(data).hexdigest()
            if expected != actual:
                logger.warning(
                    (
                        "Integrity hash mismatch for '%s'. Expected %s "
                        "got %s. "
                        "Ignoring stored data."
                    ),
                    self._file_path,
                    expected,
                    actual,
                )
                return False
            return True
        except (
            OSError,
            IOError,
            ValueError,
        ) as exc:  # pragma: no cover - corruption case
            logger.warning(
                "Failed to verify hash for %s: %s",
                self._file_path,
                exc,
            )
            return False

    def _safe_load(self):
        if os.environ.get("SK_DISABLE_PICKLE_PERSISTENCE") == "1":
            logger.info(
                (
                    "SK_DISABLE_PICKLE_PERSISTENCE set – skipping load "
                    "of '%s' "
                    "(starting empty store)"
                ),
                self._file_path,
            )
            return {}
        if not self._file_is_safe():
            return {}
        try:
            with open(self._file_path, "rb") as f:
                raw = f.read()
            if not self._verify_hash(raw):
                return {}
            # Perform actual unpickle only after integrity & permission checks
            return pickle.loads(raw)
        except (
            pickle.PickleError,
            FileNotFoundError,
            EOFError,
            OSError,
        ) as exc:  # pragma: no cover - corruption case
            logger.warning(
                "Failed to load memory store due to %s: %s",
                type(exc).__name__,
                exc,
            )
        except (
            ValueError,
            AttributeError,
            TypeError,
        ) as exc:  # pragma: no cover - unexpected
            logger.warning(
                "Unexpected error loading pickle: %s",
                exc,
            )
        return {}

    def _persist(self) -> None:
        """Write the current store to disk if modified.

        Also writes a SHA256 hash alongside the pickle to allow basic integrity
        verification on subsequent loads.
        """
        if self._dirty:
            data: bytes
            try:
                data = pickle.dumps(self._store, protocol=pickle.HIGHEST_PROTOCOL)
                with open(self._file_path, "wb") as f:
                    f.write(data)
                with open(self._hash_path, "wt", encoding="utf-8") as hf:
                    hf.write(hashlib.sha256(data).hexdigest())
                self._dirty = False  # Reset the dirty flag after persisting
            except (
                pickle.PickleError,
                OSError,
                IOError,
            ) as exc:  # pragma: no cover - IO failure
                logger.error(
                    "Failed to persist memory store '%s': %s",
                    self._file_path,
                    exc,
                )

    async def create_collection(self, collection_name: str) -> None:  # noqa: D401
        await super().create_collection(collection_name)
        self._dirty = True  # Mark the store as modified

    async def delete_collection(self, collection_name: str) -> None:  # noqa: D401
        await super().delete_collection(collection_name)
        self._dirty = True  # Mark the store as modified

    async def upsert(
        self, collection_name: str, record: MemoryRecord
    ) -> str:  # noqa: D401
        key = await super().upsert(collection_name, record)
        self._dirty = True  # Mark the store as modified
        return key

    async def upsert_batch(
        self, collection_name: str, records: List[MemoryRecord]
    ) -> List[str]:  # noqa: D401
        keys = await super().upsert_batch(collection_name, records)
        self._dirty = True  # Mark the store as modified
        return keys

    async def remove(self, collection_name: str, key: str) -> None:  # noqa: D401
        await super().remove(collection_name, key)
        self._dirty = True  # Mark the store as modified

    async def remove_batch(
        self, collection_name: str, keys: List[str]
    ) -> None:  # noqa: D401
        await super().remove_batch(collection_name, keys)
        self._dirty = True  # Mark the store as modified

    async def close(self) -> None:  # noqa: D401
        if self._dirty:
            self._persist()  # Ensure changes are saved before closing
