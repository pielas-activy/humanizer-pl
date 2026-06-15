# humanizer-pl

Dwujęzyczny (PL + EN) skill do Claude Code / Cowork, który usuwa oznaki pisania AI z tekstu,
zachowując sens, fakty i głos autora. Fork [blader/humanizer](https://github.com/blader/humanizer)
rozszerzony o pełną warstwę polskiej naturalności.

> **TL;DR (EN):** A bilingual de-slop skill. Removes AI-writing tells from Polish AND English text
> while preserving meaning and voice. The English patterns come 1:1 from blader/humanizer; the
> Polish layers, the Bielik experiment and the eval harness are new. Auto-detects language.

## Po co to

Każdy de-AI/humanizer w sieci jest po angielsku. Polski AI-slop to jednak NIE przetłumaczony
angielski: GPT i Claude po polsku mają własne tells (kalki, nadmiar imiesłowów, klisze epoki,
parataksa zamiast hipotaksy). `humanizer-pl` celuje w jedno i drugie.

## Instalacja

Skopiuj do katalogu skilli Claude Code:

```bash
git clone https://github.com/pielas-activy/humanizer-pl \
  ~/.claude/skills/humanizer-pl
```

Działa od razu w trybie domyślnym (bez zależności). Tryb z Bielikiem (opcjonalny, lokalny polski
LLM) ma auto-instalator, patrz niżej.

## Co robi

1. **Wykrywa język** -> ładuje wzorce PL albo EN (progressive disclosure, czyta tylko to, czego
   potrzebuje).
2. **De-slop, odważnie.** Usuwa myślnik długi, "to nie X, to Y", rule of three, anaforę, watę.
   Przepisuje strukturę zdań, nie tylko interpunkcję.
3. **Przebieg polszczyzny (tylko PL).** Tłumaczy leniwe anglicyzmy (zostawia żargon autora),
   pilnuje czasowników, rozwija kalki-przymiotniki, łapie ukryty "nie X, to Y" i **scala urywane
   zdania w złożone** (parataksa -> hipotaksa, najsilniejszy polski tell). Na końcu osobny **skan
   kalek** (test odwrotnego tłumaczenia, nie zamknięta lista).
4. **Final.** Skan: zero myślnika długiego, pełne ogonki, fakty 1:1.
5. **Uczy się Twojego żargonu (opcjonalnie).** Wykrywa branżowe terminy i może zapamiętać Twoją
   osobistą listę "tego nie ruszaj", per user i lokalnie. Szczegóły w sekcji "Profil żargonu".

## Tryby recenzenta polszczyzny

- **Bez Bielika (domyślny).** Recenzentem jest główny model. Zero zależności, działa wszędzie.
- **Z Bielikiem (opcja).** Lokalny natywny polski LLM (Bielik-11B przez Ollama) DORADZA, główny
  model osądza, a propozycje trafiają do usera do decyzji. Auto-instalator
  `tools/install-bielik.sh` robi wszystko za nietechnicznego usera (instaluje Ollama, pobiera
  model). Setup: [`tools/setup-bielik.md`](tools/setup-bielik.md).

### Eksperyment: czy Bielik (polski LLM) jest dobrym recenzentem polszczyzny?

Bielik jest reklamowany jako model mocny w polskim, więc przetestowaliśmy go jako recenzenta w
4 trybach na 8 realnych tekstach (81 propozycji), z każdą propozycją osądzoną przez mocniejszy
model. Wynik: **0 realnych trafień, ponad 40-50% propozycji wprost szkodliwych** (zmiana sensu,
faktu albo przepisywanie cytatu). Lepszy prompt zbił liczbę i szkody, ale nie jakość. Wniosek:
jako samodzielny recenzent gęstego w fakty tekstu Bielik-11B nie dowozi; jako doradca pod
nadzorem mocniejszego modelu jest bezpieczny, ale niewiele wnosi. Tryb z Bielikiem zostaje jako
ciekawostka i przykład, jak spiąć lokalny model w pipeline.

## Profil żargonu (opcjonalny, per user)

Skill nie zna z góry niczyjego żargonu i celowo go nie hardkoduje (nie jest "do AI" ani do żadnej
jednej branży). Zamiast tego potrafi **wykryć Twój żargon i go zapamiętać**:

- Gdy w tekście widzi dużo powracających, branżowych terminów (prawnik: "cesja", "rękojmia";
  marketer: "lead", "funnel"), sam proponuje krótką sesję w stylu "zapamiętać, których nie ruszać?".
- Możesz to też odpalić wprost: "zapamiętaj mój żargon" albo "zbuduj mój profil żargonu".
- Potwierdzoną listę zapisuje lokalnie w `references/jargon-profile.local.md` (prywatnie, per
  maszyna, gitignore, nie trafia do repo) i przy kolejnych tekstach pilnuje, żeby tych słów nie
  tłumaczyć ani nie "poprawiać".

Każdy ma swój profil: prawnik prawniczy, marketer marketingowy, Ty swój. Dzięki temu uniwersalny
skill nie przekłada Twojego fachowego słownictwa na siłę.

## Struktura

```
humanizer-pl/
  SKILL.md                  router: wykryj język -> wzorce -> proces -> (PL) polszczyzna
  references/
    patterns-en.md          33 wzorce blader 1:1 (EN) + TOC
    patterns-pl.md          6 kategorii PL + rodzina "manufaktura rytmu"
    polszczyzna-pl.md        warstwa naturalności PL (anglicyzmy, czasowniki, kalki,
                            ukryty "nie X, to Y", parataksa -> hipotaksa, skan kalek)
    przyklady.md            pary PRZED/PO (PL z banku, EN z blader)
    raport-html.md          szablon raportu HTML (side-by-side + lista zmian), tryb opcjonalny
  evals/
    evals.json              6 binarnych asercji + 2 zamrożone case'y
    run_evals.py            deterministyczny runner
  tools/                    tryb "z Bielikiem" (opcjonalny)
    install-bielik.sh, bielik-advisor.py, bielik-review.py, setup-bielik.md
```

## Twarde zasady wyjścia

- Zero myślnika długiego (U+2014) i półpauzy (U+2013), zawsze ASCII `-`.
- Polskie znaki (pełne ogonki) w polskim tekście.
- Nie zmieniaj języka, nie wymyślaj faktów, output nie puszy treści.

Wyjątek: `references/patterns-en.md` i sekcja EN w `przyklady.md` cytują blader 1:1, więc w
negatywnych przykładach "before" mają myślniki - to demonstrowany tell. Wynik skilla ich nie
zawiera.

## Evals

```bash
python3 evals/run_evals.py
```

Sprawdza 6 binarnych asercji na zamrożonych przykładach: brak myślnika, polskie znaki, brak słów
z banów, output nie dłuższy niż input, pierwsza linia nie wypełniacz, brak artefaktów chatbota.

## Użycie

W Claude Code: `/humanizer-pl` albo "zhumanizuj ten post / wywal AI-slop z tego maila".
Auto-wykrywa PL/EN. Tryb z Bielikiem: "zhumanizuj + sprawdź Bielikiem". Raport HTML ze zmianami
(side-by-side + lista zmian): "zhumanizuj + raport HTML". Profil żargonu (czego nie tłumaczyć):
"zapamiętaj mój żargon".

## Atrybucja

Fork [blader/humanizer](https://github.com/blader/humanizer) (MIT), który z kolei bazuje na
wikipedijowym przewodniku "Signs of AI writing". Angielskie wzorce w `patterns-en.md` są jego,
przeniesione 1:1. Polskie warstwy, integracja z Bielikiem i evals to dodatki. Licencja: MIT.
