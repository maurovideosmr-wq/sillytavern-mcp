import os
import shutil
import logging

from sillytavern_mcp import st_client
from sillytavern_mcp.utils import sanitize_filename, resolve_st_dirs, resolve_st_url

logger = logging.getLogger(__name__)


def register_tool(mcp):
    @mcp.tool(description="Import an existing SillyTavern character card PNG file (with embedded V2/V3 metadata) into the SillyTavern characters directory. Copies the file as-is without modifying metadata.")  # noqa: E501
    async def import_character_card(
        source_path: str,
        st_data_path: str | None = None,
        user: str | None = None,
        st_url: str | None = None,
    ) -> str:
        if not os.path.isfile(source_path):
            return f"Error: source file not found: {source_path}"

        ext = os.path.splitext(source_path)[1].lower()
        if ext != ".png":
            return "Error: only .png character card files are supported."

        characters_dir, _ = resolve_st_dirs(st_data_path, user)

        safe_name = sanitize_filename(os.path.splitext(os.path.basename(source_path))[0])
        dest = os.path.join(characters_dir, f"{safe_name}.png")
        counter = 1
        while os.path.exists(dest):
            dest = os.path.join(characters_dir, f"{safe_name}_{counter}.png")
            counter += 1

        shutil.copy2(source_path, dest)

        reload_triggered = False
        resolved_st_url = resolve_st_url(st_url)
        if resolved_st_url:
            reload_triggered = st_client.try_refresh_characters(resolved_st_url)

        parts = [
            f"Character card imported: {source_path}",
            f"Copied to: {dest}",
        ]
        if reload_triggered:
            parts.append("SillyTavern cache refresh triggered via API.")
        elif resolved_st_url:
            parts.append("SillyTavern API refresh attempted.")
        else:
            parts.append(
                "Open the SillyTavern character list to see the new character. "
                "(Set SILLYTAVERN_URL for auto-refresh.)"
            )

        return "\n".join(parts)
