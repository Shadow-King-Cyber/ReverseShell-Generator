"""Configuración global del generador."""

from pathlib import Path


class Config:
    """Configuración centralizada."""

    BASE_DIR = Path(__file__).resolve().parent.parent
    SCOPE_FILE = BASE_DIR / "scope.json"
    AUDIT_LOG = BASE_DIR / "audit_log.jsonl"
    REPORTS_DIR = BASE_DIR / "reports"

    DEFAULT_LHOST = "10.0.0.1"
    DEFAULT_PORT = 4444

    SUPPORTED_LANGUAGES = [
        "python", "bash", "powershell", "java", "php", "c", "netcat", "ruby", "perl"
    ]

    SUPPORTED_ENCODINGS = ["base64", "hex", "rot13", "xor"]

    OWASP_MAPPING = {
        "reverse": "A05:2021 — Misconfiguration de Seguridad",
        "bind": "A05:2021 — Misconfiguration de Seguridad",
    }
