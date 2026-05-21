import logging
import os

from sillytavern_mcp.resources.docs_distilled import DOC_DIRS, _read_md_file, _list_md_files

logger = logging.getLogger(__name__)

_DOC_INDEX: list[tuple[str, str, str]] = []
_DOC_BY_NAME: dict[str, list[tuple[str, str]]] = {}
_DESC_LINES: list[str] = []

for cfg in DOC_DIRS:
    files = _list_md_files(cfg["dir"])
    for name, filepath in files:
        _DOC_INDEX.append((name, filepath, cfg["label"]))
        _DOC_BY_NAME.setdefault(name, []).append((filepath, cfg["label"]))
    if files:
        names_str = ", ".join(n for n, _ in files)
        _DESC_LINES.append(f"{cfg['label']} — {names_str}")

_DESC = "Current docs: " + ". ".join(_DESC_LINES) if _DESC_LINES else "No docs available."


def register_tool(mcp):
    @mcp.tool(description=(
        "List all available documentation topics.\n"
        + _DESC + "\n"
        "Returns a grouped numbered list; pass any name to read_doc."
    ))
    async def list_doc() -> str:
        lines = [f"Available docs ({len(_DOC_INDEX)} total):"]
        for cfg in DOC_DIRS:
            files = _list_md_files(cfg["dir"])
            if not files:
                continue
            lines.append(f"\n  [{cfg['label']}]")
            for name, _ in files:
                lines.append(f"    - {name}")
        lines.append("")
        lines.append('Use read_doc(name="<topic>") to read the full content.')
        return "\n".join(lines)

    @mcp.tool(description=(
        "Read the full content of a documentation page by topic name.\n"
        + _DESC + "\n"
        "Use list_doc to see all available topics."
    ))
    async def read_doc(name: str) -> str:
        if not _DOC_BY_NAME:
            return "Error: no doc directories found."

        if name in _DOC_BY_NAME:
            entries = _DOC_BY_NAME[name]
            parts = []
            for filepath, label in entries:
                parts.append(f"--- {label} ---\n{_read_md_file(filepath)}")
            return "\n\n".join(parts)

        available = sorted(_DOC_BY_NAME.keys())
        return (
            f"Doc '{name}' not found.\n"
            f"Available: {', '.join(available)}\n"
            "Use list_doc to see the full list."
        )
