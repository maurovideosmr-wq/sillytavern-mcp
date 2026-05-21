import json
import logging
import urllib.request
import urllib.error
import http.cookiejar

logger = logging.getLogger(__name__)


class _STSession:
    def __init__(self):
        self.cookie_jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookie_jar)
        )

    def request(self, url: str, method: str = "GET", headers: dict | None = None, body: dict | None = None, timeout: int = 10):
        hdrs = {"Content-Type": "application/json", **(headers or {})}
        data = json.dumps(body).encode("utf-8") if body else None
        req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
        with self.opener.open(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))


_session = _STSession()


def _get_session():
    return _session


def get_csrf_token(st_url: str) -> str | None:
    try:
        _, result = _get_session().request(f"{st_url}/csrf-token")
        return result.get("token") or result.get("csrf_token")
    except Exception as e:
        logger.debug("Failed to get CSRF token from %s: %s", st_url, e)
        return None


def trigger_reload(st_url: str, csrf_token: str) -> bool:
    try:
        _get_session().request(
            f"{st_url}/api/characters/all",
            method="POST",
            headers={"x-csrf-token": csrf_token},
            body={},
        )
        logger.info("Character cache reload triggered at %s", st_url)
        return True
    except Exception as e:
        logger.warning("Failed to trigger character reload at %s: %s", st_url, e)
        return False


def try_refresh_characters(st_url: str) -> bool:
    token = get_csrf_token(st_url)
    if not token:
        return False
    return trigger_reload(st_url, token)


def check_ping(st_url: str) -> tuple[bool, str]:
    try:
        _, result = _get_session().request(f"{st_url}/csrf-token", timeout=5)
        return True, "ST responds to /csrf-token"
    except Exception:
        try:
            _, result = _get_session().request(f"{st_url}/version", timeout=5)
            return True, "ST responds to /version"
        except Exception as e2:
            return False, str(e2)


def get_version(st_url: str) -> dict | None:
    try:
        _, data = _get_session().request(f"{st_url}/version", timeout=5)
        return data
    except Exception:
        return None


def get_csrf_status(st_url: str) -> dict:
    token = get_csrf_token(st_url)
    if not token:
        return {"csrf_available": False, "csrf_token": None, "api_accessible": False}

    try:
        _, data = _get_session().request(
            f"{st_url}/api/characters/all",
            method="POST",
            headers={"x-csrf-token": token},
            body={},
            timeout=5,
        )
        char_count = 0
        if isinstance(data, list):
            char_count = len(data)
        return {"csrf_available": True, "csrf_token": token[:20] + "...", "api_accessible": True, "character_count": char_count}
    except urllib.error.HTTPError as e:
        return {"csrf_available": True, "csrf_token": token[:20] + "...", "api_accessible": False, "http_status": e.code, "error": str(e)}
    except Exception as e:
        return {"csrf_available": True, "csrf_token": token[:20] + "...", "api_accessible": False, "error": str(e)}
