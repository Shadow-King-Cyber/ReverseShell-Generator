"""Tests para scoring de severidad."""

from reverse_shell_generator.scoring.severity import ShellSeverity


def test_python_reverse_severity():
    sev = ShellSeverity()
    result = sev.get_severity("python", "reverse")
    assert result.severity == "Medio"
    assert result.score == 7
    assert result.language == "python"


def test_powershell_reverse_severity():
    sev = ShellSeverity()
    result = sev.get_severity("powershell", "reverse")
    assert result.severity == "Alto"
    assert result.score == 9


def test_c_reverse_severity():
    sev = ShellSeverity()
    result = sev.get_severity("c", "reverse")
    assert result.severity == "Alto"
    assert result.score == 9


def test_python_bind_severity():
    sev = ShellSeverity()
    result = sev.get_severity("python", "bind")
    assert result.severity == "Medio"
    assert result.score == 6


def test_unknown_severity():
    sev = ShellSeverity()
    result = sev.get_severity("brainfuck", "reverse")
    assert result.severity == "Bajo"
    assert result.score == 3


def test_get_summary():
    sev = ShellSeverity()
    shells = [
        {"language": "python", "shell_type": "reverse"},
        {"language": "powershell", "shell_type": "reverse"},
        {"language": "bash", "shell_type": "reverse"},
    ]
    summary = sev.get_summary(shells)
    assert summary["Alto"] == 1
    assert summary["Medio"] == 2


def test_owasp_mapping():
    sev = ShellSeverity()
    mapping = sev.get_owasp_mapping()
    assert "A05:2021" in mapping
    assert "T1059" in mapping
