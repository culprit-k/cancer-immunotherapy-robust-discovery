"""Tests for local checkpoint SHA-256 verification."""
import hashlib
import tempfile
import unittest
from pathlib import Path

from scripts.verify_virtues_checkpoint import verify


class VerifyVirTuesCheckpointTests(unittest.TestCase):
    def test_matching_hash_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "weights.bin"
            path.write_bytes(b"test checkpoint bytes")
            expected = hashlib.sha256(b"test checkpoint bytes").hexdigest()
            result = verify(path, expected)
            self.assertEqual(result["gate"], "PASS_PINNED_FILE_HASH")
            self.assertTrue(result["hash_matches"])

    def test_hash_mismatch_is_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "weights.bin"
            path.write_bytes(b"wrong bytes")
            result = verify(path, "0" * 64)
            self.assertEqual(result["gate"], "BLOCKED_HASH_MISMATCH")
            self.assertFalse(result["hash_matches"])

    def test_missing_file_is_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = verify(Path(tmp) / "not-found.safetensors")
            self.assertEqual(result["gate"], "BLOCKED_FILE_NOT_FOUND")


if __name__ == "__main__":
    unittest.main()
