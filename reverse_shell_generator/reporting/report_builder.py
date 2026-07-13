"""Constructor de reportes consolidados."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class ReportData:
    """Datos para generar un reporte."""
    shells_generated: int
    languages_used: list[str]
    encoding_used: str | None
    severity_summary: dict[str, int]
    owasp_mapping: dict[str, str]
    entries: list[dict[str, Any]] = field(default_factory=list)


class ReportBuilder:
    """Construye reportes consolidados de actividad."""

    def build_summary(self, entries: list[dict[str, Any]]) -> dict[str, Any]:
        if not entries:
            return {
                "total": 0,
                "languages": [],
                "encoding_used": None,
                "severity_summary": {},
                "owasp_mapping": {},
            }

        languages = list({e.get("language", "") for e in entries if e.get("language")})
        encoding = None
        for e in entries:
            if e.get("encoding_used"):
                encoding = e["encoding_used"]
                break

        severity: dict[str, int] = {"Alto": 0, "Medio": 0, "Bajo": 0}
        for e in entries:
            sev = e.get("severity", "Bajo")
            severity[sev] = severity.get(sev, 0) + 1

        return {
            "total": len(entries),
            "languages": languages,
            "encoding_used": encoding,
            "severity_summary": severity,
            "owasp_mapping": {
                "A05:2021": "Misconfiguration de Seguridad",
                "T1059": "Ejecución de Comando",
            },
        }

    def build_report(self, data: ReportData) -> dict[str, Any]:
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tool": "ReverseShell-Generator",
            "version": "1.0.0",
            "summary": {
                "shells_generated": data.shells_generated,
                "languages_used": data.languages_used,
                "encoding_used": data.encoding_used,
                "severity_summary": data.severity_summary,
            },
            "owasp_mapping": data.owasp_mapping,
            "entries": data.entries,
        }
