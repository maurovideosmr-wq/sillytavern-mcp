import os
import shutil
import logging

from sillytavern_mcp.utils import resolve_st_root

logger = logging.getLogger(__name__)

PLUGIN_SRC = os.path.join(os.path.dirname(os.path.dirname(__file__)), "st_console_plugin")


def register_tool(mcp):
    @mcp.tool(description="Install the st-console-logger plugin into SillyTavern's plugins/ directory and enable server plugins in config.yaml. Requires one ST restart to take effect.")
    async def setup_st_logging(
        st_root: str | None = None,
    ) -> str:
        resolved_root = resolve_st_root(st_root)
        if not resolved_root:
            return (
                "Error: could not detect SillyTavern root directory.\n"
                "Set SILLYTAVERN_DATA_DIR in kilo.json environment or pass st_root."
            )

        if not os.path.isdir(PLUGIN_SRC):
            return f"Error: plugin source not found at {PLUGIN_SRC}"

        plugin_dst = os.path.join(resolved_root, "plugins", "st-console-logger")
        os.makedirs(os.path.dirname(plugin_dst), exist_ok=True)

        if os.path.isdir(plugin_dst):
            shutil.rmtree(plugin_dst)
        shutil.copytree(PLUGIN_SRC, plugin_dst)

        parts = [f"Plugin copied to: {plugin_dst}"]

        config_path = os.path.join(resolved_root, "config.yaml")
        config_modified = False
        if os.path.isfile(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                config = f.read()

            if "enableServerPlugins: false" in config:
                config = config.replace("enableServerPlugins: false", "enableServerPlugins: true")
                with open(config_path, "w", encoding="utf-8") as f:
                    f.write(config)
                config_modified = True
                parts.append("config.yaml: enabled server plugins (enableServerPlugins: true)")
            elif "enableServerPlugins: true" in config:
                parts.append("config.yaml: server plugins already enabled")
            else:
                parts.append("config.yaml: could not find enableServerPlugins setting (check manually)")
        else:
            parts.append(f"config.yaml not found at {config_path}, check manually")

        parts.append("")
        parts.append("ST Console Logger installed successfully!")
        if config_modified:
            parts.append("  - Server plugins have been enabled in config.yaml")
        parts.append("  - Plugin files placed in plugins/st-console-logger/")
        parts.append("")
        parts.append("Next step: RESTART SillyTavern for the plugin to take effect.")
        parts.append("After restart, console output will be captured to data/st_console.log")
        parts.append("Use get_st_console to read the captured output.")

        return "\n".join(parts)
