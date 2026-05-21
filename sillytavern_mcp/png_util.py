import json
import os
import struct
import zlib
import base64


def _make_chunk(chunk_type: bytes, data: bytes) -> bytes:
    length = struct.pack(">I", len(data))
    crc = struct.pack(">I", zlib.crc32(chunk_type + data) & 0xFFFFFFFF)
    return length + chunk_type + data + crc


def parse_chunks(png_bytes: bytes) -> list[dict]:
    if png_bytes[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("Not a valid PNG file")
    chunks = []
    offset = 8
    while offset < len(png_bytes):
        length = struct.unpack(">I", png_bytes[offset : offset + 4])[0]
        chunk_type = png_bytes[offset + 4 : offset + 8]
        data = png_bytes[offset + 8 : offset + 8 + length]
        chunks.append({"type": chunk_type, "data": data})
        offset += 12 + length
    return chunks


def assemble_png(chunks: list[dict]) -> bytes:
    out = b"\x89PNG\r\n\x1a\n"
    for c in chunks:
        out += _make_chunk(c["type"], c["data"])
    return out


def find_text_chunks(chunks: list[dict], keyword: bytes) -> list[int]:
    indices = []
    for i, c in enumerate(chunks):
        if c["type"] != b"tEXt":
            continue
        null_pos = c["data"].find(b"\x00")
        if null_pos < 0:
            continue
        kw = c["data"][:null_pos]
        if kw.lower() == keyword.lower():
            indices.append(i)
    return indices


def make_text_chunk(keyword: str, text: str) -> dict:
    data = keyword.encode("latin-1") + b"\x00" + text.encode("latin-1")
    return {"type": b"tEXt", "data": data}


def embed_character_json(png_bytes: bytes, json_str: str) -> bytes:
    chunks = parse_chunks(png_bytes)

    for idx in reversed(find_text_chunks(chunks, b"chara")):
        chunks.pop(idx)
    for idx in reversed(find_text_chunks(chunks, b"ccv3")):
        chunks.pop(idx)

    b64_json = base64.b64encode(json_str.encode("utf-8")).decode("ascii")

    v2_data = json.loads(json_str)
    v3_data = dict(v2_data)
    v3_data["spec"] = "chara_card_v3"
    v3_data["spec_version"] = "3.0"
    v3_json_str = json.dumps(v3_data, ensure_ascii=False)
    b64_v3 = base64.b64encode(v3_json_str.encode("utf-8")).decode("ascii")

    chara_chunk = make_text_chunk("chara", b64_json)
    ccv3_chunk = make_text_chunk("ccv3", b64_v3)

    iend_idx = len(chunks) - 1
    if iend_idx >= 0 and chunks[iend_idx]["type"] == b"IEND":
        chunks.insert(iend_idx, chara_chunk)
        chunks.insert(iend_idx + 1, ccv3_chunk)
    else:
        chunks.append(chara_chunk)
        chunks.append(ccv3_chunk)

    return assemble_png(chunks)


def extract_character_json(png_bytes: bytes) -> dict:
    chunks = parse_chunks(png_bytes)

    ccv3_indices = find_text_chunks(chunks, b"ccv3")
    if ccv3_indices:
        text_data = chunks[ccv3_indices[0]]["data"]
        null_pos = text_data.find(b"\x00")
        b64_text = text_data[null_pos + 1:].decode("latin-1")
        json_str = base64.b64decode(b64_text).decode("utf-8")
        return json.loads(json_str)

    chara_indices = find_text_chunks(chunks, b"chara")
    if chara_indices:
        text_data = chunks[chara_indices[0]]["data"]
        null_pos = text_data.find(b"\x00")
        b64_text = text_data[null_pos + 1:].decode("latin-1")
        json_str = base64.b64decode(b64_text).decode("utf-8")
        return json.loads(json_str)

    raise ValueError("No character metadata (chara/ccv3) found in PNG")


_IMAGE_MIME = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".bmp": "image/bmp",
}


def image_file_to_data_uri(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    mime = _IMAGE_MIME.get(ext, "image/png")
    with open(file_path, "rb") as f:
        raw = f.read()
    b64 = base64.b64encode(raw).decode("ascii")
    return f"data:{mime};base64,{b64}"


def data_uri_to_bytes(data_uri: str) -> tuple[bytes, str]:
    if "," not in data_uri:
        raise ValueError("Not a valid data URI")
    header, b64_data = data_uri.split(",", 1)
    mime = header.split(";")[0] if header.startswith("data:") else "image/png"
    mime = mime.replace("data:", "", 1)
    raw = base64.b64decode(b64_data)
    return raw, mime
