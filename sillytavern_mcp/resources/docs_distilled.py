import logging
import os
import functools

from fastmcp.resources import FunctionResource

logger = logging.getLogger(__name__)

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DOC_DIRS = [
    {
        "dir": os.path.join(ROOT, "docs", "ST-API-Distilled"),
        "uri_prefix": "docs://STAPI",
        "label": "SillyTavern REST API",
    },
    {
        "dir": os.path.join(ROOT, "docs", "JS-Slash-Runner-Distilled"),
        "uri_prefix": "docs://TH",
        "label": "JS-Slash-Runner (Tavern Helper)",
    },
    {
        "dir": os.path.join(ROOT, "docs", "ST-Prompt-Template-Distilled"),
        "uri_prefix": "docs://STPT",
        "label": "ST-Prompt-Template (EJS Templates)",
    },
    {
        "dir": os.path.join(ROOT, "docs", "MagVarUpdate-Distilled"),
        "uri_prefix": "docs://MVU",
        "label": "MagVarUpdate (MVU Variable Framework)",
    },
]


def _read_md_file(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def _list_md_files(doc_dir: str) -> list[tuple[str, str]]:
    if not os.path.isdir(doc_dir):
        return []
    result = []
    for entry in sorted(os.listdir(doc_dir)):
        if not entry.endswith(".md"):
            continue
        filepath = os.path.join(doc_dir, entry)
        if not os.path.isfile(filepath):
            continue
        name = entry.removesuffix(".md")
        result.append((name, filepath))
    return result


def _name_to_slug(name: str) -> str:
    return name.replace("_", "-").replace(" ", "-")


def register(mcp) -> int:
    total = 0
    for cfg in DOC_DIRS:
        files = _list_md_files(cfg["dir"])
        for name, filepath in files:
            uri = f"{cfg['uri_prefix']}/{name}"
            fn = functools.partial(_read_md_file, filepath)
            fn.__name__ = f"read_doc_{cfg['uri_prefix'].replace('://', '_')}_{name}"
            resource = FunctionResource.from_function(
                fn=fn,
                uri=uri,
                name=name,
                mime_type="text/markdown",
            )
            mcp.add_resource(resource)
            total += 1
        logger.info("Registered %d resources from %s", len(files), cfg["label"])
    logger.info("Total resources registered: %d", total)
    return total
