#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bielik w trybie DORADCY (drugi rzut oka) dla humanizer-pl.

Bierze tekst po przebiegu polszczyzny (recenzent Opus) i KAZE Bielikowi podsunac
konkretne propozycje, gdzie polski mogłby brzmiec naturalniej. Bielik tylko proponuje.
Opus (glowny model) potem osadza kazda propozycje: przyjmuje, odrzuca albo wyluskuje
ziarno - i to on robi finalne poprawki, trzymajac fakty. Bielik 11B bywa, ze zmienia
sens (np. "kuracja" -> "lekarstwo"), wiec NIGDY nie aplikujemy jego zmian wprost.

Uzycie:
  python3 bielik-advisor.py --file tekst.md          # 6 propozycji (domyslnie)
  python3 bielik-advisor.py --file tekst.md --n 8
  cat tekst.md | python3 bielik-advisor.py
  python3 bielik-advisor.py --check                  # dostepnosc Ollama + modelu

Env: BIELIK_MODEL, OLLAMA_HOST (jak w bielik-review.py).
Kody wyjscia: 0 ok, 1 zly input, 2 brak Ollama, 3 brak modelu.
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
    "Jesteś natywnym korektorem polszczyzny. Czytasz cudzy, gotowy tekst i wyłapujesz miejsca, które "
    "brzmią jak tłumaczenie z angielskiego, a nie jak naturalny polski. NIE jesteś autorem: nie "
    "zmieniasz tego, CO tekst mówi, tylko JAK brzmi. Nietknięte zostawiasz: terminy techniczne i "
    "obcojęzyczne, których autor używa świadomie; nazwy własne; tekst w cudzysłowie (cytaty); liczby "
    "i fakty. Twoja jedyna robota to szyk zdania i dobór polskich słów o tym samym znaczeniu. "
    "Odpowiadasz wyłącznie poprawnym JSON."
)

PROMPT_HEAD = (
    "Przeczytaj CAŁY tekst i wskaż TYLKO realne miejsca, gdzie polski brzmi nienaturalnie (najwyżej "
    "{n}, ale może być mniej albo wcale - wtedy zwróć pustą listę, NIE wymyślaj). Dla każdego: "
    "fragment (dokładny cytat), propozycja (ten sam sens, lepsze brzmienie), powod.\n"
    '{"propozycje":[{"fragment":"<cytat>","propozycja":"<naturalniej>","powod":"<dlaczego>"}]}\n\n'
    'TEKST:\n"""\n'
)
PROMPT_TAIL = '\n"""'


def _post(path, payload, timeout):
    req = urllib.request.Request(
        HOST + path,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def call_advisor(text, n):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": PROMPT_HEAD.replace("{n}", str(n)) + text + PROMPT_TAIL},
        ],
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.4},
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
                "tryb": "z Bielikiem niedostepny -> uruchom tools/install-bielik.sh albo uzyj trybu bez Bielika",
                "powod": "Ollama nie odpowiada na " + HOST,
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
            "powod": "" if have else "Brak modelu. Uruchom tools/install-bielik.sh (zrobi pull za usera).",
        },
        0 if have else 3,
    )


def main():
    ap = argparse.ArgumentParser(description="Bielik w trybie doradcy (drugi rzut oka)")
    ap.add_argument("--file", help="plik z tekstem; domyslnie stdin")
    ap.add_argument("--n", type=int, default=6, help="liczba propozycji (domyslnie 6)")
    ap.add_argument("--check", action="store_true", help="sprawdz dostepnosc Ollama + modelu")
    a = ap.parse_args()

    if a.check:
        return check()

    text = open(a.file, encoding="utf-8").read() if a.file else sys.stdin.read()
    if not text.strip():
        return emit({"blad": "pusty input"}, 1)

    try:
        raw = call_advisor(text, a.n)
    except urllib.error.URLError as e:
        return emit(
            {
                "ok": False,
                "tryb": "fallback -> bez Bielika",
                "powod": "Nie moge polaczyc z Ollama (" + HOST + "). Uruchom tools/install-bielik.sh.",
                "blad": str(e),
            },
            2,
        )
    except Exception as e:  # noqa: BLE001
        return emit({"ok": False, "powod": "Blad wywolania Bielika", "blad": str(e)}, 2)

    try:
        parsed = json.loads(raw)
        props = parsed.get("propozycje", parsed if isinstance(parsed, list) else [])
        return emit({"model": MODEL, "tryb": "doradca", "propozycje": props,
                     "uwaga": "Bielik tylko proponuje. Opus osadza kazda propozycje i robi final, trzymajac fakty."}, 0)
    except Exception:
        print(raw)
        return 0


if __name__ == "__main__":
    sys.exit(main())
