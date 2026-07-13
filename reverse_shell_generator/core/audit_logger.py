"""Auditoría de operaciones de shell."""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class AuditLogger:
    """Registra todas las operaciones de generación de shells."""

    def __init__(self, log_path: str | Path = "audit_log.jsonl") -> None:
        self._log_path = Path(log_path)

    def log(self, event_type: str, details: dict[str, Any]) -> None:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "details": details,
        }
        with open(self._log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def log_generation(self, shell_type: str, language: str, lhost: str, port: int) -> None:
        self.log("shell_generated", {
            "shell_type": shell_type,
            "language": language,
            "lhost": lhost,
            "port": port,
        })

    def log_encoding(self, encoding_type: str, original_size: int) -> None:
        self.log("payload_encoded", {
            "encoding_type": encoding_type,
            "original_size": original_size,
        })

    def read_all(self) -> list[dict[str, Any]]:
        if not self._log_path.exists():
            return []
        entries = []
        with open(self._log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    entries.append(json.loads(line))
        return entries

    def read_by_type(self, event_type: str) -> list[dict[str, Any]]:
        return [e for e in self.read_all() if e.get("event_type") == event_type]
