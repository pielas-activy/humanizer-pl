---
name: humanizer-pl
version: 1.0.0
description: Removes AI-writing tells from Polish AND English text while preserving meaning and the author's voice. Use when asked to humanize, de-AI, de-slop or clean up AI-sounding text (post, email, draft, newsletter). Auto-detects language (PL/EN). Does NOT trigger for translation or general editing.
license: MIT
compatibility: claude-code opencode
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# Humanizer PL: de-slop dwujęzyczny (PL + EN)

Router. Wykrywa język tekstu, ładuje TYLKO właściwy plik wzorców, prowadzi wspólny proces
przepisywania. Jeden mały `SKILL.md`, wzorce per język w `references/` (progressive disclosure).
Usuwa uniwersalny AI-slop, NIE narzuca niczyjego głosu. Bazuje na forku
[blader/humanizer](https://github.com/blader/humanizer) (treść EN nietknięta, 1:1).

## KROK 0: wykryj język i wczytaj wzorce

Patrzysz na tekst wejściowy. Heurystyka:

- Polskie znaki (`ą ć ę ł ń ó ś ź ż`) -> tekst jest po polsku (sygnał główny). Wczytaj
  `references/patterns-pl.md`.
- Brak ogonków, ale są polskie słowa funkcyjne (`że, się, oraz, który`) -> też polski (fallback,
  gdy ktoś pisze bez ogonków). Wczytaj `references/patterns-pl.md`.
- Brak polskich sygnałów, tekst angielski -> wczytaj `references/patterns-en.md`.
- Tekst mieszany -> potraktuj każdy fragment w jego języku; nie tłumacz między językami.
- Dla polskiego wczytaj DODATKOWO `references/polszczyzna-pl.md` na drugi przebieg (naturalność PL:
  anglicyzmy, zdania bez czasownika, kalki-przymiotniki, ukryty "nie X, to Y").

Wczytaj `references/przyklady.md` dla par PRZED/PO, jeśli potrzebujesz kalibracji. References są
płaskie, jeden poziom w głąb. Nie zagnieżdżaj dalej.

Jeśli w `references/` jest `jargon-profile.local.md` (osobisty profil żargonu usera, lokalny i
gitignorowany), wczytaj go. Terminy z niego są TWARDO CHRONIONE we wszystkich przebiegach (de-slop,
polszczyzna, skan kalek): nigdy ich nie tłumaczysz ani nie "poprawiasz". To rozszerza generyczny
guard o konkretne słownictwo tego usera.

## Wspólny proces

1. **Przeczytaj wejście** i znajdź każdy tell z wczytanego pliku wzorców.
2. **Kalibracja głosu (opcjonalna).** Jeśli user dał próbkę swojego pisania, przeczytaj ją najpierw: długość zdań, poziom słownictwa, jak
   zaczyna akapity, nawyki interpunkcyjne, powracające zwroty. Dopasuj wynik do tej próbki, nie do
   generycznego "ładnego" stylu. Bez próbki: naturalny, zróżnicowany, konkretny głos.
3. **Draft.** Przepisz, nie wycinaj treści. Pokrywasz wszystko, co pokrywał oryginał (pięć
   akapitów -> pięć akapitów). Zachowujesz sens, fakty, liczby, język i głos autora. Wymieniasz
   tell na konkret, nie na inny tell.
4. **Audyt.** Zapytaj wprost: "Co w tym tekście wciąż brzmi jak AI?" Wypisz krótko, co zostało.
5. **Final.** Popraw to, co audyt wyłapał. Potem przeskanuj wynik na znaki `U+2014` (myślnik długi)
   i `U+2013` (półpauza). Każde trafienie = draft niegotowy.
6. **Przebieg polszczyzny (tylko PL).** Puść wynik jeszcze raz wg `references/polszczyzna-pl.md`
   (patrz sekcja niżej). To osobny cel niż de-slop: naturalność polskiego.
7. **Pokaż before/after** plus krótkie bullety "co usunąłem".

## Głębokość ingerencji (nie bądź nieśmiały)

De-slop to przepisanie, nie kosmetyka. Jeśli po Twoim przebiegu jedyne zmiany to wymiana myślników
i kilka słów, byłeś za miękki. Czysty tekst zmienia STRUKTURĘ zdań, nie tylko interpunkcję.

- **Wzorzec, który się POWTARZA, jest tellem właśnie dlatego, że się powtarza.** "To nie X, to Y",
  rule of three, anafora ("Bez X. Bez Y."), unikanie "jest/są" - uderzające raz to głos; te same
  konstrukcje 3-4 razy w jednym tekście to manufaktura rytmu. Policz wystąpienia. Rozbij monotonię:
  przepisz większość na zwykłe zdania, zostaw najwyżej jedno dla emfazy.
- **Zaczynaj od pointy, nie od negacji.** "Trudna część to nie budowanie. To wiedza, CO zbudować" ->
  "Najtrudniej jest wiedzieć, CO zbudować. Samo budowanie jest łatwe." Twierdzenie na przód, negację
  zdegraduj albo wytnij.
- **Guard false-positives chroni KONKRET, nie konstrukcję.** Zostawiasz nietknięty trudny do
  podrobienia detal, liczbę, nazwisko, mieszane uczucia, świeży żargon autora. To NIE jest licencja
  na to, żeby tylko wymienić myślniki. Schematyczne, waflowate zdanie przepisujesz naprawdę.
- **Test odwagi (przed oddaniem finału):** przejrzyj diff. Jeśli ponad 80% zmian to same myślniki i
  pojedyncze słowa, wróć i przepisz strukturę najsłabszych akapitów. Lepszy humanizer zostawia
  widoczny ślad na poziomie zdań, nie tylko interpunkcji.

## Przebieg polszczyzny (PL, drugi przebieg)

Dla polskiego tekstu de-slop to dopiero połowa. Drugi przebieg pilnuje, żeby polski brzmiał jak
polski, nie jak tłumaczenie z angielskiego. Pełne reguły i tabele w `references/polszczyzna-pl.md`.
W skrócie sześć rzeczy:

- **Anglicyzmy: tłumacz leniwe, zostaw żargon.** "supply" -> podaż, "kuracja"/curation -> selekcja
  albo wybór, "commodity" -> towar masowy. ZOSTAW świadomy żargon zawodowy autora (z dowolnej
  branży: prawo, medycyna, kuchnia, finanse, sport, IT) oraz nazwy własne.
- **Każde zdanie ma czasownik osobowy.** Nie zaczynaj od przymiotnika-orzecznika w stylu kalki
  ("Najcenniejsza w internecie jest...") - przestaw szyk albo dopisz czasownik. Urwany dopełniacz
  bez czasownika ("Od rozwiązywania problemów z agentem u boku.") scal z sąsiadem.
- **Rozwiń kalki-przymiotniki.** "zawody automatyzacyjne" -> "zawody, które można zautomatyzować".
- **Złap ukryty "nie X, to Y".** "Nie uczę promptowania, uczę myślenia." -> "Zamiast uczyć
  promptowania, skupiam się na myśleniu."
- **Scalaj urywane zdania w złożone (parataksa -> hipotaksa).** AI sieka po polsku na krótkie
  zdania; polski woli jedno złożone. To też rozbraja staccato "to nie X, to Y": "To nie jest 'wpis
  do CV'. To jest nowa drabina." -> "to nie jest już tylko 'wpis do CV', ale dostawienie nowej
  drabiny w ścieżce kariery." Nie scalaj wszystkiego; jedno krótkie zdanie dla emfazy zostaje.
- **Skan kalek (osobny ruch na końcu).** Kalki są gramatyczne, więc przepuszcza je i de-slop, i
  szybkie czytanie. Przejedź tekst jeszcze raz TYLKO pod kątem kalek, testem: (1) odwrotne
  tłumaczenie na angielski ("na ten moment" -> "at this point"), (2) czy jest prostsze polskie słowo
  (finalnie -> ostatecznie), (3) rejestr (korpo czy mowa). Listy nie da się domknąć, więc to test,
  nie słownik. Pełna sekcja "Skan kalek" w `references/polszczyzna-pl.md`.

Recenzenta polszczyzny masz w dwóch trybach (wybierz):

- **Tryb bez Bielika (domyślny).** Recenzentem jest główny model: po przebiegu sam czyta wynik i
  flaguje te cztery rzeczy, potem poprawia. Zero zależności, działa wszędzie. W workflow zrób z tego
  osobnego subagenta "recenzent polszczyzny".
- **Tryb z Bielikiem (opcja, Bielik jako DORADCA = drugi rzut oka).** Lokalny natywny polski model
  podsuwa propozycje, a Opus je osądza. Pełny pipeline ma 4 etapy:
  1. **Humanizer** (de-slop, główny model).
  2. **Recenzent Opus** (przebieg polszczyzny, główny model).
  3. **Doradca Bielik**: `python3 .claude/skills/humanizer-pl/tools/bielik-advisor.py --file <tekst>`
     - zwraca N konkretnych propozycji naturalniejszego brzmienia.
  4. **Pokaż propozycje userowi, user decyduje.** NIE aplikuj zmian Bielika po cichu. Pokaż userowi
     listę: każda propozycja (fragment -> na co zmienić) plus krótka ocena Opusa obok (szkodliwa /
     żargon / bez poprawy / realna), żeby user widział, które są ryzykowne. User wybiera, co przyjąć.
     Opus wykonuje tylko zaakceptowane zmiany, trzymając fakty. Bielik proponuje, Opus ostrzega,
     decyzja należy do usera. (Bielik bywa, że zmienia sens, np. "kuracja" -> "lekarstwo" - dlatego
     nigdy nie pisze do tekstu wprost.)

  **Auto-instalacja dla nietechnicznego usera.** Gdy user wybiera tryb z Bielikiem, NIE każ mu nic
  instalować. Sam sprawdź `bielik-advisor.py --check`; jeśli `ok: false`, uruchom za niego
  `bash .claude/skills/humanizer-pl/tools/install-bielik.sh` (instaluje Ollama nieinteraktywnie,
  startuje serwer, pobiera Bielika ~6.7 GB, idempotentnie). Pełna instrukcja: `tools/setup-bielik.md`.
  Jeśli Ollama mimo to niedostępna -> `fallback -> bez Bielika`.

  Uwaga z testu (2026-06-13, Bielik-11B Q4): jako samodzielny recenzent/przepisywacz Bielik wypada
  SŁABO (gubi kalki, myli "kuracja"/"lekarstwo"). Jako DORADCA pod sędzią-Opusem jest bezpieczny:
  w teście 3 z 5 jego propozycji zaszkodziłyby, Opus złapał wszystkie i wyłuskał 1 realne ziarno.

Żargon autora zostaje w obu trybach. W trybie z Bielikiem to zawsze Opus jest sędzią i wykonawcą
finalnych poprawek; Bielik tylko podsuwa (drugi rzut oka).

## Twarde zasady wyjścia

- **Zero myślnika długiego i półpauzy.** Zawsze zwykły myślnik ASCII `-`. To twarda zasada projektu,
  nie preferencja. Zamienniki w kolejności: kropka, przecinek, dwukropek, nawias, przebudowa zdania.
- **Polskie znaki zachowane** w polskim tekście. `własny` nie `wlasny`, `się` nie `sie`.
- **Nie zmieniaj języka.** Polski wchodzi, polski wychodzi. Humanizacja to nie tłumaczenie.
- **Output nie dłuższy niż input.** Humanizacja de-slopu skraca, nie puszy. To zakaz inflacji, nie
  licencja na wycinanie treści: jeśli wierne pokrycie wymaga więcej miejsca niż zwięzły wkład,
  pokrycie wygrywa (gate celuje w slop, a slop zawsze się kurczy).
- **Pierwsza linia nie jest wypełniaczem.** Żadnego "Warto zauważyć" / "W dzisiejszych czasach" /
  "In today's world" na otwarcie. Zaczynaj od konkretu.
- **Nie wymyślaj faktów.** Nie dodawaj liczb ani źródeł, których nie było w oryginale; jeśli
  oryginał był ogólnikowy, zostaw miejsce na konkret zamiast zmyślać.

## Format wyniku

Oddaj: draft, krótkie bullety "wciąż brzmi jak AI", final, opcjonalnie podsumowanie zmian.
Przy false-positives: chroń to, co naprawdę ludzkie (konkretny detal, liczba, mieszane uczucia,
świeży żargon autora) - tego nie ruszaj. Ale to NIE wymówka na nieśmiałość: schematyczne i
powtórzone konstrukcje przepisuj naprawdę (patrz "Głębokość ingerencji"). Guard z sekcji "What NOT
to flag" w `references/patterns-en.md` obowiązuje też dla PL.

## Tryb opcjonalny: raport HTML (side-by-side + lista zmian)

Na życzenie usera ("raport HTML", "pokaż zmiany side by side", "raport zmian", "diff HTML",
"podświetl zmiany") oddaj dodatkowo samodzielny plik HTML z dwiema kolumnami obok siebie (oryginał
lewo, wynik prawo, z podświetlonymi zmianami) i tabelą zmian pod spodem (fragment przed -> po, typ
tellu, krótki powód). Gdy user o to prosi, wczytaj `references/raport-html.md` (szablon plus
instrukcja) i wygeneruj plik. To dodatek, nie zamiennik zwykłego before/after w czacie.

## Tryb opcjonalny: profil żargonu (osobista lista keep, per user)

Skill uniwersalny nie zna z góry niczyjego żargonu, więc zamiast wpisywać go na sztywno pozwala
każdemu userowi zbudować własną listę terminów do ochrony. Lista żyje lokalnie w
`references/jargon-profile.local.md` (gitignorowana, nigdy nie trafia do repo) i jest wczytywana w
KROK 0. Te terminy są chronione ponad generyczny guard: nie tłumaczysz ich ani nie ruszasz.

Kiedy zaproponować sesję:
- **Wprost**, gdy user prosi ("zbuduj/zaktualizuj mój profil żargonu", "zapamiętaj mój żargon").
- **Z własnej inicjatywy**, gdy w tekście widzisz dużo powracających, branżowych terminów obcych,
  przy których wahasz się "zostawić czy tłumaczyć". Wtedy zaproponuj krótką sesję, nie rób tego po
  cichu.

Sesja: wypisz kandydatów (terminy plus zgadnięty obszar), user potwierdza, dodaje albo usuwa, a Ty
zapisujesz wynik do `references/jargon-profile.local.md` (prosta lista, opcjonalnie z obszarem).
Profil jest per user i prywatny; na kolejnych przebiegach po prostu go wczytujesz.


## Learnings

(Reflection write-back. Dopisuj tu krótkie wnioski, gdy w praktyce wyjdzie nowy tell albo wzorzec.)

- 2026-06-13: Napięcie 1:1 vs zakaz myślnika. `references/patterns-en.md` cytuje blader dosłownie,
  więc jego negatywne przykłady "Before" zawierają myślnik długi (to jest demonstrowany tell).
  Rozwiązanie: zakaz myślnika obowiązuje OUTPUT skilla i prozę autorską (router, patterns-pl,
  evals), a nie wierne cytaty źródła. Evals sprawdzają wynik humanizacji, nie pliki reference.
- 2026-06-13: Z testu na blogu wyszło, że skill był NIEŚMIAŁY (wymiana myślników plus parę
  słów, ale zostawione 4x "to nie X, to Y"). Za dużo hamulców ("nie wycinaj", "output nie dłuższy",
  guard) plus zachowawczy blader = kosmetyka. Dodano sekcję "Głębokość ingerencji": powtórzony
  wzorzec to tell, zaczynaj od pointy nie od negacji, guard chroni konkret nie konstrukcję, test
  odwagi na diffie. Domyślnie ma przepisywać strukturę, nie tylko interpunkcję.
- 2026-06-13: Z testów na blogach: de-slop nie wystarcza dla PL, bo zostawia
  anglicyzmy ("supply", "kuracja"), zdania bez czasownika / z frontem przymiotnika, kalki
  ("zawody automatyzacyjne") i UKRYTY "nie X, to Y" ("Nie uczę promptowania, uczę myślenia").
  Dodano osobną warstwę `references/polszczyzna-pl.md` + krok 6 "Przebieg polszczyzny" + wzorzec
  dedykowanego subagenta-recenzenta polszczyzny w workflow. Cel: polski ma brzmieć jak polski,
  zostawiając żargon autora.
- 2026-06-13: Recenzent polszczyzny w dwóch trybach. Bez Bielika (główny model) i
  z Bielikiem (lokalny natywny polski LLM przez Ollama, `tools/bielik-review.py`). Bielik flaguje
  kalki swoim native uchem, główny model naprawia (Bielik mniejszy, ryzyko faktów). Darmowo,
  lokalnie, z fallbackiem do trybu bez Bielika gdy Ollama niedostępna. Setup: `tools/setup-bielik.md`.
- 2026-06-13: Audyt Bielika (4 tryby x 8 tekstów, 81 itemów): 0 realnych wygranych, 51% szkodliwych
  w trybie wymuszonym, 42% w ulepszonym. Ulepszony prompt (rola zamiast listy nazw, bez wymuszania
  N) ściął propozycje 39->14 i szkody 19->6, ale sufit jakości został. Werdykt: bez Bielika domyślnie,
  z Bielikiem = ciekawostka. Tryb z Bielikiem POKAZUJE propozycje userowi (fragment -> zmiana + ocena
  Opusa), user decyduje - nie aplikujemy po cichu.
- 2026-06-13: Z testów wyszły dwa braki, które de-slop przepuszczał. (1) "to nie X, to Y" przeżywa
  najczęściej jako DWA urywane zdania - problemem jest staccato, nie kontrast; fix to scalenie w
  zdanie złożone. (2) Zdania-dopełniacze bez czasownika ("Od rozwiązywania problemów z agentem u
  boku.") - polski tak nie pisze. Master-fix dla obu: parataksa -> hipotaksa (sekcja 5 w
  polszczyzna-pl.md). AI sieka po polsku na krótkie zdania, polski woli złożone.
- 2026-06-14: Kalki przeżywają de-slop, bo to poprawna polszczyzna - pass strukturalny się po nich
  prześlizguje, a kolejne przebiegi na tym samym tekście łapały nowe ("na ten moment", "finalnie").
  Wniosek z użycia: słownika kalek nie da się domknąć (lista zawsze niepełna). Fix: osobny, nazwany
  "Skan kalek" oparty na TEŚCIE (odwrotne tłumaczenie + prostsze polskie słowo + rejestr), nie na
  dopasowaniu do listy; lista = tylko ziarno do kalibracji. Sekcja w polszczyzna-pl.md + bullet w
  przebiegu polszczyzny.
- 2026-06-14: Odchudzenie z biasu AI. Skill jest uniwersalny i publiczny, a przykłady "zostaw
  żargon" oraz część par PRZED/PO były z jednej branży (AI/vibecoding), co sugerowało, że skill jest
  "do AI". Keep-lista i guard przepisane na zasadę (żargon zawodowy z DOWOLNEJ branży), część
  przykładów PRZED/PO rozsiana na różne dziedziny (gastronomia, fitness, sprzedaż).
- 2026-06-14: Dodany tryb opcjonalny "raport HTML" (references/raport-html.md): samodzielny plik z
  side-by-side oryginał vs wynik (podświetlone zmiany) + tabela zmian (przed -> po, typ tellu, powód).
  Na życzenie usera, nie domyślnie.
- 2026-06-14: Zamiast hardkodować żargon (czyjkolwiek) w uniwersalnym skillu, dodany tryb "profil
  żargonu": per-user lista keep w `references/jargon-profile.local.md` (gitignore `references/*.local.md`),
  wczytywana w KROK 0 i chroniona we wszystkich przebiegach. Skill może sam zaproponować sesję, gdy
  wykryje gęsty branżowy żargon. Żargon konkretnego usera (np. autora) żyje w jego profilu, nie w repo.
