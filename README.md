# ReverseShell-Generator

Generador de shells para investigación de seguridad ofensiva autorizada.

> **ADVERTENCIA**: Solo para laboratorios y entornos autorizados. El uso no autorizado es ilegal.

## Características

- **Genera reverse shells**: Python, Bash, PowerShell, Java, PHP, C, Netcat, Ruby, Perl
- **Genera bind shells**: Bash, Python, PowerShell, Netcat
- **Codifica payloads**: Base64, Hex, ROT13, XOR
- **CLI Click** con generación interactiva
- **Mapeo OWASP** por tipo de shell
- **Scoring de severidad** por lenguaje
- **Reportes JSON + HTML** con Chart.js

## Instalación

```bash
git clone https://github.com/Shadow-King-Cyber/ReverseShell-Generator.git
cd ReverseShell-Generator
pip install -r requirements.txt
```

## Uso

```bash
# Listar shells disponibles
reverse-shell list

# Generar reverse shell Python
reverse-shell generate python --lhost 10.0.0.1 --port 4444

# Generar bind shell Bash
reverse-shell bind bash --port 4444

# Generar y codificar en Base64
reverse-shell generate python --lhost 10.0.0.1 --port 4444 --encode base64

# Ver mapping OWASP
reverse-shell mapping

# Generar reporte
reverse-shell report
```

## Licencia

MIT License — Shadow-King-Cyber
