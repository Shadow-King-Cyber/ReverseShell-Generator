"""Tests para el generador de reverse shells."""

from reverse_shell_generator.generators.reverse import ReverseShellGenerator


def test_generate_python():
    gen = ReverseShellGenerator()
    shell = gen.generate("python", "192.168.1.100", 4444)
    assert shell.language == "python"
    assert shell.lhost == "192.168.1.100"
    assert shell.port == 4444
    assert "socket" in shell.payload
    assert "192.168.1.100" in shell.payload


def test_generate_bash():
    gen = ReverseShellGenerator()
    shell = gen.generate("bash", "10.0.0.1", 8080)
    assert shell.language == "bash"
    assert "10.0.0.1" in shell.payload
    assert "8080" in shell.payload
    assert "/dev/tcp" in shell.payload


def test_generate_powershell():
    gen = ReverseShellGenerator()
    shell = gen.generate("powershell", "172.16.0.1", 9999)
    assert shell.language == "powershell"
    assert "172.16.0.1" in shell.payload
    assert "9999" in shell.payload


def test_generate_java():
    gen = ReverseShellGenerator()
    shell = gen.generate("java", "10.0.0.1", 4444)
    assert shell.language == "java"
    assert "10.0.0.1" in shell.payload
    assert "Socket" in shell.payload


def test_generate_php():
    gen = ReverseShellGenerator()
    shell = gen.generate("php", "10.0.0.1", 4444)
    assert shell.language == "php"
    assert "fsockopen" in shell.payload


def test_generate_c():
    gen = ReverseShellGenerator()
    shell = gen.generate("c", "10.0.0.1", 4444)
    assert shell.language == "c"
    assert "socket" in shell.payload


def test_generate_netcat():
    gen = ReverseShellGenerator()
    shell = gen.generate("netcat", "10.0.0.1", 4444)
    assert shell.language == "netcat"
    assert "nc" in shell.payload


def test_generate_ruby():
    gen = ReverseShellGenerator()
    shell = gen.generate("ruby", "10.0.0.1", 4444)
    assert shell.language == "ruby"
    assert "TCPSocket" in shell.payload


def test_generate_perl():
    gen = ReverseShellGenerator()
    shell = gen.generate("perl", "10.0.0.1", 4444)
    assert shell.language == "perl"
    assert "socket" in shell.payload


def test_unsupported_language():
    gen = ReverseShellGenerator()
    try:
        gen.generate("brainfuck", "10.0.0.1", 4444)
        assert False, "Debería haber lanzado ValueError"
    except ValueError as e:
        assert "no soportado" in str(e)


def test_list_languages():
    gen = ReverseShellGenerator()
    langs = gen.list_languages()
    assert "python" in langs
    assert "bash" in langs
    assert "powershell" in langs
    assert len(langs) == 9


def test_payload_formato_consistente():
    gen = ReverseShellGenerator()
    for lang in ["python", "bash", "netcat"]:
        shell = gen.generate(lang, "10.0.0.1", 4444)
        assert isinstance(shell.payload, str)
        assert len(shell.payload) > 0
