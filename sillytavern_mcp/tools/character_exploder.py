import os
import json
import re
import logging
from pathlib import Path

import yaml

from sillytavern_mcp.utils import sanitize_filename

logger = logging.getLogger(__name__)

LONG_TEXT_THRESHOLD = 800
LONG_REPLACE_THRESHOLD = 500

DATA_LONG_FIELDS = {
    "description", "personality", "scenario", "first_mes",
    "mes_example", "creator_notes", "system_prompt",
    "post_history_instructions",
}

DATA_META_FIELDS = {"creator", "character_version", "tags"}

CARD_EXCLUDED = {"data"}


def _get_char_name(card: dict) -> str:
    return card.get("data", {}).get("name") or card.get("name", "character")


def _dict_drop(data: dict, *keys: str) -> dict:
    return {k: v for k, v in data.items() if k not in keys}


def _is_long_text(value: str, threshold: int = LONG_TEXT_THRESHOLD) -> bool:
    return isinstance(value, str) and len(value) > threshold


def _read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def _write_file(path: str, content: str) -> None:
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(content)


def _dump_yaml(data) -> str:
    return yaml.safe_dump(
        data, allow_unicode=True, sort_keys=False,
        default_flow_style=False, width=120,
    )


def _read_yaml(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _write_yaml(path: str, data) -> None:
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(_dump_yaml(data))


def _resolve_path(card_dir: str, ref: str) -> str:
    if os.path.isabs(ref):
        return ref
    return os.path.normpath(os.path.join(card_dir, ref))


def _write_text_file_or_inline(value: str, threshold: int, dir_path: str, filename: str) -> str | dict:
    if _is_long_text(value, threshold):
        _write_file(os.path.join(dir_path, filename), value)
        return {"_path": filename}
    return value


def _resolve_ref(value, card_dir: str) -> str | dict:
    if isinstance(value, dict) and "_path" in value:
        return _read_file(_resolve_path(card_dir, value["_path"]))
    return value


def _resolve_ref_in_obj(obj, card_dir: str, key: str) -> None:
    if key in obj:
        obj[key] = _resolve_ref(obj[key], card_dir)


def _build_card_frontmatter(card: dict, data: dict) -> dict:
    fm = {}
    for k, v in card.items():
        if k in CARD_EXCLUDED:
            continue
        fm[k] = v
    return fm


def _extract_base64_image(value: str, output_dir: str, filename: str) -> str | None:
    if not isinstance(value, str) or not value.startswith("data:image"):
        return None
    import base64
    try:
        meta, b64 = value.split(",", 1)
        raw = base64.b64decode(b64)
        ext_map = {
            "image/png": "png", "image/jpeg": "jpg",
            "image/webp": "webp", "image/gif": "gif",
        }
        mime = meta.split(";")[0] if ";" in meta else "image/png"
        ext = ext_map.get(mime, "png")
        fpath = os.path.join(output_dir, filename)
        with open(fpath, "wb") as f:
            f.write(raw)
        return fpath
    except Exception:
        return None


def explode_card(
    source_path: str,
    output_dir: str | None = None,
) -> tuple[str, str, int]:
    if not os.path.isfile(source_path):
        raise FileNotFoundError(f"File not found: {source_path}")

    card = json.loads(_read_file(source_path))
    data = card.get("data", {})
    char_name = _get_char_name(card)
    safe_name = sanitize_filename(char_name)

    base_dir = output_dir or os.path.join(
        os.path.dirname(source_path) or os.getcwd(),
        f"{safe_name}_exploded",
    )
    os.makedirs(base_dir, exist_ok=True)

    created = []
    log = lambda p: created.append(os.path.relpath(p, base_dir))

    card_yaml = os.path.join(base_dir, "card.yaml")
    fm = _build_card_frontmatter(card, data)
    _write_yaml(card_yaml, fm)
    log(card_yaml)

    data_meta = {}
    for k in DATA_META_FIELDS:
        if k in data:
            data_meta[k] = data[k]
    # Also write creator_notes from data (may differ from card.creator_notes)
    if "creator_notes" in data and "creator_notes" not in card:
        data_meta["creator_notes"] = data["creator_notes"]
    if "group_only_greetings" in data:
        data_meta["group_only_greetings"] = True
    if data.get("alternate_greetings"):
        data_meta["alternate_greetings_count"] = len(data["alternate_greetings"])
    wb = data.get("character_book", {})
    if wb:
        wb_name = wb.get("name", "")
        if wb_name:
            data_meta["character_book_name"] = wb_name
    if data_meta:
        p = os.path.join(base_dir, "data_meta.yaml")
        _write_yaml(p, data_meta)
        log(p)

    for fname in DATA_LONG_FIELDS:
        val = data.get(fname, "")
        p = os.path.join(base_dir, f"{fname}.md")
        _write_file(p, val)
        log(p)

    cover_uri = data.get("extensions", {}).get("cover")
    if cover_uri:
        cover_path = _extract_base64_image(cover_uri, base_dir, "cover.png")
        if cover_path:
            log(cover_path)

    alt_greetings = data.get("alternate_greetings", [])
    if alt_greetings:
        gd = os.path.join(base_dir, "greetings")
        for i, g in enumerate(alt_greetings):
            preview = g.strip()[:40].replace("\r", "").replace("\n", " ").replace("/", "_")
            preview = sanitize_filename(preview) or ""
            fname = f"{i+1:02d}_{preview}.md" if preview else f"{i+1:02d}.md"
            p = os.path.join(gd, fname)
            _write_file(p, g)
            log(p)

    if "group_only_greetings" in data:
        gd = os.path.join(base_dir, "greetings_group")
        os.makedirs(gd, exist_ok=True)
        group_only = data.get("group_only_greetings", [])
        for i, g in enumerate(group_only):
            preview = g.strip()[:40].replace("\r", "").replace("\n", " ").replace("/", "_")
            preview = sanitize_filename(preview) or ""
            fname = f"{i+1:02d}_{preview}.md" if preview else f"{i+1:02d}.md"
            p = os.path.join(gd, fname)
            _write_file(p, g)
            log(p)

    dp = data.get("extensions", {}).get("depth_prompt", {})
    if dp:
        p = os.path.join(base_dir, "depth_prompt.yaml")
        _write_yaml(p, dp)
        log(p)

    regex_scripts = data.get("extensions", {}).get("regex_scripts", [])
    if regex_scripts:
        rd = os.path.join(base_dir, "regex")
        for idx, script in enumerate(regex_scripts):
            sname = script.get("scriptName", "unnamed")
            safe_sname = sanitize_filename(sname)
            out = _dict_drop(script, "replaceString")
            rs = script.get("replaceString", "")
            if _is_long_text(rs, LONG_REPLACE_THRESHOLD):
                html_name = f"{idx+1:02d}_{safe_sname}_replace.html"
                _write_file(os.path.join(rd, html_name), rs)
                out["replaceString"] = {"_path": html_name}
            else:
                out["replaceString"] = rs
            yml_name = f"{idx+1:02d}_{safe_sname}.yaml"
            p = os.path.join(rd, yml_name)
            _write_yaml(p, out)
            log(p)

    th = data.get("extensions", {}).get("tavern_helper")
    if th is not None:
        th_dir = os.path.join(base_dir, "tavern_helper")
        os.makedirs(th_dir, exist_ok=True)
        th_scripts = th.get("scripts", [])
        for idx, script in enumerate(th_scripts):
            sname = script.get("name", "unnamed")
            safe_sname = sanitize_filename(sname)
            script_dir = os.path.join(th_dir, f"{idx+1:02d}_{safe_sname}")
            out = _dict_drop(script, "content")
            content = script.get("content", "")
            if content:
                starts = ("import", "export", "function", "const", "let", "var", "$(()")
                ext = "js" if content.strip().startswith(starts) else "js"
                _write_file(os.path.join(script_dir, f"content.{ext}"), content)
                out["content"] = {"_path": f"content.{ext}"}
            else:
                out["content"] = ""
            p = os.path.join(script_dir, "script.yaml")
            _write_yaml(p, out)
            log(p)
        p = os.path.join(th_dir, "variables.yaml")
        _write_yaml(p, th.get("variables", {}))
        log(p)

    wb = data.get("character_book", {})
    if wb:
        wb_dir = os.path.join(base_dir, "worldbook")
        entries = wb.get("entries", [])
        wb_meta = _dict_drop(wb, "entries")
        if wb_meta:
            p = os.path.join(wb_dir, "meta.yaml")
            _write_yaml(p, wb_meta)
            log(p)
        if entries:
            ed = os.path.join(wb_dir, "entries")
            for entry in entries:
                eid = entry.get("id", 0)
                comment = entry.get("comment", "")
                safe_comment = sanitize_filename(comment) if comment else f"entry_{eid}"
                yml_name = f"{eid:06d}_{safe_comment}.yaml"
                out = _dict_drop(entry, "content")
                content = entry.get("content", "")
                if _is_long_text(content):
                    content_md = f"{eid:06d}_content.md"
                    _write_file(os.path.join(ed, content_md), content)
                    out["content"] = {"_path": content_md}
                else:
                    out["content"] = content
                p = os.path.join(ed, yml_name)
                _write_yaml(p, out)
                log(p)

    return char_name, base_dir, len(created)


def implode_card(source_dir: str, output_path: str | None = None) -> tuple[str, str]:
    if not os.path.isdir(source_dir):
        raise NotADirectoryError(f"Directory not found: {source_dir}")

    card_yaml = os.path.join(source_dir, "card.yaml")
    if not os.path.isfile(card_yaml):
        raise FileNotFoundError("card.yaml not found in source directory")

    fm = _read_yaml(card_yaml)
    if not isinstance(fm, dict):
        raise ValueError("Invalid card.yaml")

    card = {k: v for k, v in fm.items()}
    card.setdefault("spec", "chara_card_v3")
    card.setdefault("spec_version", "3.0")
    card.setdefault("avatar", "none")
    card.setdefault("talkativeness", 0.5)
    card.setdefault("fav", False)
    card.setdefault("tags", [])

    data = {}
    card["data"] = data
    data["name"] = card.get("name", "")

    # data_meta.yaml
    meta_path = os.path.join(source_dir, "data_meta.yaml")
    data_meta = _read_yaml(meta_path) if os.path.isfile(meta_path) else {}
    if isinstance(data_meta, dict):
        for k in DATA_META_FIELDS:
            if k in data_meta:
                data[k] = data_meta[k]
        if "creator_notes" in data_meta and "creator_notes" not in card:
            data["creator_notes"] = data_meta["creator_notes"]
        has_group_only = data_meta.get("group_only_greetings", False)
        alt_count = data_meta.get("alternate_greetings_count", 0)
        wb_name = data_meta.get("character_book_name", "")
    else:
        has_group_only = False
        alt_count = 0
        wb_name = ""

    for fname in DATA_LONG_FIELDS:
        fpath = os.path.join(source_dir, f"{fname}.md")
        data[fname] = _read_file(fpath) if os.path.isfile(fpath) else ""

    greetings_dir = os.path.join(source_dir, "greetings")
    alt_greetings = []
    if os.path.isdir(greetings_dir):
        for gf in sorted(f for f in os.listdir(greetings_dir) if f.endswith((".md", ".txt"))):
            alt_greetings.append(_read_file(os.path.join(greetings_dir, gf)))
    data["alternate_greetings"] = alt_greetings

    greetings_group_dir = os.path.join(source_dir, "greetings_group")
    group_only = []
    if os.path.isdir(greetings_group_dir):
        for gf in sorted(f for f in os.listdir(greetings_group_dir) if f.endswith((".md", ".txt"))):
            group_only.append(_read_file(os.path.join(greetings_group_dir, gf)))
    if has_group_only or os.path.isdir(greetings_group_dir):
        data["group_only_greetings"] = group_only

    extensions = {}
    data["extensions"] = extensions
    extensions["talkativeness"] = card.get("talkativeness", "0.5")
    extensions["fav"] = card.get("fav", False)
    if wb_name:
        extensions["world"] = wb_name

    dp_path = os.path.join(source_dir, "depth_prompt.yaml")
    if os.path.isfile(dp_path):
        dp = _read_yaml(dp_path)
        if isinstance(dp, dict):
            extensions["depth_prompt"] = dp
    else:
        extensions["depth_prompt"] = {"prompt": "", "depth": 4, "role": "system"}

    cover_path = os.path.join(source_dir, "cover.png")
    if os.path.isfile(cover_path):
        import base64
        with open(cover_path, "rb") as f:
            raw = f.read()
        b64 = base64.b64encode(raw).decode("ascii")
        extensions["cover"] = f"data:image/png;base64,{b64}"

    regex_dir = os.path.join(source_dir, "regex")
    regex_scripts = []
    if os.path.isdir(regex_dir):
        for rf in sorted(f for f in os.listdir(regex_dir) if f.endswith(".yaml")):
            script = _read_yaml(os.path.join(regex_dir, rf))
            if not isinstance(script, dict):
                continue
            rs = script.get("replaceString")
            if isinstance(rs, dict) and "_path" in rs:
                html_path = _resolve_path(regex_dir, rs["_path"])
                if os.path.isfile(html_path):
                    script["replaceString"] = _read_file(html_path)
            regex_scripts.append(script)
    if regex_scripts:
        extensions["regex_scripts"] = regex_scripts

    th_dir = os.path.join(source_dir, "tavern_helper")
    th = {}
    if os.path.isdir(th_dir):
        th_scripts = []
        for item in sorted(os.listdir(th_dir)):
            script_dir = os.path.join(th_dir, item)
            if not os.path.isdir(script_dir):
                continue
            syaml = os.path.join(script_dir, "script.yaml")
            if not os.path.isfile(syaml):
                continue
            script = _read_yaml(syaml)
            if not isinstance(script, dict):
                continue
            content_ref = script.get("content")
            if isinstance(content_ref, dict) and "_path" in content_ref:
                cpath = _resolve_path(script_dir, content_ref["_path"])
                if os.path.isfile(cpath):
                    script["content"] = _read_file(cpath)
            th_scripts.append(script)
        th["scripts"] = th_scripts
        vars_path = os.path.join(th_dir, "variables.yaml")
        if os.path.isfile(vars_path):
            th_vars = _read_yaml(vars_path)
            if isinstance(th_vars, dict):
                th["variables"] = th_vars
        th.setdefault("variables", {})
        extensions["tavern_helper"] = th

    wb_dir = os.path.join(source_dir, "worldbook")
    wb = {}
    if os.path.isdir(wb_dir):
        meta_path = os.path.join(wb_dir, "meta.yaml")
        if os.path.isfile(meta_path):
            wb_meta = _read_yaml(meta_path)
            if isinstance(wb_meta, dict):
                wb.update(wb_meta)
        entries_dir = os.path.join(wb_dir, "entries")
        entries = []
        if os.path.isdir(entries_dir):
            for ef in sorted(f for f in os.listdir(entries_dir) if f.endswith(".yaml")):
                entry = _read_yaml(os.path.join(entries_dir, ef))
                if not isinstance(entry, dict):
                    continue
                content_ref = entry.get("content")
                if isinstance(content_ref, dict) and "_path" in content_ref:
                    cpath = _resolve_path(entries_dir, content_ref["_path"])
                    if os.path.isfile(cpath):
                        entry["content"] = _read_file(cpath)
                entries.append(entry)
        if entries:
            entries.sort(key=lambda e: e.get("id", 0))
            wb["entries"] = entries
    if wb:
        data["character_book"] = wb

    if card.get("name") is None:
        card["name"] = data.get("name", "character")

    if "create_date" not in card:
        from datetime import datetime, timezone
        card["create_date"] = datetime.now(timezone.utc).isoformat()

    char_name = _get_char_name(card)
    safe_name = sanitize_filename(char_name)
    if output_path:
        dest = output_path
    else:
        dest = os.path.join(os.path.dirname(source_dir) or os.getcwd(), f"{safe_name}.json")

    os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
    _write_json(dest, card)

    return char_name, dest


def register_tool(mcp):
    @mcp.tool(
        description=(
            "Explode a SillyTavern character card JSON into multiple smaller "
            "YAML/MD/JS/HTML files organized by module for easier editing. "
            "Long texts become separate .md files, worldbook entries, regex scripts, "
            "and tavern_helper scripts each get their own YAML files."
        )
    )
    async def explode_character_card(
        source_path: str,
        output_dir: str | None = None,
    ) -> str:
        try:
            char_name, base_dir, count = explode_card(source_path, output_dir)
            return (
                f"Exploded character card: {char_name}\n"
                f"Source: {source_path}\n"
                f"Output: {base_dir}\n"
                f"Files created: {count}"
            )
        except (FileNotFoundError, NotADirectoryError) as e:
            return f"Error: {e}"
        except Exception as e:
            logger.exception("Failed to explode card")
            return f"Error: {e}"

    @mcp.tool(
        description=(
            "Implode an exploded character card directory back into a single "
            "JSON character card file. Reads YAML/MD/JS/HTML files and "
            "reassembles the original JSON structure."
        )
    )
    async def implode_character_card(
        source_dir: str,
        output_path: str | None = None,
    ) -> str:
        try:
            char_name, dest = implode_card(source_dir, output_path)
            card = json.loads(_read_file(dest))
            spec = card.get("spec", "unknown")
            return (
                f"Reassembled character card JSON: {dest}\n"
                f"Character: {char_name}\n"
                f"Spec: {spec}"
            )
        except (FileNotFoundError, NotADirectoryError) as e:
            return f"Error: {e}"
        except Exception as e:
            logger.exception("Failed to implode card")
            return f"Error: {e}"


def _write_json(path: str, card: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(card, f, ensure_ascii=False, indent=2)
