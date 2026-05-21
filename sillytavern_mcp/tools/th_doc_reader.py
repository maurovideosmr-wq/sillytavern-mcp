import logging
import os

from sillytavern_mcp.resources.docs_distilled import DISTILLED_DIR, _read_md_file

logger = logging.getLogger(__name__)

_DOC_NAMES = sorted(
    f.removesuffix(".md")
    for f in os.listdir(DISTILLED_DIR)
    if f.endswith(".md") and os.path.isfile(os.path.join(DISTILLED_DIR, f))
) if os.path.isdir(DISTILLED_DIR) else []


def register_tool(mcp):
    @mcp.tool(description=(
        "List all available documentation topics.\n"
        "Current docs: JS-Slash-Runner (Tavern Helper) — "
        + ", ".join(_DOC_NAMES)
        + ".\n"
        "Returns a numbered list; pass any name to read_doc."
    ))
    async def list_doc() -> str:
        if not os.path.isdir(DISTILLED_DIR):
            return "Error: doc directory not found."

        lines = [f"Available docs ({len(_DOC_NAMES)} total):"]
        for i, name in enumerate(_DOC_NAMES, 1):
            lines.append(f"  {i:2d}. {name}")
        lines.append("")
        lines.append('Use read_doc(name="<topic>") to read the full content.')
        return "\n".join(lines)

    @mcp.tool(description=(
        "Read the full content of a documentation page by topic name.\n"
        "Current docs: JS-Slash-Runner (Tavern Helper) — "
        + ", ".join(_DOC_NAMES)
        + ".\n"
        "Use list_doc to see all available topics."
    ))
    async def read_doc(name: str) -> str:
        if not os.path.isdir(DISTILLED_DIR):
            return "Error: doc directory not found."

        filepath = os.path.join(DISTILLED_DIR, f"{name}.md")
        if not os.path.isfile(filepath):
            return (
                f"Doc '{name}' not found.\n"
                f"Available: {', '.join(_DOC_NAMES)}\n"
                "Use list_doc to see the full list."
            )

        return _read_md_file(filepath)
