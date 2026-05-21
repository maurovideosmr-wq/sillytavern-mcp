import logging

from sillytavern_mcp import mcp
from sillytavern_mcp.tools.write_character import register_tool as register_write
from sillytavern_mcp.tools.import_character import register_tool as register_import
from sillytavern_mcp.tools.st_diagnostics import register_tool as register_diagnostics
from sillytavern_mcp.tools.st_console import register_tool as register_console
from sillytavern_mcp.tools.setup_logging import register_tool as register_setup

logger = logging.getLogger(__name__)


def setup():
    register_write(mcp)
    register_import(mcp)
    register_diagnostics(mcp)
    register_console(mcp)
    register_setup(mcp)
    logger.info("Tools registered")
