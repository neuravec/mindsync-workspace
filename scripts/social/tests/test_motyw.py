"""Pole posta `motyw` (jasna wersja szablonow wariantu D i bold-cta), offline.

Pilnuje trzech rzeczy: domyslny motyw nie zmienia odcisku ani HTML zadnego istniejacego posta,
`jasny` dokleja klase tylko w szablonach, ktore maja jasna wersje, a bramka lapie zla wartosc.

Uruchom:  python -m pytest scripts/social/tests/test_motyw.py -q
"""

from __future__ import annotations

import copy
import importlib.util
import json
import re
import sys
from pathlib import Path

SOCIAL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOCIAL_DIR))
import social_common as sc  # noqa: E402


def _modul(nazwa, plik):
    spec = importlib.util.spec_from_file_location(nazwa, SOCIAL_DIR / plik)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


gate = _modul("social_gate_motyw_t", "social-gate.py")
render = _modul("render_motyw_t", "render.py")

CTA = {"szablon": "bold-cta", "pola": {"tytul": "Walk into therapy prepared", "akcent": "prepared",
                                       "tekst": "Download MindSync.", "akcja": "Link in bio"}}
POST = {
    "id": "2026-12-02-test-motyw", "platforma": "instagram", "typ": "carousel", "status": "szkic",
    "planowana_data": "2026-12-02", "planowana_godzina_et": "12:00", "glos": "monika-v1",
    "temat": "test", "zrodlo": None, "kryzysowy": False,
    "slajdy": [
        {"szablon": "cover", "pola": {"tytul": "A calm test cover"}},
        CTA,
    ],
    "caption": "Test. Link in bio.", "hashtagi": ["#therapytips"],
    "alt_text": ["Slide 1 of 2.", "Slide 2 of 2."], "media": [],
    "publikacja": {"ig_container_id": None, "ig_media_id": None, "permalink": None, "opublikowano": None},
}


def _klasa_body(html_doc):
    m = re.search(r'<body class="([^"]*)"', html_doc)
    assert m, "szablon bez <body class=...>"
    return m.group(1).split()


def check(tmp_path, d):
    p = tmp_path / "post.json"
    p.write_text(json.dumps(d), encoding="utf-8")
    _n, blok, ostrz, _d = gate.sprawdz(str(p), set())
    return blok, ostrz


def test_domyslny_motyw_nie_zmienia_odcisku():
    bez = copy.deepcopy(POST)
    ciemny = dict(copy.deepcopy(POST), motyw="ciemny")
    pusty = dict(copy.deepcopy(POST), motyw="")
    assert sc.hash_slajdow(bez) == sc.hash_slajdow(ciemny) == sc.hash_slajdow(pusty)
    # zmiana motywu zmienia grafiki, wiec bramka musi uznac stare media za nieaktualne
    assert sc.hash_slajdow(dict(copy.deepcopy(POST), motyw="jasny")) != sc.hash_slajdow(bez)


def test_klasa_tylko_w_szablonach_z_jasna_wersja():
    for sz in sc.MOTYW_SZABLONY:
        assert sc.klasa_motywu(sz, "jasny") == "motyw-jasny"
        assert sc.klasa_motywu(sz, "ciemny") == ""
        assert sc.klasa_motywu(sz, None) == ""
    assert sc.klasa_motywu("cover", "jasny") == ""
    assert sc.klasa_motywu("bold-cta", "neon") == ""


def test_szablony_z_motywem_maja_placeholder_i_arkusz():
    for sz in sc.MOTYW_SZABLONY:
        tpl = (Path(sc.TEMPLATES) / (sz + ".html")).read_text(encoding="utf-8")
        assert "{{motyw_klasa}}" in tpl, sz
        assert 'href="motyw-jasny.css"' in tpl, sz
    css = (Path(sc.TEMPLATES) / "motyw-jasny.css").read_text(encoding="utf-8")
    # kazda regula arkusza zawezona do body.motyw-jasny: domyslny wyglad zostaje nietkniety
    selektory = re.findall(r"(?:^|\})\s*([^{}@/][^{}]*)\{", re.sub(r"/\*.*?\*/", "", css, flags=re.S))
    assert selektory
    for grupa in selektory:
        for sel in grupa.split(","):
            assert "motyw-jasny" in sel, sel.strip()


def test_render_dokleja_klase_body():
    logo = "<svg></svg>"
    jasny = render.zbuduj_html("bold-cta", CTA["pola"], 2, 2, "carousel", logo, "jasny")
    assert "motyw-jasny" in _klasa_body(jasny)
    domyslny = render.zbuduj_html("bold-cta", CTA["pola"], 2, 2, "carousel", logo)
    assert "motyw-jasny" not in _klasa_body(domyslny)
    assert "{{" not in domyslny
    # szablon bez jasnej wersji: motyw nie zmienia HTML
    pola = {"tytul": "A calm test cover"}
    assert (render.zbuduj_html("cover", pola, 1, 2, "carousel", logo, "jasny")
            == render.zbuduj_html("cover", pola, 1, 2, "carousel", logo))


def test_bramka_motyw(tmp_path):
    blok, ostrz = check(tmp_path, dict(copy.deepcopy(POST), motyw="neon"))
    assert any("motyw" in b for b in blok)

    blok, ostrz = check(tmp_path, dict(copy.deepcopy(POST), motyw="jasny"))
    assert not any("motyw" in b for b in blok)
    assert not any("spoza kontraktu" in o and "motyw" in o for o in ostrz)
    assert any("motyw `jasny`: slajdy 1 " in o for o in ostrz)   # cover nie ma jasnej wersji

    tylko_cta = dict(copy.deepcopy(POST), motyw="jasny", slajdy=[CTA, CTA], alt_text=["a", "b"])
    blok, ostrz = check(tmp_path, tylko_cta)
    assert not any(o.startswith("motyw") for o in ostrz)
