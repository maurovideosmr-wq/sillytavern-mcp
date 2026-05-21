import os


def detect_vendor_root() -> str | None:
    candidates = [
        os.path.join(os.getcwd(), "Vendor", "SillyTavern"),
        os.path.join(os.getcwd(), "..", "SillyTavern"),
    ]
    for p in candidates:
        if os.path.isdir(p):
            return os.path.abspath(p)
    return None


def detect_data_dir() -> str | None:
    vendor_root = detect_vendor_root()
    if vendor_root:
        data_dir = os.path.join(vendor_root, "data")
        if os.path.isdir(data_dir):
            return data_dir
    for p in ("data", os.path.join("..", "SillyTavern", "data")):
        full = os.path.join(os.getcwd(), p)
        if os.path.isdir(full):
            return os.path.abspath(full)
    return None


def find_st_default_avatar() -> bytes | None:
    vendor_root = detect_vendor_root()
    if vendor_root:
        avatar_path = os.path.join(vendor_root, "public", "img", "ai4.png")
        if os.path.isfile(avatar_path):
            with open(avatar_path, "rb") as f:
                return f.read()
    return None


def sanitize_filename(name: str) -> str:
    if not name or not name.strip():
        return ""
    safe = "".join(c for c in name.strip() if c not in r'<>:"/\|?*').strip()
    return safe[:200] if safe else "character"


def detect_st_root() -> str | None:
    vendor_root = detect_vendor_root()
    if vendor_root:
        return vendor_root
    data_dir = os.environ.get("SILLYTAVERN_DATA_DIR")
    if data_dir:
        parent = os.path.dirname(data_dir)
        if os.path.isfile(os.path.join(parent, "server.js")):
            return os.path.abspath(parent)
    return None


def resolve_st_root(st_root: str | None = None) -> str | None:
    if st_root:
        return st_root
    return detect_st_root()


def resolve_st_dirs(
    st_data_path: str | None = None,
    user: str | None = None,
) -> tuple[str, str]:
    data_dir = st_data_path or os.environ.get("SILLYTAVERN_DATA_DIR") or detect_data_dir()
    resolved_user = user or os.environ.get("SILLYTAVERN_USER") or "default-user"

    if data_dir:
        chars_dir = os.path.join(data_dir, resolved_user, "characters")
    else:
        chars_dir = os.path.join(os.getcwd(), "characters")

    os.makedirs(chars_dir, exist_ok=True)
    return chars_dir, data_dir or chars_dir


def resolve_st_url(st_url: str | None = None) -> str | None:
    return st_url or os.environ.get("SILLYTAVERN_URL")
