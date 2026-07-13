"""Tests para el auditor de operaciones."""

import tempfile
from pathlib import Path
from reverse_shell_generator.core.audit_logger import AuditLogger


def test_log_and_read():
    with tempfile.TemporaryDirectory() as tmp:
        log_path = Path(tmp) / "test.jsonl"
        logger = AuditLogger(log_path)
        logger.log_generation("reverse", "python", "10.0.0.1", 4444)
        entries = logger.read_all()
        assert len(entries) == 1
        assert entries[0]["event_type"] == "shell_generated"
        assert entries[0]["details"]["language"] == "python"


def test_read_by_type():
    with tempfile.TemporaryDirectory() as tmp:
        log_path = Path(tmp) / "test.jsonl"
        logger = AuditLogger(log_path)
        logger.log_generation("reverse", "python", "10.0.0.1", 4444)
        logger.log_encoding("base64", 100)
        shells = logger.read_by_type("shell_generated")
        assert len(shells) == 1
        encodings = logger.read_by_type("payload_encoded")
        assert len(encodings) == 1


def test_log_encoding():
    with tempfile.TemporaryDirectory() as tmp:
        log_path = Path(tmp) / "test.jsonl"
        logger = AuditLogger(log_path)
        logger.log_encoding("hex", 50)
        entries = logger.read_all()
        assert entries[0]["details"]["encoding_type"] == "hex"


def test_read_empty_log():
    with tempfile.TemporaryDirectory() as tmp:
        log_path = Path(tmp) / "empty.jsonl"
        logger = AuditLogger(log_path)
        assert logger.read_all() == []
