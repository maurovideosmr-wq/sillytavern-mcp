import os
import logging

from sillytavern_mcp.default_avatar import make_default_avatar
from sillytavern_mcp.character_schema import build_v2_card
from sillytavern_mcp.png_util import embed_character_json
from sillytavern_mcp import st_client
from sillytavern_mcp.utils import sanitize_filename, resolve_st_dirs, resolve_st_url, find_st_default_avatar

logger = logging.getLogger(__name__)


def register_tool(mcp):
    @mcp.tool(description="Create a new SillyTavern character card from text attributes (name, personality, first message, etc). Writes a V2/V3 PNG card to the characters directory. Provide avatar_path for a custom avatar; otherwise uses the ST default avatar.")  # noqa: E501
    async def write_character_card(
        name: str,
        description: str = "",
        personality: str = "",
        scenario: str = "",
        first_mes: str = "",
        mes_example: str = "",
        creator_notes: str = "",
        system_prompt: str = "",
        post_history_instructions: str = "",
        tags: list[str] | None = None,
        alternate_greetings: list[str] | None = None,
        talkativeness: float = 0.5,
        creator: str = "",
        character_version: str = "1.0",
        avatar_path: str | None = None,
        st_data_path: str | None = None,
        user: str | None = None,
        st_url: str | None = None,
    ) -> str:
        safe_name = sanitize_filename(name)
        if not safe_name:
            return "Error: invalid character name"

        characters_dir, _ = resolve_st_dirs(st_data_path, user)
        output_path = os.path.join(characters_dir, f"{safe_name}.png")

        json_str = build_v2_card(
            name=name,
            description=description,
            personality=personality,
            scenario=scenario,
            first_mes=first_mes,
            mes_example=mes_example,
            creator_notes=creator_notes,
            system_prompt=system_prompt,
            post_history_instructions=post_history_instructions,
            tags=tags or [],
            alternate_greetings=alternate_greetings or [],
            talkativeness=talkativeness,
            creator=creator,
            character_version=character_version,
        )

        avatar_bytes = None
        avatar_source = None
        if avatar_path and os.path.isfile(avatar_path):
            with open(avatar_path, "rb") as f:
                avatar_bytes = f.read()
            avatar_source = avatar_path
        else:
            default_avatar = find_st_default_avatar()
            if default_avatar:
                avatar_bytes = default_avatar
                avatar_source = "SillyTavern default (ai4.png)"
            else:
                avatar_bytes = make_default_avatar()
                avatar_source = "generated placeholder"

        png_result = embed_character_json(avatar_bytes, json_str)

        with open(output_path, "wb") as f:
            f.write(png_result)

        reload_triggered = False
        resolved_st_url = resolve_st_url(st_url)
        if resolved_st_url:
            reload_triggered = st_client.try_refresh_characters(resolved_st_url)

        parts = [
            f"Character card written to: {output_path}",
            f"Avatar source: {avatar_source}",
        ]
        if reload_triggered:
            parts.append("SillyTavern cache refresh triggered via API.")
        elif resolved_st_url:
            parts.append("SillyTavern API refresh attempted (check ST console for details).")
        else:
            parts.append(
                "Open the SillyTavern character list to see the new character. "
                "(Set SILLYTAVERN_URL for auto-refresh.)"
            )

        return "\n".join(parts)
