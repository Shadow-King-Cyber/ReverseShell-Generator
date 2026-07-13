# ReverseShell-Generator

Generador de shells para investigación de seguridad ofensiva autorizada.

> **ADVERTENCIA**: Solo para laboratorios y entornos autorizados. El uso no autorizado es ilegal.

## Características

- **Genera reverse shells**: Python, Bash, PowerShell, Java, PHP, C, Netcat, Ruby, Perl
- **Genera bind shells**: Bash, Python, PowerShell, Netcat
- **Codifica payloads**: Base64, Hex, ROT13, XOR
- **Scoring de severidad** por lenguaje y tipo de shell
- **Mapeo OWASP** por tipo de shell
- **Reportes JSON + HTML** con visualizaciones
- **CLI Click** con generación interactiva
- **Scope authorization** — requiere alcance autorizado para generar

## Aviso Legal

Esta herramienta se proporciona únicamente con fines educativos y para pruebas de seguridad autorizadas. El usuario asume toda la responsabilidad de garantizar que cuenta con la autorización adecuada.

**Al usar este software, aceptas que:**
- Solo lo usarás en entornos controlados y autorizados (CTF, laboratorios)
- No usarás los payloads generados contra sistemas ajenos sin autorización
- Los autores no asumen responsabilidad por uso indebido

Leyes aplicables (incluyendo pero no limitándose a):
- **Panamá**: Ley 51 de 2012 — Delitos Informáticos
- **USA**: Computer Fraud and Abuse Act (CFAA)
- **UE**: Directive on Attacks against Information Systems (2013/40/EU)

## Requisitos

- Python 3.11+

```bash
git clone https://github.com/Shadow-King-Cyber/ReverseShell-Generator.git
cd ReverseShell-Generator
pip install -r requirements.txt
```

## Inicio Rápido

```bash
# 1. Configurar alcance autorizado
cp scope.example.json scope.json
# Editar scope.json con authorized: true

# 2. Listar shells disponibles
reverse-shell list

# 3. Generar reverse shell Python
reverse-shell generate python --lhost 10.0.0.1 --port 4444

# 4. Generar y codificar en Base64
reverse-shell generate python --lhost 10.0.0.1 --port 4444 --encode base64

# 5. Generar reporte
reverse-shell report
```

## Comandos del CLI

```bash
# Listar shells disponibles
reverse-shell list

# Generar reverse shell
reverse-shell generate python --lhost 10.0.0.1 --port 4444
reverse-shell generate bash --lhost 10.0.0.1 --port 4444
reverse-shell generate powershell --lhost 10.0.0.1 --port 4444

# Generar bind shell
reverse-shell bind bash --port 4444
reverse-shell bind python --port 4444

# Codificar payload
reverse-shell generate python --lhost 10.0.0.1 --port 4444 --encode base64
reverse-shell generate python --lhost 10.0.0.1 --port 4444 --encode hex

# Guardar en archivo
reverse-shell generate python --lhost 10.0.0.1 --port 4444 --output shell.py

# Ver mapping OWASP/MITRE
reverse-shell mapping

# Generar reporte
reverse-shell report
```

## Estructura del Proyecto

```
ReverseShell-Generator/
├── reverse_shell_generator/
│   ├── core/           # ScopeManager, AuditLogger
│   ├── generators/     # ReverseShellGenerator, BindShellGenerator
│   ├── encoders/       # PayloadEncoder (Base64, Hex, ROT13, XOR)
│   ├── scoring/        # ShellSeverity con mapeo OWASP
│   ├── reporting/      # Reportes JSON/HTML
│   └── ui/             # CLI Click
├── tests/              # Suite de tests con pytest
├── requirements.txt    # Dependencias de Python
├── pyproject.toml      # Configuración del proyecto
└── LICENSE             # Licencia MIT
```

## Ejecutar Tests

```bash
pytest -v
```

## Licencia

MIT License — ver [LICENSE](LICENSE)
