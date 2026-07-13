"""CLI principal para ReverseShell-Generator."""

from pathlib import Path

import click

from ..core.scope import ScopeManager
from ..core.audit_logger import AuditLogger
from ..generators.reverse import ReverseShellGenerator
from ..generators.bind import BindShellGenerator
from ..encoders.encoder import PayloadEncoder
from ..scoring.severity import ShellSeverity
from ..reporting.report_builder import ReportBuilder, ReportData
from ..reporting.json_exporter import JsonExporter
from ..reporting.html_exporter import HtmlExporter


@click.group()
@click.version_option(version="1.0.0", prog_name="reverse-shell")
def main() -> None:
    """ReverseShell-Generator — Generador de shells para investigación autorizada."""
    pass


@main.command()
def list() -> None:
    """Lista lenguajes soportados para reverse y bind shells."""
    reverse = ReverseShellGenerator()
    bind = BindShellGenerator()
    click.echo("=== Reverse Shells ===")
    for lang in reverse.list_languages():
        click.echo(f"  - {lang}")
    click.echo("\n=== Bind Shells ===")
    for lang in bind.list_languages():
        click.echo(f"  - {lang}")


@main.command()
@click.argument("language")
@click.option("--lhost", default="10.0.0.1", help="IP del listener")
@click.option("--port", default=4444, type=int, help="Puerto del listener")
@click.option("--encode", default=None, type=click.Choice(["base64", "hex", "rot13", "xor"]), help="Codificar payload")
@click.option("--output", default=None, help="Guardar payload en archivo")
@click.option("--scope", default="scope.json", help="Ruta al archivo scope.json")
def generate(language: str, lhost: str, port: int, encode: str | None, output: str | None, scope: str) -> None:
    """Genera un reverse shell para el lenguaje indicado."""
    scope_mgr = ScopeManager(scope)
    scope_mgr.require_authorization()

    gen = ReverseShellGenerator()
    shell = gen.generate(language, lhost, port)

    payload = shell.payload
    if encode:
        enc = PayloadEncoder()
        result = enc.encode(payload, encode)
        payload = result.encoded
        click.echo(f"Codificación: {encode} ({result.original_size} → {result.encoded_size} bytes)")

    click.echo(f"\n=== {language.upper()} Reverse Shell ({lhost}:{port}) ===\n")
    click.echo(payload)

    if output:
        Path(output).write_text(payload, encoding="utf-8")
        click.echo(f"\nGuardado en: {output}")

    logger = AuditLogger()
    logger.log_generation("reverse", language, lhost, port)


@main.command()
@click.argument("language")
@click.option("--port", default=4444, type=int, help="Puerto de escucha")
@click.option("--encode", default=None, type=click.Choice(["base64", "hex", "rot13", "xor"]), help="Codificar payload")
@click.option("--output", default=None, help="Guardar payload en archivo")
@click.option("--scope", default="scope.json", help="Ruta al archivo scope.json")
def bind(language: str, port: int, encode: str | None, output: str | None, scope: str) -> None:
    """Genera un bind shell para el lenguaje indicado."""
    scope_mgr = ScopeManager(scope)
    scope_mgr.require_authorization()

    gen = BindShellGenerator()
    shell = gen.generate(language, port)

    payload = shell.payload
    if encode:
        enc = PayloadEncoder()
        result = enc.encode(payload, encode)
        payload = result.encoded
        click.echo(f"Codificación: {encode} ({result.original_size} → {result.encoded_size} bytes)")

    click.echo(f"\n=== {language.upper()} Bind Shell (:{port}) ===\n")
    click.echo(payload)

    if output:
        Path(output).write_text(payload, encoding="utf-8")
        click.echo(f"\nGuardado en: {output}")

    logger = AuditLogger()
    logger.log_generation("bind", language, "0.0.0.0", port)


@main.command()
def mapping() -> None:
    """Muestra el mapping OWASP/MITRE para shells."""
    sev = ShellSeverity()
    mappings = sev.get_owasp_mapping()
    click.echo("=== Mapping OWASP / MITRE ===\n")
    for k, v in mappings.items():
        click.echo(f"  {k}: {v}")


@main.command()
def report() -> None:
    """Genera un reporte HTML + JSON de la actividad."""
    logger = AuditLogger()
    entries = logger.read_by_type("shell_generated")
    builder = ReportBuilder()
    summary = builder.build_summary(entries)

    data = ReportData(
        shells_generated=summary["total"],
        languages_used=summary["languages"],
        encoding_used=summary["encoding_used"],
        severity_summary=summary["severity_summary"],
        owasp_mapping=summary["owasp_mapping"],
        entries=entries,
    )
    report_data = builder.build_report(data)

    json_exp = JsonExporter()
    json_path = json_exp.export(report_data)
    click.echo(f"Reporte JSON: {json_path}")

    html_exp = HtmlExporter()
    html_path = html_exp.export(report_data)
    click.echo(f"Reporte HTML: {html_path}")


if __name__ == "__main__":
    main()
