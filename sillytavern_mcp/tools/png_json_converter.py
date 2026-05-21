import os
import json
import logging

from sillytavern_mcp.default_avatar import make_default_avatar
from sillytavern_mcp.png_util import extract_character_json, embed_character_json, image_file_to_data_uri, data_uri_to_bytes
from sillytavern_mcp.utils import sanitize_filename, resolve_st_dirs, find_st_default_avatar

logger = logging.getLogger(__name__)


def _resolve_output_path(output_path: str | None, fallback_dir: str, filename: str) -> str:
    if output_path:
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        return output_path
    os.makedirs(fallback_dir, exist_ok=True)
    return os.path.join(fallback_dir, filename)


def _get_character_name(card: dict) -> str:
    return card.get("data", {}).get("name") or card.get("name", "character")


def _extract_avatar_bytes(card: dict, avatar_path: str | None = None) -> tuple[bytes, str]:
    for source in [
        card.get("data", {}).get("avatar"),
        card.get("avatar"),
    ]:
        if isinstance(source, str) and source.startswith("data:image"):
            try:
                raw, _ = data_uri_to_bytes(source)
                return raw, "embedded card avatar"
            except Exception:
                pass

    if avatar_path and os.path.isfile(avatar_path):
        with open(avatar_path, "rb") as f:
            return f.read(), avatar_path

    default_avatar = find_st_default_avatar()
    if default_avatar:
        return default_avatar, "SillyTavern default (ai4.png)"

    return make_default_avatar(), "generated placeholder"


def register_tool(mcp):
    @mcp.tool(description="Extract the V2/V3 character JSON metadata from a character card PNG and save it as a .json file. Default output goes to the ST characters directory. Supports custom output_path.")  # noqa: E501
    async def convert_png_to_json(
        source_path: str,
        output_path: str | None = None,
        st_data_path: str | None = None,
        user: str | None = None,
    ) -> str:
        if not os.path.isfile(source_path):
            return f"Error: file not found: {source_path}"

        with open(source_path, "rb") as f:
            png_bytes = f.read()
        try:
            card = extract_character_json(png_bytes)
        except ValueError as e:
            return f"Error: {e}"

        char_name = _get_character_name(card)
        safe_name = sanitize_filename(char_name)
        fallback_dir, _ = resolve_st_dirs(st_data_path, user)
        dest = _resolve_output_path(output_path, fallback_dir, f"{safe_name}.json")

        with open(dest, "w", encoding="utf-8") as f:
            json.dump(card, f, ensure_ascii=False, indent=2)

        spec = card.get("spec", "unknown")
        parts = [
            f"Extracted character card JSON to: {dest}",
            f"Character: {char_name}",
            f"Spec: {spec}",
        ]
        return "\n".join(parts)

    @mcp.tool(description="Convert a character card JSON file (V2/V3 format) into a PNG character card with avatar. Avatar priority: embedded JSON avatar > avatar_path param > ST default > generated placeholder. Default output goes to the ST characters directory.")  # noqa: E501
    async def convert_json_to_png(
        source_path: str,
        avatar_path: str | None = None,
        output_path: str | None = None,
        st_data_path: str | None = None,
        user: str | None = None,
    ) -> str:
        if not os.path.isfile(source_path):
            return f"Error: file not found: {source_path}"

        with open(source_path, "r", encoding="utf-8") as f:
            card = json.load(f)

        char_name = _get_character_name(card)
        if not char_name:
            return "Error: invalid character card JSON — missing name"

        json_str = json.dumps(card, ensure_ascii=False)

        avatar_bytes, avatar_source = _extract_avatar_bytes(card, avatar_path)

        png_result = embed_character_json(avatar_bytes, json_str)

        safe_name = sanitize_filename(char_name)
        fallback_dir, _ = resolve_st_dirs(st_data_path, user)
        dest = _resolve_output_path(output_path, fallback_dir, f"{safe_name}.png")

        with open(dest, "wb") as f:
            f.write(png_result)

        parts = [
            f"Character card PNG written to: {dest}",
            f"Character: {char_name}",
            f"Avatar source: {avatar_source}",
        ]
        return "\n".join(parts)

    @mcp.tool(description="Embed a cover/banner image into a character card PNG's extensions.cover field. The image is stored as a base64 data URI. Default output goes to the ST characters directory.")  # noqa: E501
    async def embed_cover_image(
        source_path: str,
        cover_image_path: str,
        output_path: str | None = None,
        st_data_path: str | None = None,
        user: str | None = None,
    ) -> str:
        if not os.path.isfile(source_path):
            return f"Error: source PNG not found: {source_path}"
        if not os.path.isfile(cover_image_path):
            return f"Error: cover image not found: {cover_image_path}"

        with open(source_path, "rb") as f:
            png_bytes = f.read()
        try:
            card = extract_character_json(png_bytes)
        except ValueError as e:
            return f"Error: {e}"

        cover_uri = image_file_to_data_uri(cover_image_path)

        data = card.setdefault("data", {})
        extensions = data.setdefault("extensions", {})
        extensions["cover"] = cover_uri

        json_str = json.dumps(card, ensure_ascii=False)
        png_result = embed_character_json(png_bytes, json_str)

        char_name = _get_character_name(card)
        safe_name = sanitize_filename(char_name)
        fallback_dir, _ = resolve_st_dirs(st_data_path, user)
        dest = _resolve_output_path(output_path, fallback_dir, f"{safe_name}_cover.png")

        with open(dest, "wb") as f:
            f.write(png_result)

        cover_fmt = cover_uri.split(";")[0].split("/")[-1]
        cover_kb = len(cover_uri) * 3 // 4 / 1024
        return (
            f"Cover image embedded into: {dest}\n"
            f"Character: {char_name}\n"
            f"Cover format: {cover_fmt}, ~{cover_kb:.0f} KB (base64)"
        )

    @mcp.tool(description="Extract the cover/banner image from a character card PNG's extensions.cover field and save it as an image file. Default output goes to the ST characters directory.")  # noqa: E501
    async def extract_cover_image(
        source_path: str,
        output_path: str | None = None,
        st_data_path: str | None = None,
        user: str | None = None,
    ) -> str:
        if not os.path.isfile(source_path):
            return f"Error: file not found: {source_path}"

        with open(source_path, "rb") as f:
            png_bytes = f.read()
        try:
            card = extract_character_json(png_bytes)
        except ValueError as e:
            return f"Error: {e}"

        cover_uri = card.get("data", {}).get("extensions", {}).get("cover")
        if not cover_uri:
            return f"No cover image found in {source_path} (data.extensions.cover is empty)"

        try:
            cover_bytes, mime = data_uri_to_bytes(cover_uri)
        except Exception as e:
            return f"Error: failed to decode cover image: {e}"

        ext_map = {
            "image/png": "png",
            "image/jpeg": "jpg",
            "image/webp": "webp",
            "image/gif": "gif",
            "image/bmp": "bmp",
        }
        cover_ext = ext_map.get(mime, "png")

        char_name = _get_character_name(card)
        safe_name = sanitize_filename(char_name)
        fallback_dir, _ = resolve_st_dirs(st_data_path, user)
        dest = _resolve_output_path(output_path, fallback_dir, f"{safe_name}_cover.{cover_ext}")

        with open(dest, "wb") as f:
            f.write(cover_bytes)

        cover_kb = len(cover_bytes) / 1024
        return (
            f"Cover image extracted to: {dest}\n"
            f"Character: {char_name}\n"
            f"Format: {mime}, {cover_kb:.0f} KB"
        )

    @mcp.tool(description="Read a character card PNG and return its metadata as a formatted text summary. Shows name, version, description, personality, tags, alternate greetings count, and whether a cover image is present.")  # noqa: E501
    async def get_character_card_info(
        source_path: str,
    ) -> str:
        if not os.path.isfile(source_path):
            return f"Error: file not found: {source_path}"

        with open(source_path, "rb") as f:
            png_bytes = f.read()
        try:
            card = extract_character_json(png_bytes)
        except ValueError as e:
            return f"Error: {e}"

        data = card.get("data", {})
        lines = [f"=== Character Card Info ==="]
        lines.append(f"File: {source_path}")
        lines.append(f"Name: {card.get('name', 'N/A')}")
        lines.append(f"Spec: {card.get('spec', 'N/A')} (v{card.get('spec_version', 'N/A')})")
        lines.append(f"Description: {data.get('description', 'N/A')[:200]}")
        lines.append(f"Personality: {data.get('personality', 'N/A')[:200]}")
        lines.append(f"Scenario: {data.get('scenario', 'N/A')[:200]}")
        lines.append(f"Creator: {data.get('creator', 'N/A')}")
        lines.append(f"Character version: {data.get('character_version', 'N/A')}")

        tags = data.get("tags", [])
        lines.append(f"Tags ({len(tags)}): {', '.join(tags) if tags else 'none'}")

        alt_greetings = data.get("alternate_greetings", [])
        lines.append(f"Alternate greetings: {len(alt_greetings)}")

        extensions = data.get("extensions", {})
        has_cover = "cover" in extensions and extensions["cover"]
        lines.append(f"Cover image: {'YES' if has_cover else 'NO'}")

        talk = extensions.get("talkativeness", "N/A")
        lines.append(f"Talkativeness: {talk}")

        return "\n".join(lines)
