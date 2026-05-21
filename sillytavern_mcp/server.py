import logging

from sillytavern_mcp import mcp
from sillytavern_mcp.resources import docs_distilled as docs_resources
from sillytavern_mcp.tools.write_character import register_tool as register_write
from sillytavern_mcp.tools.import_character import register_tool as register_import
from sillytavern_mcp.tools.st_diagnostics import register_tool as register_diagnostics
from sillytavern_mcp.tools.st_console import register_tool as register_console
from sillytavern_mcp.tools.setup_logging import register_tool as register_setup
from sillytavern_mcp.tools.th_doc_reader import register_tool as register_th_docs

logger = logging.getLogger(__name__)


def setup():
    register_write(mcp)
    register_import(mcp)
    register_diagnostics(mcp)
    register_console(mcp)
    register_setup(mcp)
    register_th_docs(mcp)
    docs_resources.register(mcp)
    logger.info("Tools and resources registered")
