import os
import json
import glob
import logging

from sillytavern_mcp import st_client
from sillytavern_mcp.utils import resolve_st_root, resolve_st_dirs, detect_st_root
from sillytavern_mcp.png_util import parse_chunks, find_text_chunks

logger = logging.getLogger(__name__)


def register_tool(mcp):
    @mcp.tool(description="Run a comprehensive health check on a running SillyTavern instance. Checks API connectivity, CSRF, character card integrity, chat files, config, and process status. Works on any running ST instance with zero configuration.")
    async def get_st_diagnostics(
        st_url: str | None = None,
        st_data_path: str | None = None,
    ) -> str:
        resolved_url = st_url or os.environ.get("SILLYTAVERN_URL") or "http://localhost:8000"
        results = []

        results.append("=== SillyTavern Diagnostics ===")

        # 1. API ping
        alive, ping_info = st_client.check_ping(resolved_url)
        results.append(f"\n[API] Ping: {'OK' if alive else 'FAILED'}")
        if not alive:
            results.append(f"      ST does not appear to be running at {resolved_url}")
            results.append(f"      Error: {ping_info}")
            return "\n".join(results)

        # 2. Version
        version_data = st_client.get_version(resolved_url)
        if version_data:
            ver_str = json.dumps(version_data) if isinstance(version_data, dict) else str(version_data)
            results.append(f"[Version] {ver_str[:200]}")

        # 3. CSRF / API accessibility
        csrf_status = st_client.get_csrf_status(resolved_url)
        results.append(f"[CSRF] Token available: {csrf_status['csrf_available']}")
        results.append(f"[API]  Characters endpoint: {'accessible' if csrf_status.get('api_accessible') else 'BLOCKED'}")
        if csrf_status.get("character_count") is not None:
            results.append(f"[API]  Character count from API: {csrf_status['character_count']}")
        if csrf_status.get("http_status"):
            results.append(f"[API]  HTTP {csrf_status['http_status']}: API returns errors")

        # 4. Character card file validation
        chars_dir, data_dir = resolve_st_dirs(st_data_path)
        if data_dir and os.path.isdir(chars_dir):
            png_files = glob.glob(os.path.join(chars_dir, "*.png"))
            valid = 0
            invalid = 0
            invalid_names = []
            for fp in png_files:
                try:
                    with open(fp, "rb") as f:
                        data = f.read()
                    chunks = parse_chunks(data)
                    has_chara = len(find_text_chunks(chunks, b"chara")) > 0
                    if has_chara:
                        valid += 1
                    else:
                        invalid += 1
                        invalid_names.append(os.path.basename(fp))
                except Exception:
                    invalid += 1
                    invalid_names.append(os.path.basename(fp))
            results.append(f"\n[Characters] {valid} valid, {invalid} problematic out of {len(png_files)} files")
            if invalid_names:
                for n in invalid_names[:10]:
                    results.append(f"  - {n} (missing chara/ccv3 metadata or corrupt)")

            # chat file check
            chats_root = os.path.join(data_dir, os.environ.get("SILLYTAVERN_USER", "default-user"), "chats")
            if os.path.isdir(chats_root):
                char_dirs = [d for d in os.listdir(chats_root) if os.path.isdir(os.path.join(chats_root, d))]
                empty_chars = []
                for cd in char_dirs:
                    chat_files = os.listdir(os.path.join(chats_root, cd))
                    jsonl_files = [f for f in chat_files if f.endswith(".jsonl")]
                    if not jsonl_files:
                        empty_chars.append(cd)
                results.append(f"[Chats] {len(char_dirs)} character chat dirs, {len(empty_chars)} with no chat files")
                if empty_chars[:5]:
                    results.append(f"  Empty: {', '.join(empty_chars[:5])}")
        else:
            results.append(f"\n[Characters] Data directory not found: {chars_dir}")

        # 5. Config check
        st_root = resolve_st_root()
        if st_root:
            config_path = os.path.join(st_root, "config.yaml")
            if os.path.isfile(config_path):
                with open(config_path, "r", encoding="utf-8") as f:
                    config_text = f.read()
                checks = []
                checks.append(f"  enableServerPlugins: {'true' if 'enableServerPlugins: true' in config_text else 'false'}")
                checks.append(f"  basicAuthMode: {'true' if 'basicAuthMode: true' in config_text else 'false'}")
                checks.append(f"  whitelistMode: {'true' if 'whitelistMode: true' in config_text else 'false'}")
                results.append(f"\n[Config]")
                results.extend(checks)

            # Plugin check
            plugins_dir = os.path.join(st_root, "plugins")
            plugin_dirs = []
            if os.path.isdir(plugins_dir):
                plugin_dirs = [d for d in os.listdir(plugins_dir) if os.path.isdir(os.path.join(plugins_dir, d))]
            has_logger = "st-console-logger" in plugin_dirs
            results.append(f"[Plugins] {len(plugin_dirs)} installed: {', '.join(plugin_dirs) if plugin_dirs else 'none'}")
            if has_logger:
                results.append("  Console logger plugin: INSTALLED")
            else:
                results.append("  Console logger plugin: NOT INSTALLED (call setup_st_logging to install)")

        # 6. Access log
        if data_dir:
            access_log = os.path.join(data_dir, "access.log")
            if os.path.isfile(access_log):
                with open(access_log, "r", encoding="utf-8") as f:
                    all_lines = f.readlines()
                last_n = all_lines[-10:]
                results.append(f"\n[Access Log] {len(all_lines)} total entries (last 10):")
                for line in last_n:
                    results.append(f"  {line.rstrip()[:150]}")
            else:
                results.append(f"\n[Access Log] Not found at {access_log}")

        # 7. Process status (Windows)
        import subprocess
        try:
            result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq node.exe", "/FO", "CSV", "/NH"],
                capture_output=True, text=True, timeout=5,
            )
            node_processes = [l for l in result.stdout.strip().splitlines() if l.strip()]
            st_pids = []
            for line in node_processes:
                if "server.js" in line.lower() or "sillytavern" in line.lower():
                    st_pids.append(line)
            results.append(f"\n[Process] {len(node_processes)} node.exe processes running")
            if st_pids:
                results.append(f"  ST-related: {len(st_pids)}")
        except Exception:
            results.append(f"\n[Process] Could not query process list")

        return "\n".join(results)
