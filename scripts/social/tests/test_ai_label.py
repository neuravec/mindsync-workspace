"""Etykieta AI (AI Act art. 50): wykrywanie obrazu AI, is_ai_generated w publikatorze, XMP w JPEG."""
from __future__ import annotations

import importlib.util
import io
import sys
from pathlib import Path

SOCIAL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOCIAL_DIR))

import social_common as sc  # noqa: E402


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SOCIAL_DIR / filename)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


igp = _load("ig_publish_ai", "ig-publish.py")

AI_SLAJD = {"szablon": "bold-cover", "pola": {"obraz": "social/assets/variant-c/c08c.jpg", "tytul": "x"}}
EKRAN_SLAJD = {"szablon": "aggro-split", "pola": {"ekran": "social/images/app-shots/threads_list.png"}}
TYPO_SLAJD = {"szablon": "bold-myth", "pola": {"mit": "a", "fakt": "b"}}


def test_slajd_ai_wykrywa_obraz_ai_ale_nie_zrzut_ekranu():
    assert sc.slajd_ai(AI_SLAJD) is True
    assert sc.slajd_ai(EKRAN_SLAJD) is False
    assert sc.slajd_ai(TYPO_SLAJD) is False
    assert sc.slajd_ai(dict(TYPO_SLAJD, ai_label=True)) is True
    assert sc.slajd_ai(dict(AI_SLAJD, ai_label=False)) is False


def test_is_ai_generated_tylko_na_kontenerze_glownym():
    post = {"typ": "carousel", "slajdy": [AI_SLAJD, TYPO_SLAJD], "caption": "c", "hashtagi": [], "alt_text": []}
    children, parent = igp.container_requests(post, ["u1", "u2"], send_alt=False)
    assert parent.get("is_ai_generated") == "true"
    assert all("is_ai_generated" not in c for c in children)


def test_brak_is_ai_generated_dla_prawdziwych_ekranow():
    post = {"typ": "single", "slajdy": [EKRAN_SLAJD], "caption": "c", "hashtagi": [], "alt_text": []}
    _, parent = igp.container_requests(post, ["u1"], send_alt=False)
    assert "is_ai_generated" not in parent


def test_xmp_digital_source_type_w_jpeg(tmp_path):
    from PIL import Image
    render = _load("render_ai", "render.py")
    p = tmp_path / "a.jpg"
    Image.new("RGB", (16, 16), (10, 20, 30)).save(p, "JPEG")
    assert render.dopisz_xmp_ai(str(p)) is True
    data = p.read_bytes()
    assert sc.AI_XMP_SOURCE.encode() in data
    assert render.dopisz_xmp_ai(str(p)) is False  # idempotencja: drugi raz nie dopisuje
    Image.open(io.BytesIO(data)).load()  # plik nadal poprawny
