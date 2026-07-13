"""Tests para el codificador de payloads."""

import base64
import codecs
from reverse_shell_generator.encoders.encoder import PayloadEncoder


def test_encode_base64():
    enc = PayloadEncoder()
    result = enc.encode("whoami", "base64")
    assert result.encoding_type == "base64"
    assert result.encoded == base64.b64encode(b"whoami").decode()
    assert result.original_size == 6
    assert result.encoded_size > 0


def test_encode_hex():
    enc = PayloadEncoder()
    result = enc.encode("test", "hex")
    assert result.encoding_type == "hex"
    assert result.encoded == "74657374"


def test_encode_rot13():
    enc = PayloadEncoder()
    result = enc.encode("hello", "rot13")
    assert result.encoding_type == "rot13"
    assert result.encoded == codecs.encode("hello", "rot_13")


def test_encode_xor():
    enc = PayloadEncoder()
    result = enc.encode("test", "xor")
    assert result.encoding_type == "xor"
    assert result.encoded_size == 4


def test_unsupported_encoding():
    enc = PayloadEncoder()
    try:
        enc.encode("test", "lzma")
        assert False, "Debería haber lanzado ValueError"
    except ValueError as e:
        assert "no soportada" in str(e)


def test_list_encodings():
    enc = PayloadEncoder()
    encodings = enc.list_encodings()
    assert "base64" in encodings
    assert "hex" in encodings
    assert "rot13" in encodings
    assert "xor" in encodings
    assert len(encodings) == 4
