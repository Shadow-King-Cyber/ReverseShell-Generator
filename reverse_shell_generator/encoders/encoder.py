"""Codificación y ofuscación de payloads."""

import base64
import codecs
from dataclasses import dataclass


@dataclass
class EncodedPayload:
    """Payload codificado con metadatos."""
    original: str
    encoded: str
    encoding_type: str
    original_size: int
    encoded_size: int


class PayloadEncoder:
    """Codifica payloads en varios formatos."""

    def encode(self, payload: str, encoding_type: str) -> EncodedPayload:
        encoding_type = encoding_type.lower()
        original_size = len(payload)

        encoder = getattr(self, f"_encode_{encoding_type}", None)
        if not encoder:
            raise ValueError(
                f"Codificación no soportada: {encoding_type}. "
                f"Soportadas: base64, hex, rot13, xor"
            )

        encoded = encoder(payload)
        return EncodedPayload(
            original=payload,
            encoded=encoded,
            encoding_type=encoding_type,
            original_size=original_size,
            encoded_size=len(encoded),
        )

    def _encode_base64(self, payload: str) -> str:
        return base64.b64encode(payload.encode("utf-8")).decode("ascii")

    def _encode_hex(self, payload: str) -> str:
        return payload.encode("utf-8").hex()

    def _encode_rot13(self, payload: str) -> str:
        return codecs.encode(payload, "rot_13")

    def _encode_xor(self, payload: str, key: int = 42) -> str:
        return "".join(chr(ord(c) ^ key) for c in payload)

    def list_encodings(self) -> list[str]:
        return ["base64", "hex", "rot13", "xor"]
