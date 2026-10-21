"""Wspolne klocki publikatora Instagrama MindSync (ig-publish.py, ig-token.py).

- odczyt i bezpieczny zapis scripts/social/.env (sekrety TYLKO tam, nigdy w kodzie),
- klient Instagram Graph API (graph.instagram.com) z retry i backoffem,
- czytelne bledy Meta (error.message, code, subcode, fbtrace_id).

Plik .env jest zrodlem prawdy. Zmienne srodowiskowe procesu sa tylko fallbackiem dla
kluczy, ktorych w pliku nie ma. Dzieki temu token odswiezony przez ig-token.py refresh
od razu obowiazuje w nastepnym przebiegu dripu, nawet jesli ktos ustawil stara wartosc
w zmiennych systemowych.
"""

from __future__ import annotations

import os
import random
import time
from pathlib import Path
from typing import Any, Callable

import requests

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent  # ...\Heroku
ENV_PATH = SCRIPT_DIR / ".env"

GRAPH_HOST = "https://graph.instagram.com"
DEFAULT_GRAPH_VERSION = "v23.0"

# Kody bledow Meta, ktore sa przejsciowe (rate limit, "please retry", serwis niedostepny).
TRANSIENT_META_CODES = {1, 2, 4, 17, 32, 341, 613}


# =====================================================================================
#  .env
# =====================================================================================
def parse_env_text(text: str) -> dict[str, str]:
    cfg: dict[str, str] = {}
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        key, val = s.split("=", 1)
        cfg[key.strip()] = val.strip().strip('"').strip("'")
    return cfg


def load_env(path: Path | None = None) -> dict[str, str]:
    """Plik .env wygrywa; os.environ uzupelnia tylko brakujace klucze."""
    path = path or ENV_PATH
    file_cfg: dict[str, str] = {}
    if path.exists():
        file_cfg = parse_env_text(path.read_text(encoding="utf-8-sig"))
    merged = {k: v for k, v in os.environ.items()}
    merged.update({k: v for k, v in file_cfg.items() if v != ""})
    return merged


def update_env_file(updates: dict[str, str], path: Path | None = None) -> None:
    """Podmienia/dopisuje klucze w .env, zachowujac komentarze i kolejnosc. Zapis atomowy."""
    path = path or ENV_PATH
    lines = path.read_text(encoding="utf-8-sig").splitlines() if path.exists() else []
    pending = dict(updates)
    out: list[str] = []
    for line in lines:
        s = line.strip()
        if s and not s.startswith("#") and "=" in s:
            key = s.split("=", 1)[0].strip()
            if key in pending:
                out.append(f"{key}={pending.pop(key)}")
                continue
        out.append(line)
    for key, val in pending.items():
        out.append(f"{key}={val}")
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text("\n".join(out) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def redact(params: dict[str, Any] | None) -> dict[str, Any]:
    """Kopia parametrow bez tokenu (do logow i DryRun)."""
    if not params:
        return {}
    return {k: ("<REDACTED>" if k == "access_token" else v) for k, v in params.items()}


# =====================================================================================
#  BLEDY
# =====================================================================================
class IgApiError(Exception):
    def __init__(self, message: str, *, status: int | None = None, code: int | None = None,
                 subcode: int | None = None, fbtrace_id: str | None = None,
                 retryable: bool = False, user_msg: str | None = None):
        self.status = status
        self.code = code
        self.subcode = subcode
        self.fbtrace_id = fbtrace_id
        self.retryable = retryable
        self.user_msg = user_msg
        super().__init__(message)

    def __str__(self) -> str:  # czytelnie, z kodami do szukania w docs Meta
        bits = [super().__str__()]
        meta = []
        if self.status is not None:
            meta.append(f"HTTP {self.status}")
        if self.code is not None:
            meta.append(f"code={self.code}")
        if self.subcode is not None:
            meta.append(f"subcode={self.subcode}")
        if self.fbtrace_id:
            meta.append(f"fbtrace_id={self.fbtrace_id}")
        if meta:
            bits.append("(" + ", ".join(meta) + ")")
        if self.user_msg:
            bits.append(f"| {self.user_msg}")
        return " ".join(bits)


def error_from_response(resp: requests.Response) -> IgApiError:
    status = resp.status_code
    try:
        body = resp.json()
    except ValueError:
        body = {}
    err = body.get("error") if isinstance(body, dict) else None
    if isinstance(err, dict):
        code = err.get("code")
        retryable = (status == 429 or status >= 500 or bool(err.get("is_transient"))
                     or code in TRANSIENT_META_CODES)
        return IgApiError(
            err.get("message") or f"HTTP {status}",
            status=status, code=code, subcode=err.get("error_subcode"),
            fbtrace_id=err.get("fbtrace_id"), retryable=retryable,
            user_msg=err.get("error_user_msg"),
        )
    text = (resp.text or "")[:300]
    return IgApiError(f"HTTP {status}: {text}", status=status,
                      retryable=(status == 429 or status >= 500))


# =====================================================================================
#  KLIENT GRAPH API
# =====================================================================================
class GraphClient:
    """Cienki klient graph.instagram.com. Token idzie jako parametr access_token,
    nigdy nie trafia do logow (patrz redact)."""

    def __init__(self, token: str, version: str = DEFAULT_GRAPH_VERSION, *,
                 session: Any = None, max_retry: int = 5, timeout: int = 60,
                 sleep: Callable[[float], None] = time.sleep,
                 log: Callable[[str], None] = print):
        self.token = token
        self.version = version.strip("/")
        self.session = session or requests.Session()
        self.max_retry = max_retry
        self.timeout = timeout
        self.sleep = sleep
        self.log = log

    def url(self, path: str, versioned: bool = True) -> str:
        path = path.lstrip("/")
        return f"{GRAPH_HOST}/{self.version}/{path}" if versioned else f"{GRAPH_HOST}/{path}"

    def request(self, method: str, path: str, params: dict[str, Any] | None = None, *,
                versioned: bool = True, retry: bool = True) -> dict[str, Any]:
        url = self.url(path, versioned)
        payload = dict(params or {})
        payload["access_token"] = self.token
        attempt = 0
        while True:
            attempt += 1
            try:
                if method.upper() == "GET":
                    resp = self.session.request("GET", url, params=payload, timeout=self.timeout)
                else:
                    resp = self.session.request(method.upper(), url, data=payload, timeout=self.timeout)
            except (requests.ConnectionError, requests.Timeout) as exc:
                err = IgApiError(f"Blad sieci: {type(exc).__name__}: {exc}", retryable=True)
                if retry and attempt < self.max_retry:
                    self._backoff(attempt, None, f"{method} {path}: {err}")
                    continue
                raise err from exc

            if 200 <= resp.status_code < 300:
                try:
                    return resp.json()
                except ValueError:
                    return {}

            err = error_from_response(resp)
            if retry and err.retryable and attempt < self.max_retry:
                self._backoff(attempt, resp.headers.get("Retry-After"), f"{method} {path}: {err}")
                continue
            raise err

    def _backoff(self, attempt: int, retry_after: str | None, why: str) -> None:
        wait = min(2 ** attempt, 60) + random.uniform(0, 1)
        try:
            if retry_after:
                wait = max(wait, float(retry_after))
        except ValueError:
            pass
        self.log(f"  RETRY {attempt}/{self.max_retry} za {wait:.1f}s: {why}")
        self.sleep(wait)
