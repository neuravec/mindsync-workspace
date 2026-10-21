"""Publikator Instagrama MindSync (kolejka social/queue -> Instagram API with Instagram Login).

DOMYSLNIE DRY-RUN: buduje i wypisuje dokladnie to, co by wyslal (endpointy i parametry bez
tokenu), sprawdza pliki i bramke, NIE uploaduje mediow i NIE dotyka graph.instagram.com.
Na zywo wylacznie z jawnym --live.

Uzycie:
    python scripts/social/ig-publish.py --id 2026-10-05-slug            # podglad (DRY)
    python scripts/social/ig-publish.py --id 2026-10-05-slug --live     # publikacja
    python scripts/social/ig-publish.py --due                           # co by poszlo teraz (DRY)
    python scripts/social/ig-publish.py --due --live                    # drip (Task Scheduler)

--due: posty `gotowy`, ktorych planowana_data + planowana_godzina_et (America/New_York)
<= teraz; max 1 post feed (carousel|single|reel) + 1 story na przebieg, najstarszy pierwszy.

Rolka (`typ: reel`): media = [social/media/<id>/reel.mp4, cover.jpg] (reel-render.py). Upload
MP4 na host wideo (SOCIAL_VIDEO_HOST, domyslnie SOCIAL_MEDIA_HOST; Webflow wideo nie przyjmuje)
+ HEAD video/mp4, okladka jak obraz; kontener media_type=REELS, video_url, cover_url, caption,
share_to_feed=true. Wideo przetwarza sie minutami: polling co IG_VIDEO_POLL_INTERVAL_SEC (15)
do IG_VIDEO_POLL_MAX_SEC (900).
Post zablokowany przez bramke jest pomijany i drip probuje kolejnego tego samego rodzaju.
Blad API przerywa dany rodzaj w tym przebiegu (bez kaskady), exit != 0.

Kolejnosc kontroli na post: idempotencja (publikacja.ig_media_id albo social/published-log.json)
-> status `gotowy` -> walidacja pliku i mediow -> scripts/social/social-gate.py --id <id>
-> limit publikacji (GET content_publishing_limit) -> upload mediow + HEAD -> kontenery
-> polling status_code -> media_publish -> zapis ig_media_id NATYCHMIAST -> permalink.

Kody wyjscia: 0 = ok / nic do zrobienia / pominiete (idempotencja), 1 = blad, 3 = bloker
(bramka, status, walidacja), 4 = inny przebieg trzyma blokade.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import traceback
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ig_common import (  # noqa: E402
    DEFAULT_GRAPH_VERSION, ENV_PATH, GRAPH_HOST, REPO_ROOT, GraphClient, IgApiError,
    load_env, redact,
)

ET = ZoneInfo("America/New_York")
FEED_TYPES = ("carousel", "single")
ALL_TYPES = ("carousel", "single", "story", "reel")
CAPTION_MAX = 2200
HASHTAG_MAX = 30
ALT_MAX = 1000
LOCK_STALE_SEC = 2 * 3600

EXIT_OK, EXIT_ERR, EXIT_BLOCKED, EXIT_LOCKED = 0, 1, 3, 4


# =====================================================================================
#  SCIEZKI
# =====================================================================================
@dataclass
class Paths:
    root: Path

    @property
    def queue(self) -> Path:
        return self.root / "social" / "queue"

    @property
    def published_log(self) -> Path:
        return self.root / "social" / "published-log.json"

    @property
    def drip_log(self) -> Path:
        return self.root / "social" / "_drip-log.txt"

    @property
    def drip_error(self) -> Path:
        return self.root / "social" / "_drip-error.txt"

    @property
    def lock(self) -> Path:
        return self.root / "social" / ".ig-publish.lock"

    @property
    def gate(self) -> Path:
        return self.root / "scripts" / "social" / "social-gate.py"


class Blocked(Exception):
    """Post nie moze isc na zywo (bramka, status, walidacja). Status bez zmian."""


class GateMissing(Blocked):
    pass


# =====================================================================================
#  JSON KOLEJKI I LOGI
# =====================================================================================
def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json_atomic(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def find_post_file(paths: Paths, post_id: str) -> Path:
    direct = paths.queue / f"{post_id}.json"
    if direct.exists():
        return direct
    for f in sorted(paths.queue.glob("*.json")):
        try:
            if read_json(f).get("id") == post_id:
                return f
        except (ValueError, OSError):
            continue
    raise FileNotFoundError(f"Nie ma posta o id '{post_id}' w {paths.queue}")


def load_published_log(paths: Paths) -> list[dict]:
    p = paths.published_log
    if not p.exists():
        write_json_atomic(p, [])
        return []
    raw = p.read_text(encoding="utf-8-sig").strip()
    if not raw:
        return []
    data = json.loads(raw)
    if not isinstance(data, list):  # nauczka z blog/published-log.json: tylko plaska tablica
        raise ValueError(f"{p} musi byc tablica JSON, jest {type(data).__name__}")
    return data


def already_published(post: dict, log: list[dict]) -> bool:
    pub = post.get("publikacja") or {}
    if pub.get("ig_media_id"):
        return True
    return any(e.get("id") == post.get("id") for e in log)


def write_drip_log(paths: Paths, live: bool, post_id: str, media_id: str | None, wynik: str) -> None:
    try:
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tryb = "LIVE" if live else "DRY"
        line = f"{stamp} | {tryb} | id={post_id or '?'} | media_id={media_id or '-'} | {wynik}"
        paths.drip_log.parent.mkdir(parents=True, exist_ok=True)
        with open(paths.drip_log, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
        print(f"  DRIP-LOG: {line}")
    except OSError as exc:
        print(f"  (drip-log nie zapisal: {exc})")


def write_drip_error(paths: Paths, live: bool, post_id: str, exc: BaseException) -> None:
    try:
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        block = "\n".join([
            "=" * 70,
            f"[{stamp}] tryb={'LIVE' if live else 'DRY'} id={post_id}",
            f"Wyjatek: {type(exc).__name__}: {exc}",
            "".join(traceback.format_exception(type(exc), exc, exc.__traceback__)),
        ])
        with open(paths.drip_error, "a", encoding="utf-8") as fh:
            fh.write(block + "\n")
    except OSError:
        pass


# =====================================================================================
#  WALIDACJA, CAPTION, PLAN KONTENEROW
# =====================================================================================
def build_caption(post: dict) -> str:
    caption = (post.get("caption") or "").strip()
    tags = []
    for t in post.get("hashtagi") or []:
        t = str(t).strip()
        if t:
            tags.append(t if t.startswith("#") else f"#{t}")
    if tags:
        return f"{caption}\n\n{' '.join(tags)}" if caption else " ".join(tags)
    return caption


def due_at(post: dict) -> datetime:
    d = post.get("planowana_data")
    h = post.get("planowana_godzina_et") or "00:00"
    if not d:
        raise ValueError("brak planowana_data")
    return datetime.strptime(f"{d} {h}", "%Y-%m-%d %H:%M").replace(tzinfo=ET)


def is_jpeg(path: Path) -> bool:
    with open(path, "rb") as fh:
        return fh.read(3) == b"\xff\xd8\xff"


def is_mp4(path: Path) -> bool:
    """Kontener ISO BMFF: bajty 4-8 = 'ftyp'."""
    with open(path, "rb") as fh:
        return fh.read(12)[4:8] == b"ftyp"


def validate_post(post: dict, paths: Paths) -> tuple[list[str], list[Path]]:
    """Zwraca (lista_problemow, sciezki_mediow). Pusta lista = OK."""
    problems: list[str] = []
    typ = post.get("typ")
    if post.get("platforma") != "instagram":
        problems.append(f"platforma='{post.get('platforma')}', oczekiwano 'instagram'")
    if typ not in ALL_TYPES:
        problems.append(f"typ='{typ}' (dozwolone: {', '.join(ALL_TYPES)})")
    media = post.get("media") or []
    files: list[Path] = []
    for i, rel in enumerate(media):
        p = (paths.root / rel).resolve()
        files.append(p)
        if not p.exists():
            problems.append(f"brak pliku media: {rel} (uruchom {'reel-render.py' if typ == 'reel' else 'render.py'})")
        elif typ == "reel" and i == 0:
            if not is_mp4(p):
                problems.append(f"rolka: pierwsze medium nie jest MP4: {rel}")
        elif not is_jpeg(p):
            problems.append(f"media nie jest JPEG: {rel}")
    if typ == "reel" and len(media) != 2:
        problems.append(f"reel wymaga 2 mediow [reel.mp4, cover.jpg], jest {len(media)}")
    if typ == "carousel" and not 2 <= len(media) <= 10:
        problems.append(f"carousel wymaga 2-10 mediow, jest {len(media)}")
    if typ in ("single", "story") and len(media) != 1:
        problems.append(f"{typ} wymaga dokladnie 1 medium, jest {len(media)}")
    if typ != "story":
        cap = build_caption(post)
        if not cap:
            problems.append("pusty caption")
        if len(cap) > CAPTION_MAX:
            problems.append(f"caption ma {len(cap)} znakow (max {CAPTION_MAX})")
        if cap.count("#") > HASHTAG_MAX:
            problems.append(f"caption ma {cap.count('#')} hashtagow (max {HASHTAG_MAX})")
        for i, alt in enumerate(post.get("alt_text") or []):
            if alt and len(alt) > ALT_MAX:
                problems.append(f"alt_text[{i}] ma {len(alt)} znakow (max {ALT_MAX})")
    try:
        due_at(post)
    except ValueError as exc:
        problems.append(f"zla data/godzina publikacji: {exc}")
    return problems, files


# AI Act art. 50 / Meta "AI info": posty z obrazem AI (te same reguly co social_common.slajd_ai)
AI_PREFIKSY = ("social/assets/variant-c/", "blog/images/")
POLA_OBRAZOW = ("obraz", "ekran", "ekran_przed", "ekran_po")


def post_is_ai(post: dict) -> bool:
    for sl in post.get("slajdy") or []:
        sl = sl or {}
        if isinstance(sl.get("ai_label"), bool):
            if sl["ai_label"]:
                return True
            continue
        pola = sl.get("pola") or {}
        if any(str(pola.get(k) or "").replace("\\", "/").startswith(AI_PREFIKSY) for k in POLA_OBRAZOW):
            return True
    return False


def container_requests(post: dict, urls: list[str], send_alt: bool) -> tuple[list[dict], dict]:
    """(kontenery_dzieci, kontener_glowny) jako slowniki parametrow POST /{ig}/media.

    Gdy post zawiera obraz AI, kontener glowny (nie dzieci karuzeli: API tego nie przyjmuje)
    dostaje is_ai_generated=true (samoujawnienie AI w Instagram API)."""
    children, parent = _container_requests(post, urls, send_alt)
    if post_is_ai(post):
        parent["is_ai_generated"] = "true"
    return children, parent


def _container_requests(post: dict, urls: list[str], send_alt: bool) -> tuple[list[dict], dict]:
    typ = post["typ"]
    alts = post.get("alt_text") or []
    caption = build_caption(post)

    def alt_for(i: int) -> dict:
        if send_alt and i < len(alts) and alts[i]:
            return {"alt_text": alts[i]}
        return {}

    if typ == "story":
        return [], {"media_type": "STORIES", "image_url": urls[0]}
    if typ == "reel":
        # urls = [video_url, cover_url]; alt_text dla rolek API nie przyjmuje
        parent = {"media_type": "REELS", "video_url": urls[0], "caption": caption, "share_to_feed": "true"}
        if len(urls) > 1 and urls[1]:
            parent["cover_url"] = urls[1]
        return [], parent
    if typ == "single":
        return [], {"image_url": urls[0], "caption": caption, **alt_for(0)}
    children = [{"is_carousel_item": "true", "image_url": u, **alt_for(i)} for i, u in enumerate(urls)]
    return children, {"media_type": "CAROUSEL", "children": None, "caption": caption}


# =====================================================================================
#  BRAMKA (agent A: scripts/social/social-gate.py)
# =====================================================================================
def run_gate(paths: Paths, post_id: str) -> tuple[bool, str]:
    if not paths.gate.exists():
        raise GateMissing(f"Brak bramki {paths.gate}. Bez niej publikacja na zywo jest zablokowana.")
    proc = subprocess.run(
        [sys.executable, str(paths.gate), "--id", post_id],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        cwd=str(paths.root), timeout=600,
    )
    out = ((proc.stdout or "") + (proc.stderr or "")).strip()
    return proc.returncode == 0, out


# =====================================================================================
#  PUBLIKATOR
# =====================================================================================
@dataclass
class Settings:
    ig_user_id: str = ""
    graph_version: str = DEFAULT_GRAPH_VERSION
    send_alt: bool = True
    poll_interval: float = 5.0
    poll_max_sec: float = 300.0
    video_poll_interval: float = 15.0
    video_poll_max_sec: float = 900.0
    media_host_name: str = ""
    video_host_name: str = ""

    @classmethod
    def from_env(cls, cfg: dict[str, str]) -> "Settings":
        return cls(
            ig_user_id=cfg.get("IG_USER_ID", ""),
            graph_version=cfg.get("IG_GRAPH_VERSION") or DEFAULT_GRAPH_VERSION,
            send_alt=(cfg.get("IG_SEND_ALT_TEXT", "1").strip().lower() not in ("0", "false", "no", "")),
            poll_interval=float(cfg.get("IG_POLL_INTERVAL_SEC") or 5),
            poll_max_sec=float(cfg.get("IG_POLL_MAX_SEC") or 300),
            video_poll_interval=float(cfg.get("IG_VIDEO_POLL_INTERVAL_SEC") or 15),
            video_poll_max_sec=float(cfg.get("IG_VIDEO_POLL_MAX_SEC") or 900),
            media_host_name=cfg.get("SOCIAL_MEDIA_HOST", ""),
            video_host_name=cfg.get("SOCIAL_VIDEO_HOST", "") or cfg.get("SOCIAL_MEDIA_HOST", ""),
        )


@dataclass
class Publisher:
    paths: Paths
    settings: Settings
    live: bool = False
    client: GraphClient | None = None
    media_host: Any = None
    video_host: Any = None   # host dla .mp4 (SOCIAL_VIDEO_HOST); None = media_host
    gate: Callable[[Paths, str], tuple[bool, str]] = run_gate
    sleep: Callable[[float], None] = time.sleep
    now_utc: Callable[[], datetime] = field(default=lambda: datetime.now(timezone.utc))
    config_error: str | None = None

    # ---------- jeden post ----------
    def process(self, post_file: Path) -> int:
        post = read_json(post_file)
        pid = post.get("id") or post_file.stem
        tryb = "LIVE" if self.live else "DRY-RUN (zero wysylki)"
        print(f"\n=== {pid} [{post.get('typ')}] {tryb}")

        log = load_published_log(self.paths)
        if already_published(post, log):
            print("  POMINIETO: post juz opublikowany (ig_media_id albo published-log)")
            write_drip_log(self.paths, self.live, pid, (post.get("publikacja") or {}).get("ig_media_id"),
                           "POMINIETO juz opublikowany")
            return EXIT_OK

        blockers: list[str] = []
        if post.get("status") != "gotowy":
            blockers.append(f"status='{post.get('status')}', wymagany 'gotowy'")
        problems, files = validate_post(post, self.paths)
        blockers += problems
        try:
            ok, out = self.gate(self.paths, pid)
            if out:
                print("  BRAMKA (social-gate.py):\n    " + out.replace("\n", "\n    "))
            if not ok:
                blockers.append("bramka social-gate.py zglosila blokery")
        except GateMissing as exc:
            blockers.append(str(exc))

        if not self.live:
            self.print_plan(post, files)
            if blockers:
                print("  BLOKERY (na zywo publikacja zostalaby przerwana):")
                for b in blockers:
                    print(f"    - {b}")
                write_drip_log(self.paths, False, pid, None, "BLOKER: " + "; ".join(blockers)[:300])
                return EXIT_BLOCKED
            write_drip_log(self.paths, False, pid, None, "DRY OK: plan zbudowany, nic nie wyslano")
            return EXIT_OK

        if blockers:
            for b in blockers:
                print(f"  BLOKER: {b}")
            write_drip_log(self.paths, True, pid, None, "POMINIETO bloker: " + "; ".join(blockers)[:300])
            return EXIT_BLOCKED

        try:
            media_id = self.publish_live(post, post_file, files)
        except Exception as exc:  # noqa: BLE001 - kazdy blad ma trafic do logu
            print(f"  BLAD: {exc}")
            write_drip_error(self.paths, True, pid, exc)
            write_drip_log(self.paths, True, pid, None, f"BLAD: {str(exc)[:300]}")
            return EXIT_ERR
        return EXIT_OK if media_id else EXIT_ERR

    # ---------- DRY: dokladny plan ----------
    def print_plan(self, post: dict, files: list[Path]) -> None:
        s = self.settings
        ig = s.ig_user_id or "<IG_USER_ID>"
        base = f"{GRAPH_HOST}/{s.graph_version}"
        cfg_warn = []
        if not s.ig_user_id:
            cfg_warn.append("IG_USER_ID")
        if not s.media_host_name:
            cfg_warn.append("SOCIAL_MEDIA_HOST")
        if cfg_warn:
            print(f"  UWAGA: na zywo brakowaloby w scripts/social/.env: {', '.join(cfg_warn)}")
        print("  PLAN (parametry bez tokenu; access_token dokladany w chwili wysylki):")
        print(f"    GET  {base}/{ig}/content_publishing_limit  fields=quota_usage,config")
        urls = []
        for i, f in enumerate(files, 1):
            ph = f"<URL {i:02d}>"
            urls.append(ph)
            exists = "OK" if f.exists() else "BRAK PLIKU"
            video = f.suffix.lower() == ".mp4"
            host = (s.video_host_name if video else s.media_host_name) or "?"
            uwaga = "  !! Webflow nie hostuje wideo, ustaw SOCIAL_VIDEO_HOST=cloudinary" if video and host == "webflow" else ""
            print(f"    UPLOAD [{host}] {f} ({exists}) -> {ph}, potem HEAD (200, "
                  f"{'video/mp4' if video else 'image/jpeg'}){uwaga}")
        if not files:
            return
        children, parent = container_requests(post, urls, s.send_alt)
        for i, ch in enumerate(children, 1):
            print(f"    POST {base}/{ig}/media  {json.dumps(ch, ensure_ascii=False)}  -> <CHILD {i}>")
            print(f"    GET  {base}/<CHILD {i}>  fields=status_code,status  (poll do FINISHED)")
        if children:
            parent = dict(parent, children=",".join(f"<CHILD {i}>" for i in range(1, len(children) + 1)))
        print(f"    POST {base}/{ig}/media  {json.dumps(parent, ensure_ascii=False)}  -> <CONTAINER>")
        if post.get("typ") == "reel":
            print(f"    GET  {base}/<CONTAINER>  fields=status_code,status  (poll co {s.video_poll_interval:g}s "
                  f"do FINISHED, maks. {s.video_poll_max_sec:g}s: wideo przetwarza sie minutami)")
        else:
            print(f"    GET  {base}/<CONTAINER>  fields=status_code,status  (poll do FINISHED)")
        print(f"    POST {base}/{ig}/media_publish  {{\"creation_id\": \"<CONTAINER>\"}}  -> <MEDIA_ID>")
        print(f"    GET  {base}/<MEDIA_ID>  fields=permalink")
        if post.get("typ") != "story":
            print("  CAPTION:\n    " + build_caption(post).replace("\n", "\n    "))

    # ---------- LIVE ----------
    def publish_live(self, post: dict, post_file: Path, files: list[Path]) -> str:
        if self.config_error:
            raise RuntimeError(self.config_error)
        if not self.client or not self.settings.ig_user_id:
            raise RuntimeError("Brak IG_ACCESS_TOKEN / IG_USER_ID w scripts/social/.env")
        if self.media_host is None:
            raise RuntimeError("Brak hosta mediow (SOCIAL_MEDIA_HOST)")
        ig = self.settings.ig_user_id
        pid = post["id"]

        self.check_quota()

        urls = []
        for i, f in enumerate(files, 1):
            video = f.suffix.lower() == ".mp4"
            host = (self.video_host or self.media_host) if video else self.media_host
            name = f"{pid}/{f.stem}" if post.get("typ") == "reel" else f"{pid}/{i:02d}"
            url = host.upload(f, name)
            host.verify(url, "video" if video else "image")
            print(f"  [media {i}/{len(files)}] {f.name} -> {url}")
            urls.append(url)

        children, parent = container_requests(post, urls, self.settings.send_alt)
        child_ids = []
        for i, ch in enumerate(children, 1):
            cid = self.client.request("POST", f"{ig}/media", ch)["id"]
            child_ids.append(cid)
            print(f"  [kontener dziecko {i}/{len(children)}] {cid}")
        for cid in child_ids:
            self.wait_finished(cid)
        if children:
            parent["children"] = ",".join(child_ids)
        container_id = self.client.request("POST", f"{ig}/media", parent)["id"]
        print(f"  [kontener] {container_id}")
        if post.get("typ") == "reel":
            self.wait_finished(container_id, self.settings.video_poll_max_sec, self.settings.video_poll_interval)
        else:
            self.wait_finished(container_id)

        media_id = self.publish_container(container_id)
        print(f"  [opublikowano] media_id={media_id}")

        # Zapis NATYCHMIAST po media_publish: nawet jesli permalink padnie, kolejny
        # przebieg nie opublikuje posta drugi raz.
        published_at = self.now_utc().astimezone(timezone.utc).isoformat(timespec="seconds")
        post = read_json(post_file)
        pub = post.get("publikacja") if isinstance(post.get("publikacja"), dict) else {}
        pub.update({"ig_container_id": container_id, "ig_media_id": media_id,
                    "permalink": pub.get("permalink"), "opublikowano": published_at})
        post["publikacja"] = pub
        post["status"] = "opublikowany"
        write_json_atomic(post_file, post)
        log = load_published_log(self.paths)
        entry = {"id": pid, "typ": post.get("typ"), "plik": post_file.name,
                 "ig_media_id": media_id, "permalink": None, "opublikowano": published_at}
        log.append(entry)
        write_json_atomic(self.paths.published_log, log)

        permalink = None
        try:
            permalink = self.client.request("GET", media_id, {"fields": "permalink"}).get("permalink")
        except IgApiError as exc:
            print(f"  UWAGA: nie pobrano permalinku ({exc}); post jest opublikowany")
        if permalink:
            post["publikacja"]["permalink"] = permalink
            write_json_atomic(post_file, post)
            entry["permalink"] = permalink
            write_json_atomic(self.paths.published_log, log)
        write_drip_log(self.paths, True, pid, media_id, f"OK opublikowano {permalink or '(bez permalinku)'}")
        return media_id

    def check_quota(self) -> None:
        ig = self.settings.ig_user_id
        res = self.client.request("GET", f"{ig}/content_publishing_limit", {"fields": "quota_usage,config"})
        data = (res.get("data") or [{}])[0]
        usage = int(data.get("quota_usage") or 0)
        total = int((data.get("config") or {}).get("quota_total") or 100)
        print(f"  [limit] {usage}/{total} publikacji w 24h")
        if usage >= total:
            raise IgApiError(f"Limit publikacji wyczerpany ({usage}/{total} w 24h), sprobuj pozniej")

    def wait_finished(self, container_id: str, max_sec: float | None = None,
                      interval: float | None = None) -> None:
        max_sec = self.settings.poll_max_sec if max_sec is None else max_sec
        interval = self.settings.poll_interval if interval is None else interval
        waited = 0.0
        while True:
            res = self.client.request("GET", container_id, {"fields": "status_code,status"})
            code = res.get("status_code")
            if code == "FINISHED":
                return
            if code in ("ERROR", "EXPIRED"):
                raise IgApiError(f"Kontener {container_id}: status_code={code} ({res.get('status') or 'brak opisu'})")
            if waited >= max_sec:
                raise IgApiError(f"Kontener {container_id}: brak FINISHED po {int(waited)}s (ostatnio {code})")
            self.sleep(interval)
            waited += interval

    def publish_container(self, container_id: str) -> str:
        """media_publish bez slepego retry: po bledzie przejsciowym najpierw sprawdzamy, czy
        kontener nie zostal juz opublikowany (timeout po stronie klienta przy udanej
        publikacji), zeby nie wrzucic posta dwa razy."""
        ig = self.settings.ig_user_id
        attempts = self.client.max_retry
        for attempt in range(1, attempts + 1):
            try:
                return self.client.request("POST", f"{ig}/media_publish",
                                           {"creation_id": container_id}, retry=False)["id"]
            except IgApiError as exc:
                if not exc.retryable or attempt == attempts:
                    raise
                try:
                    st = self.client.request("GET", container_id, {"fields": "status_code"}).get("status_code")
                except IgApiError:
                    st = None
                if st == "PUBLISHED":
                    recent = self.client.request("GET", f"{ig}/media", {"fields": "id,timestamp", "limit": 1})
                    items = recent.get("data") or []
                    if items:
                        print("  UWAGA: media_publish zwrocil blad, ale kontener jest PUBLISHED; "
                              "biore najnowsze media konta")
                        return items[0]["id"]
                self.client._backoff(attempt, None, f"media_publish: {exc}")
        raise IgApiError("media_publish: wyczerpane proby")  # pragma: no cover

    # ---------- DRIP ----------
    def run_due(self, now_et: datetime) -> int:
        log = load_published_log(self.paths)
        cands = []
        for f in sorted(self.paths.queue.glob("*.json")):
            if f.name.startswith("_"):
                continue
            try:
                post = read_json(f)
                if post.get("status") != "gotowy" or already_published(post, log):
                    continue
                when = due_at(post)
            except (ValueError, OSError) as exc:
                print(f"  POMIJAM {f.name}: nieczytelny ({exc})")
                continue
            if when <= now_et:
                cands.append((when, f.name, f, post.get("typ")))
        cands.sort(key=lambda c: (c[0], c[1]))
        print(f"Teraz (ET): {now_et:%Y-%m-%d %H:%M}. Kandydaci: {len(cands)}")
        if not cands:
            print("Nic do publikacji.")
            return EXIT_OK

        rc = EXIT_OK
        for kind in ("feed", "story"):
            group = [c for c in cands if (c[3] == "story") == (kind == "story")]
            for _, _, f, _ in group:
                res = self.process(f)
                if res == EXIT_OK:
                    break
                if res == EXIT_BLOCKED:
                    if not self.live:
                        rc = max(rc, EXIT_BLOCKED)
                    continue  # zablokowany nie moze wstrzymac calej kolejki
                rc = EXIT_ERR
                break  # blad API: nie probujemy kolejnego w tym przebiegu
        return rc


# =====================================================================================
#  BLOKADA PRZEBIEGU (Task Scheduler + reczne uruchomienie naraz)
# =====================================================================================
def acquire_lock(paths: Paths) -> bool:
    paths.lock.parent.mkdir(parents=True, exist_ok=True)
    if paths.lock.exists() and time.time() - paths.lock.stat().st_mtime > LOCK_STALE_SEC:
        paths.lock.unlink(missing_ok=True)
    try:
        fd = os.open(paths.lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        return False
    with os.fdopen(fd, "w") as fh:
        fh.write(f"pid={os.getpid()} start={datetime.now().isoformat(timespec='seconds')}\n")
    return True


def release_lock(paths: Paths) -> None:
    paths.lock.unlink(missing_ok=True)


# =====================================================================================
#  CLI
# =====================================================================================
def build_publisher(paths: Paths, live: bool, cfg: dict[str, str]) -> Publisher:
    """Bledy konfiguracji (brak tokenu, hosta) nie wywracaja przebiegu, w ktorym nic nie
    jest do publikacji: zglaszamy je dopiero, gdy jakis post faktycznie ma isc na zywo."""
    settings = Settings.from_env(cfg)
    pub = Publisher(paths=paths, settings=settings, live=live)
    if live:
        try:
            token = cfg.get("IG_ACCESS_TOKEN", "")
            if not token:
                raise RuntimeError(f"Brak IG_ACCESS_TOKEN w {ENV_PATH}")
            if not settings.ig_user_id:
                raise RuntimeError(f"Brak IG_USER_ID w {ENV_PATH}")
            pub.client = GraphClient(token, settings.graph_version)
            from media_host import get_media_host
            pub.media_host = get_media_host(cfg)
            if (cfg.get("SOCIAL_VIDEO_HOST") or "").strip():
                pub.video_host = get_media_host(cfg, kind="video")
        except Exception as exc:  # noqa: BLE001
            pub.config_error = f"BLAD konfiguracji: {exc}"
    return pub


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Publikator Instagrama MindSync (DRY-RUN domyslnie).")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--id", help="id posta (social/queue/<id>.json)")
    g.add_argument("--due", action="store_true", help="publikuj zalegle posty gotowy (1 feed + 1 story)")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", default=True, help="podglad, zero wysylki (domyslnie)")
    mode.add_argument("--live", action="store_true", help="publikacja NA ZYWO")
    ap.add_argument("--now", help=argparse.SUPPRESS)   # testy: 'YYYY-MM-DD HH:MM' w ET
    ap.add_argument("--root", help=argparse.SUPPRESS)  # testy: inny katalog repo
    args = ap.parse_args(argv)

    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:  # noqa: BLE001
        pass

    paths = Paths(Path(args.root).resolve() if args.root else REPO_ROOT)
    live = bool(args.live)
    print(f"TRYB: {'LIVE (publikacja na Instagram!)' if live else 'DRY-RUN (zero wysylki)'}")

    if live and not acquire_lock(paths):
        print(f"Inny przebieg trzyma blokade {paths.lock}; koncze.")
        write_drip_log(paths, live, "-", None, "POMINIETO: blokada innego przebiegu")
        return EXIT_LOCKED
    try:
        pub = build_publisher(paths, live, load_env())
        if args.id:
            try:
                f = find_post_file(paths, args.id)
            except FileNotFoundError as exc:
                print(f"BLAD: {exc}")
                return EXIT_ERR
            return pub.process(f)
        now_et = (datetime.strptime(args.now, "%Y-%m-%d %H:%M").replace(tzinfo=ET)
                  if args.now else datetime.now(ET))
        return pub.run_due(now_et)
    finally:
        if live:
            release_lock(paths)


if __name__ == "__main__":
    sys.exit(main())
