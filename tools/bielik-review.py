#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recenzent polszczyzny oparty o lokalnego Bielika (Ollama). Tryb "z Bielikiem".

Czyta polski tekst (juz zhumanizowany / de-slopped), pyta Bielika o NATURALNOSC
polszczyzny i zwraca flagi w JSON. NIE przepisuje calego tekstu - tylko ocenia i
wskazuje kalki / nienaturalnosci. Glowny model (Opus) nastepnie naprawia oflagowane
miejsca, trzymajac fakty. To jest "native polskie ucho" jako drugi recenzent.

Uzycie:
  python3 bielik-review.py --file tekst.md
  cat tekst.md | python3 bielik-review.py
  python3 bielik-review.py --check          # tylko sprawdz dostepnosc Ollama + modelu

Zmienne srodowiskowe:
  BIELIK_MODEL  domyslnie "SpeakLeash/bielik-11b-v3.0-instruct:Q4_K_M"
                (lzejszy/szybszy: "SpeakLeash/bielik-4.5b-v3.0-instruct")
  OLLAMA_HOST   domyslnie "http://localhost:11434"

Kody wyjscia: 0 ok, 1 zly input, 2 brak Ollama, 3 brak modelu.
Wymaga tylko biblioteki standardowej (urllib). Zero zaleznosci, zero kosztu, lokalnie.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

MODEL = os.environ.get("BIELIK_MODEL", "SpeakLeash/bielik-11b-v3.0-instruct:Q4_K_M")
HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")

SYSTEM = (
    "Jesteś redaktorem i korektorem języka polskiego z natywnym wyczuciem. Oceniasz, czy tekst "
    "brzmi jak napisany po polsku przez człowieka, czy jak tłumaczenie z angielskiego. NIE "
    "przepisujesz całego tekstu. Wskazujesz konkretne fragmenty, które brzmią nienaturalnie: kalki "
    "składniowe, zdania bez czasownika osobowego, zdania zaczynane przymiotnikiem-orzecznikiem, "
    "leniwe anglicyzmy mające polski odpowiednik, sztuczny szyk. Żargon techniczny i terminy bez "
    "polskiego odpowiednika (judgment, moat, MCP, deploy, tooling, routing layer) ZOSTAWIASZ, tego "
    "nie flagujesz. Odpowiadasz wyłącznie poprawnym JSON, bez komentarza poza JSON."
)

PROMPT_TMPL = (
    "Oceń naturalność polszczyzny w tekście poniżej. Zwróć dokładnie taki JSON:\n"
    '{"ocena": <liczba 1-5>, "werdykt": "naturalny" lub "ok" lub "kalka", '
    '"flagi": [{"fragment": "<dokładny cytat z tekstu>", "problem": "<co brzmi źle>", '
    '"propozycja": "<naturalniej po polsku>"}], "uwagi": "<1-2 zdania ogólnie>"}\n'
    "Zasady: zostaw żargon autora i nazwy własne. Flaguj tylko realne kalki i nienaturalności "
    "(maksymalnie 12 flag). Nie zmieniaj faktów ani liczb.\n\n"
    'TEKST:\n"""\n{text}\n"""'
)


def _post(path, payload, timeout):
    req = urllib.request.Request(
        HOST + path,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def call_bielik(text):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": PROMPT_TMPL.replace("{text}", text)},
        ],
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.2},
    }
    data = _post("/api/chat", payload, timeout=240)
    return data["message"]["content"]


def emit(obj, code):
    print(json.dumps(obj, ensure_ascii=False, indent=2))
    return code


def check():
    try:
        with urllib.request.urlopen(HOST + "/api/tags", timeout=5) as r:
            tags = json.loads(r.read().decode("utf-8"))
    except Exception as e:
        return emit(
            {
                "ok": False,
                "tryb": "z Bielikiem niedostepny -> uzyj trybu bez Bielika",
                "powod": "Ollama nie odpowiada na " + HOST
                + ". Uruchom 'ollama serve' albo zainstaluj: brew install ollama.",
                "blad": str(e),
            },
            2,
        )
    names = [m.get("name", "") for m in tags.get("models", [])]
    base = MODEL.split(":")[0]
    have = any(base in n for n in names)
    return emit(
        {
            "ok": have,
            "model": MODEL,
            "dostepne_modele": names,
            "powod": "" if have else "Brak modelu. Pobierz: ollama pull " + MODEL,
        },
        0 if have else 3,
    )


def main():
    ap = argparse.ArgumentParser(description="Recenzent polszczyzny (Bielik / Ollama)")
    ap.add_argument("--file", help="plik z tekstem; domyslnie czyta ze stdin")
    ap.add_argument("--check", action="store_true", help="sprawdz dostepnosc Ollama + modelu")
    a = ap.parse_args()

    if a.check:
        return check()

    text = open(a.file, encoding="utf-8").read() if a.file else sys.stdin.read()
    if not text.strip():
        return emit({"blad": "pusty input"}, 1)

    try:
        raw = call_bielik(text)
    except urllib.error.URLError as e:
        return emit(
            {
                "ok": False,
                "tryb": "fallback -> bez Bielika",
                "powod": "Nie moge polaczyc z Ollama (" + HOST
                + "). Uruchom 'ollama serve' albo 'brew install ollama'.",
                "blad": str(e),
            },
            2,
        )
    except Exception as e:  # noqa: BLE001
        return emit({"ok": False, "powod": "Blad wywolania Bielika", "blad": str(e)}, 2)

    try:
        parsed = json.loads(raw)
        return emit({"model": MODEL, "recenzja": parsed}, 0)
    except Exception:
        print(raw)  # surowy fallback gdyby model nie oddal czystego JSON
        return 0


if __name__ == "__main__":
    sys.exit(main())
