# Tryb "z Bielikiem": setup i użycie

Dwa tryby recenzenta polszczyzny w humanizer-pl:

- **bez Bielika (domyślny)** - recenzentem polszczyzny jest główny model (Opus). Zero zależności,
  działa wszędzie. To wystarcza w 90% przypadków.
- **z Bielikiem (opcja)** - recenzentem jest lokalny Bielik (natywny polski LLM) przez Ollama.
  Bielik FLAGUJE kalki swoim native uchem, główny model NAPRAWIA oflagowane miejsca, trzymając
  fakty. Lokalnie, za darmo, prywatnie (tekst nie wychodzi z maszyny).

## Instalacja: jedna komenda (Claude robi to za usera)

User jest nietechniczny i nie zainstaluje Ollamy sam. Dlatego skill ma auto-instalator. Gdy user
wybiera tryb z Bielikiem, Claude uruchamia za niego:

```bash
bash .claude/skills/humanizer-pl/tools/install-bielik.sh
```

Skrypt jest idempotentny i NIEINTERAKTYWNY: instaluje Ollama (omija prompt trust, który blokuje
ręczną instalację), startuje serwer, pobiera Bielika (~6.7 GB). Jak wszystko już jest, kończy od
razu. Nie wymaga od usera ani jednej decyzji.

## Instalacja ręczna (gdyby ktoś chciał krok po kroku)

```bash
NONINTERACTIVE=1 HOMEBREW_NO_REQUIRE_TAP_TRUST=1 brew install ollama
brew services start ollama   # albo: ollama serve
ollama pull SpeakLeash/bielik-11b-v3.0-instruct:Q4_K_M   # ~6.7 GB
```

Uwaga: zwykłe `brew install ollama` potrafi utknąć na pytaniu `[y/n]` (przez nieufany tap). Stąd
`NONINTERACTIVE=1 HOMEBREW_NO_REQUIRE_TAP_TRUST=1` powyżej.

Lżejszy/szybszy wariant (gdy chcesz szybciej): `ollama pull SpeakLeash/bielik-4.5b-v3.0-instruct`,
potem ustaw `export BIELIK_MODEL=SpeakLeash/bielik-4.5b-v3.0-instruct`.

Sprzęt: Apple Silicon z 16+ GB RAM spokojnie uciągnie 11B Q4. Na M4 Pro / 48 GB jest szybko.

## Sprawdzenie dostępności

```bash
python3 .claude/skills/humanizer-pl/tools/bielik-review.py --check
```
- `ok: true` -> tryb z Bielikiem gotowy.
- `ok: false` + Errno 61 -> Ollama nie działa (uruchom `ollama serve`).
- `ok: false` + "Brak modelu" -> zrób `ollama pull ...`.

## Użycie

Dwa narzędzia:

- **`bielik-advisor.py` (zalecane, tryb doradcy)** - Bielik podsuwa N propozycji, Opus je osądza.
  ```bash
  python3 .claude/skills/humanizer-pl/tools/bielik-advisor.py --file zhumanizowany.md --n 6
  ```
- **`bielik-review.py` (tryb flaggera)** - Bielik daje ocenę 1-5 i ewentualne flagi.
  ```bash
  python3 .claude/skills/humanizer-pl/tools/bielik-review.py --file zhumanizowany.md
  ```

Zwraca JSON:
```json
{ "model": "...", "recenzja": {
    "ocena": 4,
    "werdykt": "ok",
    "flagi": [ { "fragment": "...", "problem": "...", "propozycja": "..." } ],
    "uwagi": "..." } }
```

Skrypt NIE przepisuje tekstu. Daje flagi. Główny model czyta flagi i poprawia oflagowane miejsca,
zachowując fakty, zero myślnika długiego i pełne ogonki.

## Zachowanie przy braku Ollama

Skrypt nigdy nie wybucha: zwraca czytelny komunikat `tryb: fallback -> bez Bielika` i kod wyjścia 2.
Skill wtedy po prostu robi recenzję polszczyzny głównym modelem (tryb domyślny). Nic nie blokuje.

## Zmienne środowiskowe

- `BIELIK_MODEL` - nazwa modelu w Ollama (domyślnie `SpeakLeash/bielik-11b-v3.0-instruct:Q4_K_M`).
- `OLLAMA_HOST` - adres serwera (domyślnie `http://localhost:11434`).

## Wynik testu na żywo (2026-06-13, Bielik-11B-v3.0 Q4_K_M)

Przetestowane na 3 realnych tekstach AIBB + snippetach. Werdykt: **na tym zadaniu Bielik 11B Q4
przegrał z recenzentem-Opusem.** Konkretnie:

- **Jako flagger**: zawsze zwracał `flagi: []` i tylko holistyczną ocenę 4/5. Nie wskazywał
  konkretnych kalek. Co gorsza, NIE złapał kalek, które Opus złapał ("supply", "kuracja", front
  przymiotnika), a za to wytykał żargon autora (moat, judgment, vibe coder), który celowo zostaje.
- **Jako przepisywacz**: popełnił błąd znaczeniowy. "kuracja" (w sensie content curation) przełożył
  na "lekarstwo lub rozwiązanie" (zrozumiał dosłownie jako medyczną kurację). Opus poprawnie dał
  "selekcja". To dokładnie ryzyko faktów, przed którym przestrzegamy. Dodatkowo nie doczyszczał
  slopu do końca ("kompleksowe" zostało) i dopisywał treść spoza oryginału.

Sprawdzono też, czy to wina promptu (hipoteza Igora): przetestowano 4 strategie - flagger, doradca,
doradca z twardym zakazem zmian sensu + negatywnymi przykładami, oraz tryb "tylko wskazuj nie
przepisuj". Żadna nie naprawiła problemu. Przy twardym zakazie Bielik zaproponował DOKŁADNIE zakazany
przykład ("wyciągnął framework" -> "stworzył model") i chciał przepisywać dosłowne cytaty. W trybie
pointer wskazywał zdania, które są poprawne, i halucynował problemy. To potwierdza: **sufit modelu
11B Q4, nie kwestia promptu.** Jedyna nieprzetestowana zmienna to Q8 (mniej skompresowany, ~10 GB) -
oczekiwanie: co najwyżej marginalna poprawa.

Wniosek: **domyślny tryb bez Bielika (recenzent-Opus) jest lepszy.** Bielik zostaje jako opcjonalny
TANI DRUGI SYGNAŁ: jego ocena 1-5 jest spójna i lokalna za darmo, więc nadaje się na bramkę
("jeśli Bielik < 3, przejrzyj jeszcze raz"), ale NIE jako główny recenzent ani przepisywacz.
Zastrzeżenie: testowano kwant Q4 11B; Q8 albo few-shot mogą wyostrzyć flagi, ale błąd znaczeniowy
to sufit możliwości modelu, nie kwestia promptu.

## Dlaczego Bielik tylko flaguje, a nie przepisuje

Bielik (11B) jest mniejszy od głównego modelu: słabszy w trzymaniu faktów i instrukcjach złożonych,
ale ma natywne polskie ucho. Dlatego gra pod swoją siłę (wyłapywanie kalek), a ryzykowną część
(przepisanie bez gubienia faktów) zostawiamy głównemu modelowi. Podział: Bielik sędzia, Opus
wykonawca.
