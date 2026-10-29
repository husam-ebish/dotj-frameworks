"""Bounded-buffer hashes for oracle inputs; every invocation reads the full file."""

import hashlib
from pathlib import Path


_SHA256_BUFFER_BYTES = 256 * 1024


def sha256_file(path):
    """Return the SHA-256 hex digest; propagate open/read errors without caching."""
    digest = hashlib.sha256()
    buffer = bytearray(_SHA256_BUFFER_BYTES)
    view = memoryview(buffer)
    with Path(path).open("rb", buffering=0) as stream:
        while True:
            count = stream.readinto(buffer)
            if count == 0:
                break
            digest.update(view[:count])
    return digest.hexdigest()
