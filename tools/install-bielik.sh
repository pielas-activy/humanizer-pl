#!/usr/bin/env bash
# Auto-instalator Ollama + Bielik dla trybu "z Bielikiem" w humanizer-pl.
# Robi wszystko za nietechnicznego usera: instaluje Ollama, startuje serwer, pobiera model.
# Idempotentny i NIEINTERAKTYWNY (omija prompt trust, ktory wczesniej blokowal instalacje).
# Bez `sleep` - czekanie na serwer realizuje curl --retry-connrefused.
set -uo pipefail

MODEL="${BIELIK_MODEL:-SpeakLeash/bielik-11b-v3.0-instruct:Q4_K_M}"
HOST="${OLLAMA_HOST:-http://localhost:11434}"
BASE="${MODEL%%:*}"
OLLAMA_BIN=""

say(){ printf '\n>> %s\n' "$1"; }
find_bin(){
  for p in "$(command -v ollama 2>/dev/null)" /opt/homebrew/bin/ollama /usr/local/bin/ollama "$HOME/.ollama/bin/ollama"; do
    [ -n "$p" ] && [ -x "$p" ] && { printf '%s' "$p"; return 0; }
  done
  return 1
}

# 1. Binarka Ollama
OLLAMA_BIN="$(find_bin || true)"
if [ -z "$OLLAMA_BIN" ]; then
  say "Instaluje Ollama (nieinteraktywnie)..."
  if command -v brew >/dev/null 2>&1; then
    NONINTERACTIVE=1 HOMEBREW_NO_REQUIRE_TAP_TRUST=1 brew install ollama
  else
    say "Brak Homebrew - instaluje Ollama oficjalnym skryptem."
    curl -fsSL https://ollama.com/install.sh | sh
  fi
  OLLAMA_BIN="$(find_bin || true)"
fi
[ -z "$OLLAMA_BIN" ] && { echo "BLAD: nie udalo sie zainstalowac Ollama."; exit 1; }
say "Ollama: $OLLAMA_BIN ($("$OLLAMA_BIN" --version 2>/dev/null | head -1))"

# 2. Serwer (jak nie chodzi - odpal)
if ! curl -sf -m 3 "$HOST/api/version" >/dev/null 2>&1; then
  say "Uruchamiam serwer Ollama..."
  command -v brew >/dev/null 2>&1 && brew services start ollama >/dev/null 2>&1 || true
  if ! curl -sf -m 3 "$HOST/api/version" >/dev/null 2>&1; then
    nohup "$OLLAMA_BIN" serve >/tmp/ollama-serve.log 2>&1 &
  fi
  curl --retry-connrefused --retry 30 --retry-delay 1 -sf -m 60 "$HOST/api/version" >/dev/null 2>&1 || true
fi
curl -sf -m 3 "$HOST/api/version" >/dev/null 2>&1 || { echo "BLAD: serwer Ollama nie wstal (sprawdz /tmp/ollama-serve.log)."; exit 2; }
say "Serwer dziala: $(curl -s "$HOST/api/version")"

# 3. Model Bielik
if "$OLLAMA_BIN" list 2>/dev/null | grep -q "$BASE"; then
  say "Bielik juz jest: $MODEL"
else
  say "Pobieram Bielika ($MODEL, ~6.7 GB, to chwile potrwa)..."
  "$OLLAMA_BIN" pull "$MODEL"
fi

if "$OLLAMA_BIN" list 2>/dev/null | grep -q "$BASE"; then
  say "GOTOWE. Tryb z Bielikiem dziala. Sprawdz: python3 tools/bielik-advisor.py --check"
  exit 0
else
  echo "BLAD: model sie nie pobral."; exit 3
fi
