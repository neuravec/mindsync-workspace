"""Testy publikatora Instagrama (offline: requests zmockowany, zero sieci).

Uruchom:  python -m pytest scripts/social/tests/test_ig_publish.py -q
"""

from __future__ import annotations

import importlib.util
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
import requests

SOCIAL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOCIAL_DIR))


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SOCIAL_DIR / filename)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


igp = _load("ig_publish", "ig-publish.py")
igt = _load("ig_token", "ig-token.py")
import ig_common  # noqa: E402

JPEG = b"\xff\xd8\xff\xe0" + b"\x00" * 64
BASE = "https://graph.instagram.com/v23.0"


# =====================================================================================
#  ATRAPY
# =====================================================================================
class FakeResponse:
    def __init__(self, status: int = 200, body: dict | None = None, headers: dict | None = None):
        self.status_code = status
        self._body = body if body is not None else {}
        self.headers = headers or {}
        self.text = json.dumps(self._body)

    def json(self):
        return self._body


class FakeSession:
    """Router: handler(method, url, params) -> FakeResponse. Zapisuje kazde wywolanie."""

    def __init__(self, handler):
        self.handler = handler
        self.calls: list[tuple[str, str, dict]] = []

    def request(self, method, url, params=None, data=None, timeout=None, **kw):
        payload = dict(params or data or {})
        self.calls.append((method, url, payload))
        return self.handler(method, url, payload)


class FakeHost:
    name = "fake"

    def __init__(self):
        self.uploaded: list[tuple[str, str]] = []
        self.verified: list[str] = []

    def upload(self, path, public_id):
        self.uploaded.append((path.name, public_id))
        ext = ".mp4" if path.suffix.lower() == ".mp4" else ".jpg"
        return f"https://cdn.example/{public_id}{ext}"

    def verify(self, url, kind=None):
        self.verified.append((url, kind) if kind == "video" else url)


class GraphScript:
    """Domyslny scenariusz udanej publikacji; poszczegolne testy nadpisuja odpowiedzi."""

    def __init__(self, status_seq=None, publish_responses=None):
        self.n = 0
        self.status_seq = status_seq or {}
        self.publish_responses = list(publish_responses or [])

    def __call__(self, method, url, p):
        path = url.replace(BASE + "/", "")
        if path.endswith("content_publishing_limit"):
            return FakeResponse(body={"data": [{"quota_usage": 3, "config": {"quota_total": 100}}]})
        if method == "POST" and path.endswith("/media"):
            self.n += 1
            return FakeResponse(body={"id": f"c{self.n}"})
        if method == "POST" and path.endswith("/media_publish"):
            if self.publish_responses:
                return self.publish_responses.pop(0)
            return FakeResponse(body={"id": "M1"})
        if method == "GET" and p.get("fields", "").startswith("status_code"):
            seq = self.status_seq.get(path)
            code = seq.pop(0) if seq else "FINISHED"
            return FakeResponse(body={"status_code": code, "status": f"{code}: test"})
        if method == "GET" and p.get("fields") == "permalink":
            return FakeResponse(body={"permalink": "https://www.instagram.com/p/XYZ/"})
        if method == "GET" and path.endswith("/media"):
            return FakeResponse(body={"data": [{"id": "M-REC"}]})
        return FakeResponse(404, {"error": {"message": f"unexpected {method} {path}", "code": 100}})


# =====================================================================================
#  FIXTURES
# =====================================================================================
@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("prawdziwe wywolanie sieciowe w tescie")
    monkeypatch.setattr(requests.Session, "request", boom)
    monkeypatch.setattr(requests.Session, "head", boom)
    monkeypatch.setattr(requests, "request", boom)


@pytest.fixture
def root(tmp_path):
    (tmp_path / "social" / "queue").mkdir(parents=True)
    return tmp_path


def make_post(root: Path, pid: str, typ: str, n_media: int, *, status="gotowy",
              date="2026-10-05", hour="09:00", publikacja=None) -> Path:
    media = []
    for i in range(1, n_media + 1):
        rel = f"social/media/{pid}/{i:02d}.jpg"
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(JPEG)
        media.append(rel)
    post = {
        "id": pid, "platforma": "instagram", "typ": typ, "status": status,
        "planowana_data": date, "planowana_godzina_et": hour, "glos": "monika-v1",
        "temat": "t", "zrodlo": "z", "kryzysowy": False, "slajdy": [],
        "caption": "Small steps count.", "hashtagi": ["#therapy", "mentalhealth"],
        "alt_text": [f"alt {i}" for i in range(1, n_media + 1)], "media": media,
        "publikacja": publikacja or {"ig_container_id": None, "ig_media_id": None,
                                     "permalink": None, "opublikowano": None},
    }
    path = root / "social" / "queue" / f"{pid}.json"
    path.write_text(json.dumps(post, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def make_publisher(root: Path, handler, *, live=True, gate_ok=True, max_retry=3):
    session = FakeSession(handler)
    client = ig_common.GraphClient("SECRET-TOKEN", "v23.0", session=session,
                                   max_retry=max_retry, sleep=lambda s: None, log=lambda m: None)
    gate_calls = []

    def gate(paths, pid):
        gate_calls.append(pid)
        return (gate_ok, "gate: test")

    pub = igp.Publisher(
        paths=igp.Paths(root),
        settings=igp.Settings(ig_user_id="IGU", poll_interval=0, poll_max_sec=10,
                              media_host_name="fake"),
        live=live, client=client, media_host=FakeHost(), gate=gate, sleep=lambda s: None,
    )
    pub.gate_calls = gate_calls
    return pub, session


def posts_to(session, suffix):
    return [c for c in session.calls if c[0] == "POST" and c[1].endswith(suffix)]


# =====================================================================================
#  TESTY PUBLIKACJI
# =====================================================================================
def test_single_happy_path(root):
    f = make_post(root, "2026-10-05-single", "single", 1)
    pub, session = make_publisher(root, GraphScript())
    assert pub.process(f) == 0

    creates = posts_to(session, "/IGU/media")
    assert len(creates) == 1
    params = creates[0][2]
    assert params["image_url"] == "https://cdn.example/2026-10-05-single/01.jpg"
    assert params["caption"] == "Small steps count.\n\n#therapy #mentalhealth"
    assert params["alt_text"] == "alt 1"
    assert "media_type" not in params
    assert posts_to(session, "/media_publish")[0][2]["creation_id"] == "c1"

    post = json.loads(f.read_text(encoding="utf-8"))
    assert post["status"] == "opublikowany"
    assert post["publikacja"]["ig_media_id"] == "M1"
    assert post["publikacja"]["ig_container_id"] == "c1"
    assert post["publikacja"]["permalink"] == "https://www.instagram.com/p/XYZ/"
    assert list(post.keys())[0] == "id"  # kolejnosc kluczy zachowana
    log = json.loads((root / "social" / "published-log.json").read_text(encoding="utf-8"))
    assert log[0]["id"] == "2026-10-05-single" and log[0]["ig_media_id"] == "M1"
    drip = (root / "social" / "_drip-log.txt").read_text(encoding="utf-8")
    assert "LIVE | id=2026-10-05-single | media_id=M1 | OK opublikowano" in drip
    assert "SECRET-TOKEN" not in drip


def test_carousel_children_in_order(root):
    f = make_post(root, "2026-10-05-carousel", "carousel", 3)
    pub, session = make_publisher(root, GraphScript())
    assert pub.process(f) == 0

    creates = posts_to(session, "/IGU/media")
    assert len(creates) == 4
    for i, (_, _, p) in enumerate(creates[:3], 1):
        assert p["is_carousel_item"] == "true"
        assert p["image_url"].endswith(f"/2026-10-05-carousel/{i:02d}.jpg")
        assert p["alt_text"] == f"alt {i}"
        assert "caption" not in p
    parent = creates[3][2]
    assert parent["media_type"] == "CAROUSEL"
    assert parent["children"] == "c1,c2,c3"
    assert parent["caption"].startswith("Small steps count.")
    # dzieci polled przed utworzeniem rodzica
    order = [c for c in session.calls]
    idx_parent = order.index(creates[3])
    polled = [c[1] for c in order[:idx_parent] if c[0] == "GET" and "status_code" in c[2].get("fields", "")]
    assert [u.rsplit("/", 1)[1] for u in polled] == ["c1", "c2", "c3"]
    assert posts_to(session, "/media_publish")[0][2]["creation_id"] == "c4"


def test_story_no_caption_no_alt(root):
    f = make_post(root, "2026-10-05-story", "story", 1)
    pub, session = make_publisher(root, GraphScript())
    assert pub.process(f) == 0
    p = posts_to(session, "/IGU/media")[0][2]
    assert p == {"media_type": "STORIES", "image_url": "https://cdn.example/2026-10-05-story/01.jpg",
                 "access_token": "SECRET-TOKEN"}


def test_idempotent_by_media_id(root):
    f = make_post(root, "2026-10-05-done", "single", 1,
                  publikacja={"ig_container_id": "c", "ig_media_id": "OLD", "permalink": None,
                              "opublikowano": "x"})
    pub, session = make_publisher(root, GraphScript())
    assert pub.process(f) == 0
    assert session.calls == []
    assert pub.gate_calls == []


def test_idempotent_by_published_log(root):
    f = make_post(root, "2026-10-05-logged", "single", 1)
    (root / "social" / "published-log.json").write_text(
        json.dumps([{"id": "2026-10-05-logged", "ig_media_id": "OLD"}]), encoding="utf-8")
    pub, session = make_publisher(root, GraphScript())
    assert pub.process(f) == 0
    assert session.calls == []


def test_polling_error_keeps_status(root):
    f = make_post(root, "2026-10-05-err", "single", 1)
    script = GraphScript(status_seq={"c1": ["IN_PROGRESS", "ERROR"]})
    pub, session = make_publisher(root, script)
    assert pub.process(f) == 1
    assert posts_to(session, "/media_publish") == []
    post = json.loads(f.read_text(encoding="utf-8"))
    assert post["status"] == "gotowy" and post["publikacja"]["ig_media_id"] is None
    drip = (root / "social" / "_drip-log.txt").read_text(encoding="utf-8")
    assert "BLAD: Kontener c1: status_code=ERROR" in drip
    assert json.loads((root / "social" / "published-log.json").read_text(encoding="utf-8")) == []


def test_gate_blocks(root):
    f = make_post(root, "2026-10-05-gated", "single", 1)
    pub, session = make_publisher(root, GraphScript(), gate_ok=False)
    assert pub.process(f) == 3
    assert session.calls == []
    assert pub.media_host.uploaded == []
    assert json.loads(f.read_text(encoding="utf-8"))["status"] == "gotowy"


def test_status_not_ready_blocks(root):
    f = make_post(root, "2026-10-05-draft", "single", 1, status="szkic")
    pub, session = make_publisher(root, GraphScript())
    assert pub.process(f) == 3
    assert session.calls == []


def test_quota_exhausted_does_not_publish(root):
    f = make_post(root, "2026-10-05-quota", "single", 1)

    def handler(m, u, p):
        if u.endswith("content_publishing_limit"):
            return FakeResponse(body={"data": [{"quota_usage": 100, "config": {"quota_total": 100}}]})
        raise AssertionError("nie powinno dojsc dalej")
    pub, session = make_publisher(root, handler)
    assert pub.process(f) == 1
    assert pub.media_host.uploaded == []


def test_media_publish_recovers_when_container_already_published(root):
    f = make_post(root, "2026-10-05-rec", "single", 1)
    script = GraphScript(status_seq={"c1": ["FINISHED", "PUBLISHED"]},
                         publish_responses=[FakeResponse(500, {"error": {"message": "boom", "code": 2}})])
    pub, session = make_publisher(root, script)
    assert pub.process(f) == 0
    assert len(posts_to(session, "/media_publish")) == 1  # brak drugiej publikacji
    assert json.loads(f.read_text(encoding="utf-8"))["publikacja"]["ig_media_id"] == "M-REC"


# =====================================================================================
#  RETRY KLIENTA
# =====================================================================================
def test_retry_on_429_then_success():
    seq = [FakeResponse(429, {"error": {"message": "Application request limit reached", "code": 4}},
                        {"Retry-After": "1"}),
           FakeResponse(200, {"id": "ok"})]
    session = FakeSession(lambda m, u, p: seq.pop(0))
    sleeps = []
    c = ig_common.GraphClient("T", "v23.0", session=session, sleep=sleeps.append, log=lambda m: None)
    assert c.request("POST", "IGU/media", {"image_url": "x"}) == {"id": "ok"}
    assert len(session.calls) == 2 and len(sleeps) == 1 and sleeps[0] >= 1


def test_retry_on_network_error():
    state = {"n": 0}

    def handler(m, u, p):
        state["n"] += 1
        if state["n"] == 1:
            raise requests.ConnectionError("reset")
        return FakeResponse(200, {"id": "ok"})
    c = ig_common.GraphClient("T", session=FakeSession(handler), sleep=lambda s: None, log=lambda m: None)
    assert c.request("GET", "me")["id"] == "ok"


def test_no_retry_on_400_and_readable_message():
    session = FakeSession(lambda m, u, p: FakeResponse(400, {"error": {
        "message": "Invalid parameter", "code": 100, "error_subcode": 2207052,
        "error_user_msg": "The media could not be fetched from this URI", "fbtrace_id": "AbC"}}))
    c = ig_common.GraphClient("T", session=session, sleep=lambda s: None, log=lambda m: None)
    with pytest.raises(ig_common.IgApiError) as ei:
        c.request("POST", "IGU/media", {"image_url": "x"})
    assert len(session.calls) == 1
    msg = str(ei.value)
    assert "Invalid parameter" in msg and "subcode=2207052" in msg and "could not be fetched" in msg


# =====================================================================================
#  DRIP --due
# =====================================================================================
def test_due_publishes_oldest_feed_and_one_story(root):
    make_post(root, "2026-10-04-old", "carousel", 2, date="2026-10-04", hour="09:00")
    make_post(root, "2026-10-05-new", "single", 1, date="2026-10-05", hour="08:00")
    make_post(root, "2026-10-05-story", "story", 1, date="2026-10-05", hour="08:30")
    make_post(root, "2026-10-09-future", "single", 1, date="2026-10-09", hour="08:00")
    pub, session = make_publisher(root, GraphScript())
    now = datetime(2026, 10, 5, 10, 0, tzinfo=igp.ET)
    assert pub.run_due(now) == 0
    q = root / "social" / "queue"
    st = {p.stem: json.loads(p.read_text(encoding="utf-8"))["status"] for p in q.glob("*.json")}
    assert st == {"2026-10-04-old": "opublikowany", "2026-10-05-new": "gotowy",
                  "2026-10-05-story": "opublikowany", "2026-10-09-future": "gotowy"}


def test_due_skips_underscore_and_blocked_tries_next(root):
    make_post(root, "_przyklad", "single", 1, date="2026-10-01")
    make_post(root, "2026-10-04-a", "single", 1, date="2026-10-04")
    make_post(root, "2026-10-04-b", "single", 1, date="2026-10-04", hour="10:00")
    pub, session = make_publisher(root, GraphScript())
    pub.gate = lambda paths, pid: (pid != "2026-10-04-a", "")
    assert pub.run_due(datetime(2026, 10, 5, 10, 0, tzinfo=igp.ET)) == 0
    q = root / "social" / "queue"
    assert json.loads((q / "2026-10-04-a.json").read_text(encoding="utf-8"))["status"] == "gotowy"
    assert json.loads((q / "2026-10-04-b.json").read_text(encoding="utf-8"))["status"] == "opublikowany"
    assert json.loads((q / "_przyklad.json").read_text(encoding="utf-8"))["status"] == "gotowy"


def test_due_respects_eastern_time(root):
    make_post(root, "2026-10-05-x", "single", 1, date="2026-10-05", hour="09:00")
    pub, session = make_publisher(root, GraphScript())
    # 14:30 Warszawa = 08:30 ET (CEST/EDT): jeszcze nie
    now = datetime(2026, 10, 5, 12, 30, tzinfo=timezone.utc).astimezone(igp.ET)
    assert pub.run_due(now) == 0 and session.calls == []


# =====================================================================================
#  CLI: dry-run bez sieci, brak bramki
# =====================================================================================
def _write_gate(root: Path, code: int):
    g = root / "scripts" / "social" / "social-gate.py"
    g.parent.mkdir(parents=True, exist_ok=True)
    g.write_text(f"import sys\nprint('gate ran', sys.argv[1:])\nsys.exit({code})\n", encoding="utf-8")


def test_cli_dry_run_no_network(root, capsys, monkeypatch):
    monkeypatch.setattr(igp, "load_env", lambda: {"IG_USER_ID": "IGU", "SOCIAL_MEDIA_HOST": "cloudinary",
                                                  "IG_ACCESS_TOKEN": "SECRET-TOKEN"})
    make_post(root, "2026-10-05-c", "carousel", 2)
    _write_gate(root, 0)
    rc = igp.main(["--id", "2026-10-05-c", "--root", str(root)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "DRY-RUN" in out and "media_type" in out and "CAROUSEL" in out
    assert "/IGU/media_publish" in out and "gate ran" in out
    assert "SECRET-TOKEN" not in out
    post = json.loads((root / "social" / "queue" / "2026-10-05-c.json").read_text(encoding="utf-8"))
    assert post["status"] == "gotowy"


def test_cli_dry_run_reports_blockers(root, capsys, monkeypatch):
    monkeypatch.setattr(igp, "load_env", lambda: {})
    make_post(root, "2026-10-05-s", "single", 1, status="szkic")
    _write_gate(root, 1)
    rc = igp.main(["--id", "2026-10-05-s", "--root", str(root)])
    out = capsys.readouterr().out
    assert rc == 3 and "status='szkic'" in out and "bramka social-gate.py" in out


def test_cli_live_without_gate_is_blocked(root, capsys, monkeypatch):
    monkeypatch.setattr(igp, "load_env", lambda: {})
    make_post(root, "2026-10-05-ng", "single", 1)
    rc = igp.main(["--id", "2026-10-05-ng", "--root", str(root), "--live"])
    out = capsys.readouterr().out
    assert rc == 3 and "Brak bramki" in out
    assert not (root / "social" / ".ig-publish.lock").exists()


def test_cli_due_live_nothing_due_without_config_is_ok(root, monkeypatch):
    monkeypatch.setattr(igp, "load_env", lambda: {})
    assert igp.main(["--due", "--live", "--root", str(root), "--now", "2026-10-05 10:00"]) == 0


def test_validation_rejects_non_jpeg_and_bad_carousel(root):
    f = make_post(root, "2026-10-05-bad", "carousel", 1)
    post = json.loads(f.read_text(encoding="utf-8"))
    (root / post["media"][0]).write_bytes(b"\x89PNG....")
    problems, _ = igp.validate_post(post, igp.Paths(root))
    assert any("JPEG" in p for p in problems) and any("2-10" in p for p in problems)


# =====================================================================================
#  TOKEN
# =====================================================================================
def test_token_refresh_writes_env(tmp_path):
    env = tmp_path / ".env"
    env.write_text("# komentarz\nIG_ACCESS_TOKEN=old\nIG_USER_ID=1\nIG_TOKEN_EXPIRES_AT=2026-10-20T00:00:00+00:00\n",
                   encoding="utf-8")
    now = datetime(2026, 10, 1, 12, 0, tzinfo=timezone.utc)
    session = FakeSession(lambda m, u, p: FakeResponse(200, {"access_token": "new", "token_type": "bearer",
                                                             "expires_in": 5184000}))

    def factory(tok):
        return ig_common.GraphClient(tok, session=session, sleep=lambda s: None, log=lambda m: None)
    assert igt.main(["refresh"], env_path=env, now=now, client_factory=factory) == 0
    assert session.calls[0][1] == "https://graph.instagram.com/refresh_access_token"
    assert session.calls[0][2]["grant_type"] == "ig_refresh_token"
    cfg = ig_common.parse_env_text(env.read_text(encoding="utf-8"))
    assert cfg["IG_ACCESS_TOKEN"] == "new" and cfg["IG_USER_ID"] == "1"
    assert cfg["IG_TOKEN_EXPIRES_AT"] == (now + timedelta(days=60)).isoformat(timespec="seconds")
    assert env.read_text(encoding="utf-8").startswith("# komentarz")


def test_token_check_exit_codes(tmp_path, monkeypatch):
    for k in list(__import__("os").environ):
        if k.startswith("IG_"):
            monkeypatch.delenv(k)
    env = tmp_path / ".env"
    now = datetime(2026, 10, 1, tzinfo=timezone.utc)
    env.write_text("IG_ACCESS_TOKEN=t\nIG_TOKEN_EXPIRES_AT=2026-10-06T00:00:00+00:00\n", encoding="utf-8")
    assert igt.main(["check"], env_path=env, now=now) == 2
    env.write_text("IG_ACCESS_TOKEN=t\nIG_TOKEN_EXPIRES_AT=2026-11-20T00:00:00+00:00\n", encoding="utf-8")
    assert igt.main(["check"], env_path=env, now=now) == 0


def test_token_refresh_skipped_within_24h(tmp_path):
    env = tmp_path / ".env"
    env.write_text("IG_ACCESS_TOKEN=t\nIG_TOKEN_REFRESHED_AT=2026-10-01T06:00:00+00:00\n", encoding="utf-8")
    now = datetime(2026, 10, 1, 12, 0, tzinfo=timezone.utc)

    def factory(tok):
        raise AssertionError("nie powinno wolac API")
    assert igt.main(["refresh"], env_path=env, now=now, client_factory=factory) == 0


# =====================================================================================
#  HOSTING MEDIOW (media_host.py)
# =====================================================================================
import media_host  # noqa: E402


class HostSession:
    def __init__(self, handler):
        self.handler = handler
        self.calls = []

    def head(self, url, **kw):
        self.calls.append(("HEAD", url, kw))
        return self.handler("HEAD", url, kw)

    def post(self, url, **kw):
        self.calls.append(("POST", url, kw))
        return self.handler("POST", url, kw)

    def request(self, method, url, **kw):
        self.calls.append((method, url, kw))
        return self.handler(method, url, kw)


def test_verify_head_requires_jpeg():
    ok = HostSession(lambda m, u, k: FakeResponse(200, {}, {"Content-Type": "image/jpeg"}))
    media_host.MediaHost(session=ok, sleep=lambda s: None).verify("https://x/a.jpg")
    bad = HostSession(lambda m, u, k: FakeResponse(200, {}, {"Content-Type": "image/png"}))
    with pytest.raises(media_host.MediaHostError):
        media_host.MediaHost(session=bad, sleep=lambda s: None).verify("https://x/a.png")


def test_cloudinary_signed_upload(tmp_path):
    f = tmp_path / "01.jpg"
    f.write_bytes(JPEG)
    s = HostSession(lambda m, u, k: FakeResponse(200, {"secure_url": "https://res.cloudinary.com/x/a.jpg",
                                                      "format": "jpg"}))
    h = media_host.CloudinaryHost({"CLOUDINARY_CLOUD_NAME": "demo", "CLOUDINARY_API_KEY": "k",
                                   "CLOUDINARY_API_SECRET": "s"}, session=s)
    assert h.upload(f, "post/01") == "https://res.cloudinary.com/x/a.jpg"
    method, url, kw = s.calls[0]
    assert url == "https://api.cloudinary.com/v1_1/demo/image/upload"
    assert kw["data"]["public_id"] == "post/01" and kw["data"]["signature"] and "s" not in kw["data"].values()


def test_webflow_two_step_upload(tmp_path):
    f = tmp_path / "01.jpg"
    f.write_bytes(JPEG)

    def handler(m, u, k):
        if u.endswith("/sites/SITE/assets"):
            return FakeResponse(200, {"uploadUrl": "https://s3.example/up", "uploadDetails": {"key": "a/b"},
                                      "hostedUrl": "https://cdn.prod.website-files.com/x.jpg", "id": "A1"})
        if u == "https://s3.example/up":
            return FakeResponse(201, {})
        raise AssertionError(u)
    s = HostSession(handler)
    h = media_host.WebflowHost({"WEBFLOW_API_TOKEN": "tok", "WEBFLOW_SITE_ID": "SITE"},
                               webflow_env_path=tmp_path / "none.env", session=s)
    assert h.upload(f, "post/01") == "https://cdn.prod.website-files.com/x.jpg"
    assert s.calls[0][2]["json"]["fileName"] == "post-01.jpg"
    assert s.calls[1][2]["data"] == {"key": "a/b"}


def test_media_host_factory_errors():
    with pytest.raises(media_host.MediaHostError):
        media_host.get_media_host({})
    with pytest.raises(media_host.MediaHostError):
        media_host.get_media_host({"SOCIAL_MEDIA_HOST": "ftp"})


# =====================================================================================
#  ROLKI (typ reel): kontener REELS, host wideo, dlugi polling
# =====================================================================================
MP4 = b"\x00\x00\x00\x18ftypmp42" + b"\x00" * 64


def make_reel(root: Path, pid: str, *, status="gotowy", date="2026-10-05", hour="09:00") -> Path:
    d = root / "social" / "media" / pid
    d.mkdir(parents=True, exist_ok=True)
    (d / "reel.mp4").write_bytes(MP4)
    (d / "cover.jpg").write_bytes(JPEG)
    post = {
        "id": pid, "platforma": "instagram", "typ": "reel", "status": status,
        "planowana_data": date, "planowana_godzina_et": hour, "glos": "monika-v1",
        "temat": "t", "zrodlo": None, "kryzysowy": False, "audio": None, "cover_slajd": 1,
        "slajdy": [], "caption": "One tap for today.", "hashtagi": ["#smallhabits"], "alt_text": [],
        "media": [f"social/media/{pid}/reel.mp4", f"social/media/{pid}/cover.jpg"],
        "publikacja": {"ig_container_id": None, "ig_media_id": None, "permalink": None, "opublikowano": None},
    }
    path = root / "social" / "queue" / f"{pid}.json"
    path.write_text(json.dumps(post, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def test_reel_container_params_and_upload(root):
    f = make_reel(root, "2026-10-05-reel")
    pub, session = make_publisher(root, GraphScript())
    assert pub.process(f) == 0
    creates = posts_to(session, "/IGU/media")
    assert len(creates) == 1
    p = creates[0][2]
    assert p["media_type"] == "REELS"
    assert p["video_url"] == "https://cdn.example/2026-10-05-reel/reel.mp4"
    assert p["cover_url"] == "https://cdn.example/2026-10-05-reel/cover.jpg"
    assert p["share_to_feed"] == "true"
    assert p["caption"] == "One tap for today.\n\n#smallhabits"
    assert "alt_text" not in p and "image_url" not in p
    assert pub.media_host.uploaded == [("reel.mp4", "2026-10-05-reel/reel"), ("cover.jpg", "2026-10-05-reel/cover")]
    assert ("https://cdn.example/2026-10-05-reel/reel.mp4", "video") in pub.media_host.verified
    post = json.loads(f.read_text(encoding="utf-8"))
    assert post["status"] == "opublikowany" and post["publikacja"]["ig_media_id"] == "M1"


def test_reel_uses_separate_video_host(root):
    f = make_reel(root, "2026-10-05-reel2")
    pub, session = make_publisher(root, GraphScript())
    vhost = FakeHost()
    pub.video_host = vhost
    assert pub.process(f) == 0
    assert vhost.uploaded == [("reel.mp4", "2026-10-05-reel2/reel")]
    assert pub.media_host.uploaded == [("cover.jpg", "2026-10-05-reel2/cover")]


def test_reel_long_polling_uses_video_settings(root):
    f = make_reel(root, "2026-10-05-reel3")
    script = GraphScript(status_seq={"c1": ["IN_PROGRESS"] * 6 + ["FINISHED"]})
    pub, session = make_publisher(root, script)
    pub.settings.poll_max_sec = 10          # zwykly limit bylby za krotki
    pub.settings.video_poll_interval = 15
    pub.settings.video_poll_max_sec = 900
    sleeps = []
    pub.sleep = sleeps.append
    assert pub.process(f) == 0
    assert sleeps == [15] * 6


def test_reel_poll_timeout_keeps_status(root):
    f = make_reel(root, "2026-10-05-reel4")
    script = GraphScript(status_seq={"c1": ["IN_PROGRESS"] * 100})
    pub, session = make_publisher(root, script)
    pub.settings.video_poll_interval = 60
    pub.settings.video_poll_max_sec = 120
    assert pub.process(f) == 1
    assert posts_to(session, "/media_publish") == []
    assert json.loads(f.read_text(encoding="utf-8"))["status"] == "gotowy"
    assert "brak FINISHED po 120s" in (root / "social" / "_drip-log.txt").read_text(encoding="utf-8")


def test_reel_validation_requires_mp4_and_cover(root):
    f = make_reel(root, "2026-10-05-reel5")
    post = json.loads(f.read_text(encoding="utf-8"))
    (root / post["media"][0]).write_bytes(JPEG)          # "mp4", ktore nie jest MP4
    problems, _ = igp.validate_post(post, igp.Paths(root))
    assert any("nie jest MP4" in p for p in problems)
    post["media"] = post["media"][:1]
    problems, _ = igp.validate_post(post, igp.Paths(root))
    assert any("2 mediow" in p for p in problems)


def test_reel_settings_from_env():
    s = igp.Settings.from_env({"IG_VIDEO_POLL_MAX_SEC": "600", "SOCIAL_MEDIA_HOST": "webflow",
                               "SOCIAL_VIDEO_HOST": "cloudinary"})
    assert s.video_poll_max_sec == 600 and s.video_poll_interval == 15
    assert s.media_host_name == "webflow" and s.video_host_name == "cloudinary"
    assert igp.Settings.from_env({}).video_poll_max_sec == 900


def test_cli_dry_run_reel(root, capsys, monkeypatch):
    monkeypatch.setattr(igp, "load_env", lambda: {"IG_USER_ID": "IGU", "SOCIAL_MEDIA_HOST": "webflow"})
    make_reel(root, "2026-10-05-reelc")
    _write_gate(root, 0)
    rc = igp.main(["--id", "2026-10-05-reelc", "--root", str(root)])
    out = capsys.readouterr().out
    assert rc == 0
    assert '"media_type": "REELS"' in out and '"share_to_feed": "true"' in out and "cover_url" in out
    assert "video/mp4" in out and "SOCIAL_VIDEO_HOST=cloudinary" in out   # ostrzezenie: webflow bez wideo
    post = json.loads((root / "social" / "queue" / "2026-10-05-reelc.json").read_text(encoding="utf-8"))
    assert post["status"] == "gotowy"


def test_due_counts_reel_as_feed(root):
    make_reel(root, "2026-10-04-reel", date="2026-10-04")
    make_post(root, "2026-10-04-single", "single", 1, date="2026-10-04", hour="10:00")
    pub, session = make_publisher(root, GraphScript())
    assert pub.run_due(datetime(2026, 10, 5, 10, 0, tzinfo=igp.ET)) == 0
    q = root / "social" / "queue"
    assert json.loads((q / "2026-10-04-reel.json").read_text(encoding="utf-8"))["status"] == "opublikowany"
    assert json.loads((q / "2026-10-04-single.json").read_text(encoding="utf-8"))["status"] == "gotowy"


def test_verify_head_video_mp4():
    ok = HostSession(lambda m, u, k: FakeResponse(200, {}, {"Content-Type": "video/mp4"}))
    media_host.MediaHost(session=ok, sleep=lambda s: None).verify("https://x/reel.mp4")
    bad = HostSession(lambda m, u, k: FakeResponse(200, {}, {"Content-Type": "image/jpeg"}))
    with pytest.raises(media_host.MediaHostError):
        media_host.MediaHost(session=bad, sleep=lambda s: None).verify("https://x/reel.mp4")
    with pytest.raises(media_host.MediaHostError):  # jawny kind wygrywa z rozszerzeniem
        media_host.MediaHost(session=ok, sleep=lambda s: None).verify("https://x/a.jpg", "image")


def test_cloudinary_video_upload(tmp_path):
    f = tmp_path / "reel.mp4"
    f.write_bytes(MP4)
    s = HostSession(lambda m, u, k: FakeResponse(200, {"secure_url": "https://res.cloudinary.com/x/reel.mp4",
                                                      "format": "mp4"}))
    h = media_host.CloudinaryHost({"CLOUDINARY_CLOUD_NAME": "demo", "CLOUDINARY_UPLOAD_PRESET": "p"}, session=s)
    assert h.upload(f, "post/reel") == "https://res.cloudinary.com/x/reel.mp4"
    method, url, kw = s.calls[0]
    assert url == "https://api.cloudinary.com/v1_1/demo/video/upload"
    assert kw["files"]["file"][2] == "video/mp4"
    bad = HostSession(lambda m, u, k: FakeResponse(200, {"secure_url": "https://x/a.mov", "format": "mov"}))
    with pytest.raises(media_host.MediaHostError):
        media_host.CloudinaryHost({"CLOUDINARY_CLOUD_NAME": "demo", "CLOUDINARY_UPLOAD_PRESET": "p"},
                                  session=bad).upload(f, "post/reel")


def test_webflow_rejects_video_with_clear_message(tmp_path):
    f = tmp_path / "reel.mp4"
    f.write_bytes(MP4)

    def boom(m, u, k):
        raise AssertionError("zero wywolan sieci")
    s = HostSession(boom)
    h = media_host.WebflowHost({"WEBFLOW_API_TOKEN": "tok", "WEBFLOW_SITE_ID": "SITE"},
                               webflow_env_path=tmp_path / "none.env", session=s)
    with pytest.raises(media_host.MediaHostError) as ei:
        h.upload(f, "post/reel")
    assert "SOCIAL_VIDEO_HOST=cloudinary" in str(ei.value)
    assert s.calls == []


def test_media_host_video_kind_selection():
    cfg = {"SOCIAL_MEDIA_HOST": "webflow", "WEBFLOW_API_TOKEN": "t", "WEBFLOW_SITE_ID": "S",
           "SOCIAL_VIDEO_HOST": "cloudinary", "CLOUDINARY_CLOUD_NAME": "c", "CLOUDINARY_UPLOAD_PRESET": "p"}
    assert media_host.get_media_host(cfg, kind="video").name == "cloudinary"
    assert media_host.get_media_host(cfg).name == "webflow"
    with pytest.raises(media_host.MediaHostError):
        media_host.get_media_host({"SOCIAL_MEDIA_HOST": "webflow"}, kind="video")
