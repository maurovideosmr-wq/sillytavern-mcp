import logging
import os
import functools

from fastmcp.resources import FunctionResource

logger = logging.getLogger(__name__)

DISTILLED_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "docs",
    "JS-Slash-Runner-Distilled",
)

DOCS_URI_PREFIX = "docs://TH"


def _read_md_file(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def register(mcp) -> int:
    if not os.path.isdir(DISTILLED_DIR):
        logger.warning("Distilled docs directory not found at %s", DISTILLED_DIR)
        return 0

    count = 0
    for entry in sorted(os.listdir(DISTILLED_DIR)):
        if not entry.endswith(".md"):
            continue
        filepath = os.path.join(DISTILLED_DIR, entry)
        if not os.path.isfile(filepath):
            continue
        name = entry.removesuffix(".md")
        uri = f"{DOCS_URI_PREFIX}/{name}"

        fn = functools.partial(_read_md_file, filepath)
        fn.__name__ = f"read_th_doc_{name}"

        resource = FunctionResource.from_function(
            fn=fn,
            uri=uri,
            name=name,
            mime_type="text/markdown",
        )
        mcp.add_resource(resource)
        count += 1

    logger.info("Registered %d distilled doc resources (URI prefix: %s)", count, DOCS_URI_PREFIX)
    return count
