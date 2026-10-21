"""Kontrakt rolek i postow o nowosciach (wariant D) w social_common i social-gate (offline).

Uruchom:  python -m pytest scripts/social/tests/test_reel_feature_contract.py -q
"""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path

import pytest

SOCIAL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOCIAL_DIR))
import social_common as sc  # noqa: E402

_spec = importlib.util.spec_from_file_location("social_gate_t", SOCIAL_DIR / "social-gate.py")
gate = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gate)

EKRAN = "social/images/app/ios-1-ekran.png"   # stabilny plik w repo (zrzut sklepowy)

REEL = {
    "id": "2026-12-01-test-reel", "platforma": "instagram", "typ": "reel", "status": "szkic",
    "planowana_data": "2026-12-01", "planowana_godzina_et": "12:00", "glos": "monika-v1",
    "temat": "test", "zrodlo": {"app_feature": "habit-tracker", "frontend_commit": "3fe6055"},
    "kryzysowy": False, "audio": None, "cover_slajd": 1,
    "slajdy": [
        {"szablon": "reel-text", "scena_sek": 3, "przejscie": "fade",
         "pola": {"tytul": "Your habits, minus the guilt", "akcent": "minus the guilt"}},
        {"szablon": "feature-story", "scena_sek": 3, "przejscie": "slide", "ruch": "zoom-in",
         "pola": {"ekran": EKRAN, "tytul": "One tap for today"}},
        {"szablon": "reel-text", "scena_sek": 3, "pola": {"tytul": "Start with one habit", "tlo": "piasek"}},
    ],
    "caption": "One tap for today. Link in bio.", "hashtagi": ["#smallhabits"], "alt_text": [],
    "media": [], "publikacja": {"ig_container_id": None, "ig_media_id": None, "permalink": None, "opublikowano": None},
}


def check(tmp_path, d):
    p = tmp_path / "post.json"
    p.write_text(json.dumps(d), encoding="utf-8")
    _n, blok, ostrz, _d = gate.sprawdz(str(p), set())
    return blok, ostrz


def test_reel_plan_durations():
    sceny, razem = sc.reel_plan(REEL)
    assert [s[2] for s in sceny] == [3.0, 3.0, 3.0]
    assert razem == pytest.approx(9.0 - 2 * sc.REEL_PRZEJSCIE_SEK)
    d = copy.deepcopy(REEL)
    for s in d["slajdy"]:
        s.pop("przejscie", None)
        s.pop("scena_sek", None)
    assert sc.reel_plan(d)[1] == pytest.approx(3 * sc.REEL_SCENA_DOMYSLNA)  # cut nie skraca


def test_reel_valid_has_no_blockers(tmp_path):
    blok, ostrz = check(tmp_path, REEL)
    assert blok == []


def test_reel_blockers(tmp_path):
    d = copy.deepcopy(REEL)
    d["slajdy"][0]["przejscie"] = "wipe"
    d["slajdy"][1]["ruch"] = "spin"
    d["slajdy"][2]["scena_sek"] = 30
    d["cover_slajd"] = 9
    d["audio"] = "social/assets/nie-ma.mp3"
    blok, _ = check(tmp_path, d)
    txt = " | ".join(blok)
    for frag in ("przejscie", "ruch", "scena_sek", "cover_slajd", "brak pliku audio", "audio_licencja"):
        assert frag in txt, frag


def test_reel_too_short_and_template_outside_type(tmp_path):
    d = copy.deepcopy(REEL)
    d["slajdy"] = d["slajdy"][:2]
    for s in d["slajdy"]:
        s["scena_sek"] = 2
    d["slajdy"][1]["szablon"] = "feature-hero"   # feed, nie 9:16
    blok, _ = check(tmp_path, d)
    txt = " | ".join(blok)
    assert "wymagane 5-90 s" in txt and "niedozwolony dla typu reel" in txt


def test_feature_zoom_and_zrodlo(tmp_path):
    d = copy.deepcopy(REEL)
    d.update({"typ": "carousel", "slajdy": [
        {"szablon": "feature-hero", "pola": {"ekran": EKRAN, "tytul": "New"}},
        {"szablon": "feature-step", "pola": {"ekran": EKRAN, "naglowek": "Step", "zoom_x": "10", "zoom_y": "10"}},
        {"szablon": "feature-step", "pola": {"ekran": EKRAN, "naglowek": "Step",
                                             "zoom_x": "0", "zoom_y": "0", "zoom_w": "5000", "zoom_h": "10"}},
        {"szablon": "bold-cta", "pola": {"tytul": "Go", "akcja": "Link in bio"}}],
        "alt_text": ["a", "b", "c", "d"], "zrodlo": {"app_feature": "", "frontend_commit": "zzz"}})
    for k in ("audio", "cover_slajd"):
        d.pop(k)
    blok, ostrz = check(tmp_path, d)
    txt = " | ".join(blok)
    assert "zoom wymaga wszystkich" in txt
    assert "wychodzi poza zrzut" in txt
    assert "app_feature" in txt
    assert any("nie wyglada na sha" in o for o in ostrz)
    assert any("spoza social/images/app-shots" in o for o in ostrz)


def test_missing_screen_file_is_blocker(tmp_path):
    d = copy.deepcopy(REEL)
    d["slajdy"][1]["pola"]["ekran"] = "social/images/app-shots/nie-ma-takiego.png"
    blok, _ = check(tmp_path, d)
    assert any("brak pliku obrazu `ekran`" in b for b in blok)


def test_problemy_wideo():
    ok = {"vcodec": "h264", "pix_fmt": "yuv420p", "w": 1080, "h": 1920, "fps": 30.0, "czas": 14.2,
          "bajty": 3_000_000, "acodec": "aac", "audio_hz": 48000}
    assert sc.problemy_wideo(ok) == []
    zle = dict(ok, vcodec="hevc", fps=20, czas=4.0, acodec=None, w=720)
    txt = " | ".join(sc.problemy_wideo(zle))
    for frag in ("H.264", "fps", "czas", "audio", "1080x1920"):
        assert frag in txt


def test_example_reel_media_if_rendered():
    """Jesli przyklad rolki jest wyrenderowany, MP4 przechodzi ffprobe (ten sam test co bramka)."""
    d, _ = sc.wczytaj(str(Path(sc.QUEUE) / "_przyklad-reel-feature.json"))
    mp4 = Path(sc.abs_repo(sc.reel_media(d["id"])[0]))
    if not mp4.exists() or not sc.ffmpeg_exe():
        pytest.skip("rolka niewyrenderowana albo brak ffmpeg")
    assert sc.problemy_wideo(sc.sonda_wideo(str(mp4))) == []
