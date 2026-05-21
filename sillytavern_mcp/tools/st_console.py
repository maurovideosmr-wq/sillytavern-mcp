import os
import logging

from sillytavern_mcp.utils import resolve_st_dirs

logger = logging.getLogger(__name__)


def register_tool(mcp):
    @mcp.tool(description="Read the SillyTavern console log file (st_console.log) written by the st-console-logger plugin. Returns recent lines with support for incremental reading via since_line.")
    async def get_st_console(
        lines: int = 100,
        since_line: int = 0,
        st_data_path: str | None = None,
    ) -> str:
        _, data_dir = resolve_st_dirs(st_data_path)
        if not data_dir:
            return "Error: could not determine SillyTavern data directory"

        log_path = os.path.join(data_dir, "st_console.log")

        if not os.path.isfile(log_path):
            return (
                f"Console log not found at {log_path}.\n"
                "The st-console-logger plugin has not been installed, or ST has not been restarted since installation.\n"
                "Run setup_st_logging to install the plugin, then restart SillyTavern."
            )

        with open(log_path, "r", encoding="utf-8", errors="replace") as f:
            all_lines = f.readlines()

        total_lines = len(all_lines)

        if since_line >= total_lines:
            return f"Read {log_path}: {total_lines} total lines, no new lines since line {since_line}"

        start = max(0, since_line)
        end = min(start + lines, total_lines)
        selected = all_lines[start:end]

        file_size_kb = os.path.getsize(log_path) / 1024
        result = [
            f"Console log: {log_path}",
            f"File size: {file_size_kb:.1f} KB",
            f"Total lines: {total_lines}",
            f"Returned lines: {start}-{end} (showing last {end - start})\n",
        ]

        if not selected:
            result.append("(no output)")
        else:
            for line in selected:
                result.append(line.rstrip())

        return "\n".join(result)
