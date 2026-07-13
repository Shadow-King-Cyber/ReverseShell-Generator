"""Tests para el generador de bind shells."""

from reverse_shell_generator.generators.bind import BindShellGenerator


def test_generate_bash():
    gen = BindShellGenerator()
    shell = gen.generate("bash", 4444)
    assert shell.language == "bash"
    assert shell.port == 4444
    assert "nc" in shell.payload


def test_generate_python():
    gen = BindShellGenerator()
    shell = gen.generate("python", 8080)
    assert shell.language == "python"
    assert "8080" in shell.payload
    assert "listen" in shell.payload


def test_generate_powershell():
    gen = BindShellGenerator()
    shell = gen.generate("powershell", 9999)
    assert shell.language == "powershell"
    assert "9999" in shell.payload
    assert "TcpListener" in shell.payload


def test_generate_netcat():
    gen = BindShellGenerator()
    shell = gen.generate("netcat", 4444)
    assert shell.language == "netcat"
    assert "nc" in shell.payload


def test_unsupported_bind_language():
    gen = BindShellGenerator()
    try:
        gen.generate("go", 4444)
        assert False, "Debería haber lanzado ValueError"
    except ValueError as e:
        assert "no soportado" in str(e)


def test_list_bind_languages():
    gen = BindShellGenerator()
    langs = gen.list_languages()
    assert "bash" in langs
    assert "python" in langs
    assert len(langs) == 4
