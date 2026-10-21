"""Hosting mediow dla publikatora Instagrama.

Meta pobiera obrazy cURL-em z PUBLICZNEGO URL-a w chwili tworzenia kontenera, a plik musi
zyc jeszcze okolo godziny po publikacji. Ten modul daje jeden interfejs:

    host = get_media_host(cfg)            # wybor przez SOCIAL_MEDIA_HOST
    vhost = get_media_host(cfg, kind="video")  # SOCIAL_VIDEO_HOST, domyslnie ten sam host
    url  = host.upload(path, public_id)   # -> publiczny URL JPEG albo MP4 (po rozszerzeniu pliku)
    host.verify(url, kind)                # HEAD: 200 + content-type image/jpeg albo video/mp4
    host.cleanup(handles)                 # opcjonalnie, NIE wolane automatycznie

Wideo (rolki, .mp4): Cloudinary przyjmuje je przez /video/upload (limit pliku zalezy od planu,
darmowy 100 MB, nasze rolki maja kilka MB). Webflow Assets API wideo NIE przyjmuje (obrazy do
4 MB, dokumenty do 10 MB, Lottie; docs: developers.webflow.com/data/docs/working-with-assets),
dlatego WebflowHost.upload(.mp4) rzuca czytelny blad z rekomendacja SOCIAL_VIDEO_HOST=cloudinary.

Implementacje:
  cloudinary  REST upload (signed, gdy jest CLOUDINARY_API_SECRET; unsigned z
              CLOUDINARY_UPLOAD_PRESET w przeciwnym razie). Env: CLOUDINARY_CLOUD_NAME,
              CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET, opcjonalnie CLOUDINARY_FOLDER.
  webflow     Webflow Assets API v2, dwuetapowo jak hero w scripts/webflow/blog-publish.ps1:
              POST /v2/sites/{site}/assets (fileName + md5) -> multipart na presigned S3.
              Token i site id czytane z istniejacego scripts/webflow/.env (nie kopiujemy
              sekretow); zmienne WEBFLOW_API_TOKEN / WEBFLOW_SITE_ID w scripts/social/.env
              maja pierwszenstwo, jesli ktos chce osobny token.

cleanup NIE jest wolany przez ig-publish.py: Meta potrzebuje pliku jeszcze po publikacji,
a assety Webflow i tak lezaly dotad trwale (hero bloga). Sprzatanie to decyzja operatora.
"""

from __future__ import annotations

import hashlib
import mimetypes
import time
from pathlib import Path
from typing import Any, Callable

import requests

from ig_common import REPO_ROOT, parse_env_text

WEBFLOW_ENV_PATH = REPO_ROOT / "scripts" / "webflow" / ".env"
WEBFLOW_API = "https://api.webflow.com/v2"


class MediaHostError(Exception):
    pass


VIDEO_EXT = (".mp4",)
TYPY_OK = {"image": ("image/jpeg", "image/jpg"), "video": ("video/mp4",)}


def kind_of(path_or_url: str | Path) -> str:
    """'video' dla .mp4, inaczej 'image' (po rozszerzeniu, bez query stringa)."""
    s = str(path_or_url).split("?", 1)[0].lower()
    return "video" if s.endswith(VIDEO_EXT) else "image"


class MediaHost:
    name = "base"

    def __init__(self, session: Any = None, timeout: int = 60,
                 sleep: Callable[[float], None] = time.sleep, log: Callable[[str], None] = print):
        self.session = session or requests.Session()
        self.timeout = timeout
        self.sleep = sleep
        self.log = log

    def upload(self, path: Path, public_id: str) -> str:  # pragma: no cover - interfejs
        raise NotImplementedError

    def cleanup(self, handles: list[str]) -> None:
        """Domyslnie nic. Nadpisywane tam, gdzie API pozwala usunac plik."""
        return None

    def verify(self, url: str, kind: str | None = None, attempts: int = 4) -> None:
        """HEAD na URL: musi byc 200 i content-type image/jpeg (kind='image') albo video/mp4
        (kind='video'; domyslnie po rozszerzeniu URL-a). CDN potrafi potrzebowac chwili po
        uploadzie, wiec kilka prob z narastajaca przerwa."""
        kind = kind or kind_of(url)
        ok_types = TYPY_OK.get(kind, TYPY_OK["image"])
        last = ""
        for i in range(1, attempts + 1):
            try:
                r = self.session.head(url, allow_redirects=True, timeout=self.timeout)
                ctype = (r.headers.get("Content-Type") or "").split(";")[0].strip().lower()
                if r.status_code == 200 and ctype in ok_types:
                    return
                last = f"HTTP {r.status_code}, content-type={ctype or '?'}"
                if r.status_code == 200:  # zly typ nie naprawi sie sam
                    break
            except (requests.ConnectionError, requests.Timeout) as exc:
                last = f"{type(exc).__name__}: {exc}"
            if i < attempts:
                self.sleep(2 * i)
        raise MediaHostError(f"URL nie przeszedl kontroli HEAD ({last}): {url}")


# =====================================================================================
#  CLOUDINARY
# =====================================================================================
class CloudinaryHost(MediaHost):
    name = "cloudinary"

    def __init__(self, cfg: dict[str, str], **kw: Any):
        super().__init__(**kw)
        self.cloud = cfg.get("CLOUDINARY_CLOUD_NAME", "")
        self.api_key = cfg.get("CLOUDINARY_API_KEY", "")
        self.secret = cfg.get("CLOUDINARY_API_SECRET", "")
        self.preset = cfg.get("CLOUDINARY_UPLOAD_PRESET", "")
        self.folder = cfg.get("CLOUDINARY_FOLDER", "mindsync-social")
        if not self.cloud:
            raise MediaHostError("Brak CLOUDINARY_CLOUD_NAME w scripts/social/.env")
        if not (self.secret and self.api_key) and not self.preset:
            raise MediaHostError("Cloudinary: potrzebne CLOUDINARY_API_KEY + CLOUDINARY_API_SECRET "
                                 "(upload podpisany) albo CLOUDINARY_UPLOAD_PRESET (unsigned)")

    def _sign(self, params: dict[str, str]) -> str:
        to_sign = "&".join(f"{k}={params[k]}" for k in sorted(params) if params[k] != "")
        return hashlib.sha1((to_sign + self.secret).encode("utf-8")).hexdigest()

    def upload(self, path: Path, public_id: str) -> str:
        kind = kind_of(path)
        resource = "video" if kind == "video" else "image"
        url = f"https://api.cloudinary.com/v1_1/{self.cloud}/{resource}/upload"
        data: dict[str, str] = {"public_id": public_id, "folder": self.folder}
        if self.secret and self.api_key:
            data.update({"timestamp": str(int(time.time())), "overwrite": "true"})
            data["signature"] = self._sign(data)
            data["api_key"] = self.api_key
        else:
            data["upload_preset"] = self.preset
        with open(path, "rb") as fh:
            mime = "video/mp4" if kind == "video" else "image/jpeg"
            r = self.session.post(url, data=data, files={"file": (path.name, fh, mime)},
                                  timeout=max(self.timeout, 300) if kind == "video" else self.timeout)
        if r.status_code >= 300:
            raise MediaHostError(f"Cloudinary upload HTTP {r.status_code}: {r.text[:300]}")
        body = r.json()
        secure = body.get("secure_url")
        if not secure:
            raise MediaHostError(f"Cloudinary: brak secure_url w odpowiedzi ({path.name})")
        oczek = ("mp4",) if kind == "video" else ("jpg", "jpeg")
        if body.get("format") and body["format"].lower() not in oczek:
            raise MediaHostError(f"Cloudinary zapisal format {body['format']}, oczekiwany {'/'.join(oczek)}")
        return secure

    def cleanup(self, handles: list[str]) -> None:
        """handles = pelne public_id (z folderem). Tylko tryb podpisany."""
        if not (self.secret and self.api_key):
            raise MediaHostError("Cloudinary cleanup wymaga CLOUDINARY_API_SECRET")
        url = f"https://api.cloudinary.com/v1_1/{self.cloud}/image/destroy"
        for pid in handles:
            data = {"public_id": pid, "timestamp": str(int(time.time()))}
            data["signature"] = self._sign(data)
            data["api_key"] = self.api_key
            r = self.session.post(url, data=data, timeout=self.timeout)
            if r.status_code >= 300:
                raise MediaHostError(f"Cloudinary destroy {pid}: HTTP {r.status_code}")


# =====================================================================================
#  WEBFLOW ASSETS (wzor: Publish-WfAsset w scripts/webflow/blog-publish.ps1)
# =====================================================================================
class WebflowHost(MediaHost):
    name = "webflow"

    def __init__(self, cfg: dict[str, str], webflow_env_path: Path = WEBFLOW_ENV_PATH, **kw: Any):
        super().__init__(**kw)
        wf: dict[str, str] = {}
        if webflow_env_path.exists():
            wf = parse_env_text(webflow_env_path.read_text(encoding="utf-8-sig"))
        self.token = cfg.get("WEBFLOW_API_TOKEN") or wf.get("WEBFLOW_API_TOKEN", "")
        self.site_id = cfg.get("WEBFLOW_SITE_ID") or wf.get("WEBFLOW_SITE_ID", "")
        if not self.token or not self.site_id:
            raise MediaHostError("Webflow: brak WEBFLOW_API_TOKEN / WEBFLOW_SITE_ID "
                                 "(czytane z scripts/webflow/.env)")

    def _api(self, method: str, path: str, json_body: dict | None = None) -> dict:
        headers = {"Authorization": f"Bearer {self.token}", "Accept": "application/json"}
        for attempt in range(1, 6):
            try:
                r = self.session.request(method, f"{WEBFLOW_API}{path}", json=json_body,
                                         headers=headers, timeout=self.timeout)
            except (requests.ConnectionError, requests.Timeout) as exc:
                if attempt < 5:
                    self.sleep(2 ** attempt)
                    continue
                raise MediaHostError(f"Webflow {method} {path}: {exc}") from exc
            if r.status_code == 429 or r.status_code >= 500:
                if attempt < 5:
                    self.sleep(max(2 ** attempt, float(r.headers.get("Retry-After") or 0)))
                    continue
            if r.status_code >= 300:
                raise MediaHostError(f"Webflow {method} {path}: HTTP {r.status_code}: {r.text[:300]}")
            return r.json() if r.text.strip() else {}
        raise MediaHostError(f"Webflow {method} {path}: wyczerpane proby")

    def upload(self, path: Path, public_id: str) -> str:
        if kind_of(path) == "video":
            raise MediaHostError(
                "Webflow Assets API nie przyjmuje wideo (tylko obrazy do 4 MB, dokumenty do 10 MB, Lottie). "
                "Dla rolek ustaw SOCIAL_VIDEO_HOST=cloudinary (+ klucze CLOUDINARY_*) w scripts/social/.env; "
                "obrazy moga dalej isc przez Webflow.")
        data = path.read_bytes()
        fname = public_id.replace("/", "-") + ".jpg"
        meta = self._api("POST", f"/sites/{self.site_id}/assets",
                         {"fileName": fname, "fileHash": hashlib.md5(data).hexdigest()})
        upload_url = meta.get("uploadUrl")
        if not upload_url:
            raise MediaHostError(f"Webflow asset: brak uploadUrl ({fname})")
        # S3 presigned POST: najpierw pola z uploadDetails, plik na koncu (requests tak sklada)
        fields = {k: str(v) for k, v in (meta.get("uploadDetails") or {}).items()}
        r = self.session.post(upload_url, data=fields,
                              files={"file": (fname, data, "image/jpeg")}, timeout=self.timeout)
        if r.status_code >= 300:
            raise MediaHostError(f"Webflow asset: S3 upload HTTP {r.status_code} ({fname})")
        hosted = meta.get("hostedUrl") or meta.get("assetUrl")
        if not hosted and meta.get("id"):
            hosted = self._api("GET", f"/assets/{meta['id']}").get("hostedUrl")
        if not hosted:
            raise MediaHostError(f"Webflow asset: nie udalo sie ustalic hostedUrl ({fname})")
        return hosted


HOSTS = {"cloudinary": CloudinaryHost, "webflow": WebflowHost}


def get_media_host(cfg: dict[str, str], kind: str = "image", **kw: Any) -> MediaHost:
    """Host mediow. kind='video' bierze SOCIAL_VIDEO_HOST, a gdy go nie ma, SOCIAL_MEDIA_HOST."""
    name = ""
    if kind == "video":
        name = (cfg.get("SOCIAL_VIDEO_HOST") or "").strip().lower()
    name = name or (cfg.get("SOCIAL_MEDIA_HOST") or "").strip().lower()
    if not name:
        raise MediaHostError("Brak SOCIAL_MEDIA_HOST w scripts/social/.env (cloudinary | webflow)")
    if kind == "video" and name == "webflow":
        raise MediaHostError("Webflow nie hostuje wideo (Assets API: obrazy, dokumenty, Lottie). "
                             "Ustaw SOCIAL_VIDEO_HOST=cloudinary dla rolek.")
    if name not in HOSTS:
        raise MediaHostError(f"Nieznany SOCIAL_MEDIA_HOST='{name}' (dozwolone: {', '.join(HOSTS)})")
    return HOSTS[name](cfg, **kw)
