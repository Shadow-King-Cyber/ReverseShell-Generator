"""Tests para el constructor de reportes."""

from reverse_shell_generator.reporting.report_builder import ReportBuilder, ReportData


def test_build_summary_empty():
    builder = ReportBuilder()
    result = builder.build_summary([])
    assert result["total"] == 0
    assert result["languages"] == []


def test_build_summary_with_entries():
    builder = ReportBuilder()
    entries = [
        {"language": "python", "severity": "Medio"},
        {"language": "powershell", "severity": "Alto"},
    ]
    result = builder.build_summary(entries)
    assert result["total"] == 2
    assert "python" in result["languages"]
    assert "powershell" in result["languages"]
    assert result["severity_summary"]["Alto"] == 1
    assert result["severity_summary"]["Medio"] == 1


def test_build_report():
    builder = ReportBuilder()
    data = ReportData(
        shells_generated=2,
        languages_used=["python", "bash"],
        encoding_used=None,
        severity_summary={"Alto": 0, "Medio": 2, "Bajo": 0},
        owasp_mapping={"A05:2021": "Test"},
        entries=[],
    )
    report = builder.build_report(data)
    assert report["tool"] == "ReverseShell-Generator"
    assert report["version"] == "1.0.0"
    assert report["summary"]["shells_generated"] == 2
    assert "python" in report["summary"]["languages_used"]


def test_build_summary_encoding():
    builder = ReportBuilder()
    entries = [
        {"language": "python", "severity": "Medio", "encoding_used": "base64"},
    ]
    result = builder.build_summary(entries)
    assert result["encoding_used"] == "base64"
