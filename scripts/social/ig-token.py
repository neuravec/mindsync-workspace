"""Token Instagrama (Instagram API with Instagram Login): status, odswiezanie, kontrola.

Long-lived token zyje 60 dni. Odswiezenie (GET graph.instagram.com/refresh_access_token,
grant_type=ig_refresh_token) daje nowe 60 dni, ale tylko gdy token ma >= 24 h i jest wciaz
wazny. Wygasly token jest NIE DO ODZYSKANIA: trzeba przejsc logowanie od nowa w aplikacji
Meta. Dlatego drip woła `check` co przebieg i odswieza z wyprzedzeniem.

Komendy:
    python scripts/social/ig-token.py status
    python scripts/social/ig-token.py refresh [--dry-run] [--force]
    python scripts/social/ig-token.py check [--warn-days 10] [--auto-refresh-below 20]
    python scripts/social/ig-token.py whoami

Zapis: IG_ACCESS_TOKEN, IG_TOKEN_EXPIRES_AT (ISO UTC) i IG_TOKEN_REFRESHED_AT trafiaja do
scripts/social/.env (zapis atomowy, reszta pliku nietknieta). Token nigdy nie jest wypisywany.

Kody wyjscia `check`: 0 = ok, 2 = wygasa za < warn-days albo data nieznana/wygasl,
1 = blad (np. odswiezenie padlo).
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ig_common import (  # noqa: E402
    DEFAULT_GRAPH_VERSION, ENV_PATH, GraphClient, IgApiError, load_env, update_env_file,
)

MIN_AGE_FOR_REFRESH = timedelta(hours=24)


def parse_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def days_left(cfg: dict[str, str], now: datetime) -> float | None:
    exp = parse_iso(cfg.get("IG_TOKEN_EXPIRES_AT"))
    if exp is None:
        return None
    return (exp - now).total_seconds() / 86400


def cmd_status(cfg: dict[str, str], now: datetime) -> int:
    if not cfg.get("IG_ACCESS_TOKEN"):
        print(f"Brak IG_ACCESS_TOKEN w {ENV_PATH}")
        return 2
    d = days_left(cfg, now)
    if d is None:
        print("Token jest, ale IG_TOKEN_EXPIRES_AT nieznane. Uruchom `ig-token.py refresh`, "
              "zeby ustalic date wygasniecia (albo wpisz ja recznie z panelu Meta).")
        return 0
    print(f"Token wygasa {cfg['IG_TOKEN_EXPIRES_AT']} (za {d:.1f} dni).")
    refreshed = cfg.get("IG_TOKEN_REFRESHED_AT")
    if refreshed:
        print(f"Ostatnie odswiezenie: {refreshed}")
    if d <= 0:
        print("WYGASL. Nie da sie go odswiezyc: wygeneruj nowy token w aplikacji Meta.")
    return 0


def cmd_refresh(cfg: dict[str, str], now: datetime, *, dry_run: bool, force: bool,
                client_factory: Callable[[str], GraphClient], env_path: Path) -> int:
    token = cfg.get("IG_ACCESS_TOKEN")
    if not token:
        print(f"Brak IG_ACCESS_TOKEN w {env_path}")
        return 1
    d = days_left(cfg, now)
    if d is not None and d <= 0:
        print("Token juz wygasl; odswiezenie niemozliwe. Wygeneruj nowy w aplikacji Meta.")
        return 1
    refreshed = parse_iso(cfg.get("IG_TOKEN_REFRESHED_AT"))
    if refreshed and now - refreshed < MIN_AGE_FOR_REFRESH and not force:
        print(f"Token odswiezony {refreshed.isoformat()} (< 24 h temu); Meta i tak by odmowila. Pomijam.")
        return 0
    if dry_run:
        print("DRY-RUN: GET https://graph.instagram.com/refresh_access_token "
              "grant_type=ig_refresh_token access_token=<REDACTED>; zapis do .env pominiety.")
        return 0
    client = client_factory(token)
    try:
        res = client.request("GET", "refresh_access_token", {"grant_type": "ig_refresh_token"},
                             versioned=False)
    except IgApiError as exc:
        print(f"BLAD odswiezenia: {exc}")
        return 1
    new_token = res.get("access_token")
    expires_in = int(res.get("expires_in") or 0)
    if not new_token or expires_in <= 0:
        print("BLAD: odpowiedz bez access_token/expires_in")
        return 1
    exp = (now + timedelta(seconds=expires_in)).astimezone(timezone.utc)
    update_env_file({
        "IG_ACCESS_TOKEN": new_token,
        "IG_TOKEN_EXPIRES_AT": exp.isoformat(timespec="seconds"),
        "IG_TOKEN_REFRESHED_AT": now.astimezone(timezone.utc).isoformat(timespec="seconds"),
    }, env_path)
    print(f"OK: token odswiezony, wygasa {exp.isoformat(timespec='seconds')} "
          f"(za {expires_in / 86400:.1f} dni). Zapisano do {env_path}.")
    return 0


def cmd_check(cfg: dict[str, str], now: datetime, *, warn_days: float, auto_below: float | None,
              client_factory: Callable[[str], GraphClient], env_path: Path) -> int:
    if not cfg.get("IG_ACCESS_TOKEN"):
        print("UWAGA: brak IG_ACCESS_TOKEN")
        return 2
    d = days_left(cfg, now)
    if auto_below is not None and (d is None or 0 < d < auto_below):
        print(f"Auto-odswiezenie (pozostalo: {'?' if d is None else f'{d:.1f}'} dni, prog {auto_below}).")
        rc = cmd_refresh(cfg, now, dry_run=False, force=False, client_factory=client_factory,
                         env_path=env_path)
        if rc != 0:
            return 1
        cfg = load_env(env_path)
        d = days_left(cfg, now)
    if d is None:
        print("UWAGA: IG_TOKEN_EXPIRES_AT nieznane")
        return 2
    if d <= 0:
        print("UWAGA: token WYGASL. Wygeneruj nowy w aplikacji Meta.")
        return 2
    if d < warn_days:
        print(f"UWAGA: token wygasa za {d:.1f} dni (< {warn_days}). Uruchom `ig-token.py refresh`.")
        return 2
    print(f"OK: token wazny jeszcze {d:.1f} dni.")
    return 0


def cmd_whoami(cfg: dict[str, str], client_factory: Callable[[str], GraphClient]) -> int:
    token = cfg.get("IG_ACCESS_TOKEN")
    if not token:
        print("Brak IG_ACCESS_TOKEN")
        return 1
    try:
        res = client_factory(token).request("GET", "me", {"fields": "user_id,username"})
    except IgApiError as exc:
        print(f"BLAD: {exc}")
        return 1
    print(f"username={res.get('username')} user_id={res.get('user_id')} (id={res.get('id')})")
    if cfg.get("IG_USER_ID") and res.get("user_id") and str(res["user_id"]) != cfg["IG_USER_ID"]:
        print(f"UWAGA: IG_USER_ID w .env ({cfg['IG_USER_ID']}) != user_id z API ({res['user_id']})")
        return 2
    return 0


def main(argv: list[str] | None = None, *, env_path: Path = ENV_PATH,
         now: datetime | None = None, client_factory: Callable[[str], GraphClient] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Token Instagrama MindSync.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    r = sub.add_parser("refresh")
    r.add_argument("--dry-run", action="store_true")
    r.add_argument("--force", action="store_true", help="pomin kontrole 24 h od poprzedniego odswiezenia")
    c = sub.add_parser("check")
    c.add_argument("--warn-days", type=float, default=10)
    c.add_argument("--auto-refresh-below", type=float, default=None)
    sub.add_parser("whoami")
    args = ap.parse_args(argv)

    cfg = load_env(env_path)
    now = now or datetime.now(timezone.utc)
    version = cfg.get("IG_GRAPH_VERSION") or DEFAULT_GRAPH_VERSION
    factory = client_factory or (lambda tok: GraphClient(tok, version))

    if args.cmd == "status":
        return cmd_status(cfg, now)
    if args.cmd == "refresh":
        return cmd_refresh(cfg, now, dry_run=args.dry_run, force=args.force,
                           client_factory=factory, env_path=env_path)
    if args.cmd == "check":
        return cmd_check(cfg, now, warn_days=args.warn_days, auto_below=args.auto_refresh_below,
                         client_factory=factory, env_path=env_path)
    return cmd_whoami(cfg, factory)


if __name__ == "__main__":
    sys.exit(main())
