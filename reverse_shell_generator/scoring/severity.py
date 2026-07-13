"""Scoring de severidad por tipo de shell."""

from dataclasses import dataclass


@dataclass
class SeverityResult:
    """Resultado de severidad de un shell."""
    language: str
    shell_type: str
    severity: str
    score: int
    description: str


SEVERITY_MAP: dict[str, dict[str, tuple[str, int, str]]] = {
    "reverse": {
        "powershell": ("Alto", 9, "Shell inverso PowerShell — ejecución en memoria sin archivos"),
        "java": ("Alto", 8, "Shell inverso Java — cross-platform"),
        "python": ("Medio", 7, "Shell inverso Python — requiere intérprete"),
        "php": ("Medio", 7, "Shell inverso PHP — común en web"),
        "c": ("Alto", 9, "Shell inverso C — binario compilado"),
        "bash": ("Medio", 6, "Shell inverso Bash — requiere /bin/sh"),
        "netcat": ("Medio", 6, "Shell inverso Netcat — requiere nc instalado"),
        "ruby": ("Bajo", 5, "Shell inverso Ruby — menos común"),
        "perl": ("Bajo", 5, "Shell inverso Perl — menos común"),
    },
    "bind": {
        "powershell": ("Alto", 8, "Bind shell PowerShell — listener en memoria"),
        "python": ("Medio", 6, "Bind shell Python — requiere intérprete"),
        "bash": ("Medio", 6, "Bind shell Bash — requiere nc"),
        "netcat": ("Medio", 6, "Bind shell Netcat — requiere nc instalado"),
    },
}


class ShellSeverity:
    """Calcula la severidad de un shell generado."""

    def get_severity(self, language: str, shell_type: str = "reverse") -> SeverityResult:
        language = language.lower()
        shell_type = shell_type.lower()
        types = SEVERITY_MAP.get(shell_type, {})
        severity, score, description = types.get(
            language, ("Bajo", 3, "Severidad por defecto")
        )
        return SeverityResult(
            language=language,
            shell_type=shell_type,
            severity=severity,
            score=score,
            description=description,
        )

    def get_summary(self, shells: list[dict[str, str]]) -> dict[str, int]:
        summary: dict[str, int] = {"Alto": 0, "Medio": 0, "Bajo": 0}
        for shell in shells:
            result = self.get_severity(shell["language"], shell.get("shell_type", "reverse"))
            summary[result.severity] = summary.get(result.severity, 0) + 1
        return summary

    def get_owasp_mapping(self) -> dict[str, str]:
        return {
            "A05:2021": "Misconfiguration de Seguridad — Shells sin ofuscación",
            "T1059": "MITRE — Ejecución de Comando",
            "T1059.004": "MITRE — Shell inverso Unix",
            "T1059.001": "MITRE — PowerShell",
        }
