import struct
import zlib


def _make_chunk(chunk_type: bytes, data: bytes) -> bytes:
    length = struct.pack(">I", len(data))
    crc = struct.pack(">I", zlib.crc32(chunk_type + data) & 0xFFFFFFFF)
    return length + chunk_type + data + crc


def make_default_avatar() -> bytes:
    signature = b"\x89PNG\r\n\x1a\n"
    ihdr = _make_chunk(
        b"IHDR",
        struct.pack(">IIBBBBB", 96, 96, 8, 6, 0, 0, 0),
    )

    raw = bytearray()
    for _ in range(96):
        raw.append(0)
        raw.extend(b"\x6b\x8e\xb5\xff" * 96)

    idat = _make_chunk(b"IDAT", zlib.compress(bytes(raw)))
    iend = _make_chunk(b"IEND", b"")

    return signature + ihdr + idat + iend
