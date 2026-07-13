"""Tests para el gestor de scope."""

import tempfile
import json
from pathlib import Path
from reverse_shell_generator.core.scope import ScopeManager


def test_default_scope_not_authorized():
    with tempfile.TemporaryDirectory() as tmp:
        scope = ScopeManager(Path(tmp) / "scope.json")
        assert not scope.is_authorized()


def test_set_authorized():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "scope.json"
        scope = ScopeManager(path)
        scope.set_authorized(True)
        scope.save()
        scope2 = ScopeManager(path)
        assert scope2.is_authorized()


def test_set_targets():
    with tempfile.TemporaryDirectory() as tmp:
        scope = ScopeManager(Path(tmp) / "scope.json")
        scope.set_targets(["192.168.1.0/24", "10.0.0.0/8"])
        assert scope.get_targets() == ["192.168.1.0/24", "10.0.0.0/8"]


def test_require_authorization_raises():
    with tempfile.TemporaryDirectory() as tmp:
        scope = ScopeManager(Path(tmp) / "scope.json")
        try:
            scope.require_authorization()
            assert False, "Debería haber lanzado PermissionError"
        except PermissionError:
            pass


def test_require_authorization_ok():
    with tempfile.TemporaryDirectory() as tmp:
        scope = ScopeManager(Path(tmp) / "scope.json")
        scope.set_authorized(True)
        scope.require_authorization()


def test_purpose_and_operator():
    with tempfile.TemporaryDirectory() as tmp:
        scope = ScopeManager(Path(tmp) / "scope.json")
        scope.set_purpose("pentest autorizado")
        scope.set_operator("equipo rojo")
        assert scope.get_purpose() == "pentest autorizado"
        assert scope.get_operator() == "equipo rojo"
