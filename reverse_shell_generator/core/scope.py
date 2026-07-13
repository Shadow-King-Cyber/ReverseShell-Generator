"""Gestión de scope para autorización de uso."""

import json
from pathlib import Path
from typing import Any


class ScopeManager:
    """Gestiona el alcance autorizado de la herramienta."""

    def __init__(self, scope_path: str | Path = "scope.json") -> None:
        self._scope_path = Path(scope_path)
        self._scope = self._load_scope()

    def _load_scope(self) -> dict[str, Any]:
        if self._scope_path.exists():
            return json.loads(self._scope_path.read_text(encoding="utf-8"))
        return {"authorized": False, "targets": [], "purpose": "", "operator": ""}

    def save(self) -> None:
        self._scope_path.write_text(
            json.dumps(self._scope, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    def is_authorized(self) -> bool:
        return self._scope.get("authorized", False)

    def get_targets(self) -> list[str]:
        return self._scope.get("targets", [])

    def get_purpose(self) -> str:
        return self._scope.get("purpose", "")

    def get_operator(self) -> str:
        return self._scope.get("operator", "")

    def set_authorized(self, authorized: bool) -> None:
        self._scope["authorized"] = authorized

    def set_targets(self, targets: list[str]) -> None:
        self._scope["targets"] = targets

    def set_purpose(self, purpose: str) -> None:
        self._scope["purpose"] = purpose

    def set_operator(self, operator: str) -> None:
        self._scope["operator"] = operator

    def require_authorization(self) -> None:
        if not self.is_authorized():
            raise PermissionError(
                "Operación no autorizada. Configure scope.json con authorized: true"
            )
