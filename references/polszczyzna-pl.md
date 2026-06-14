# Polszczyzna: warstwa naturalności PL (drugi przebieg)

> Osobny przebieg PO de-slopie, tylko dla polskiego. De-slop usuwa AI-tells (myślnik, "to nie X,
> to Y", wata). Ten przebieg pilnuje czegoś innego: żeby polski brzmiał jak polski, a nie jak
> tłumaczenie z angielskiego. Można go odpalić jako osobnego "recenzenta polszczyzny" (subagent),
> który czyta gotowy wynik i flaguje cztery rzeczy poniżej.
>
> Zasada nadrzędna: zachowujesz sens, fakty i głos. Nie tłumaczysz żargonu autora ani terminów bez
> dobrego polskiego odpowiednika. Czyścisz tylko leniwe kalki i nienaturalny szyk.

## Spis treści

- [1. Anglicyzmy: tłumacz leniwe, zostaw żargon](#1-anglicyzmy-tłumacz-leniwe-zostaw-żargon)
- [2. Zdanie musi mieć czasownik](#2-zdanie-musi-mieć-czasownik)
- [3. Rozwiń kalki-przymiotniki](#3-rozwiń-kalki-przymiotniki)
- [4. Ukryty "nie X, to Y"](#4-ukryty-nie-x-to-y)
- [5. Scalaj urywane zdania w zdanie złożone](#5-scalaj-urywane-zdania-w-zdanie-złożone)
- [Jak używać](#jak-używać)

---

## 1. Anglicyzmy: tłumacz leniwe, zostaw żargon

Decyzja per słowo. ZOSTAW termin angielski, gdy to (a) ustalony żargon techniczny bez dobrego
polskiego odpowiednika, albo (b) świadomy, powracający termin autora. PRZETŁUMACZ, gdy istnieje
naturalne polskie słowo, a angielski nic nie wnosi (to wtedy lenistwo, nie głos).

| Zostaw (żargon / głos autora) | Przetłumacz (leniwy anglicyzm) |
|---|---|
| judgment, moat, agentic economy, routing layer, agent discovery, MCP, deploy, framework, product management, tooling, vibe coding | supply -> podaż |
| nazwy własne i produkty (Stripe, Notion, ChatGPT) | curation / "kuracja" -> selekcja, wybór, kuratorowanie |
| | commodity -> towar masowy, dobro powszechne |
| | "plausible content" -> wiarygodnie wyglądające treści |
| | checkout -> koszyk, płatność |
| | output (ogólny rzeczownik) -> wynik, efekt |
| | "structured knowledge graph" -> uporządkowany graf wiedzy |

Uwaga na **pseudo-polski** (kalka udająca tłumaczenie): "kuracja" zamiast "curation" brzmi gorzej
niż oryginał. Wybierz prawdziwe polskie słowo (selekcja, wybór), nie spolszczony angielski.
Gdy nie masz pewności, czy coś to żargon autora, sprawdź czy termin powtarza się w tekście jako
świadomy motyw - jeśli tak, zostaw.

## 2. Zdanie musi mieć czasownik

Polski AI-slop kalkuje angielski szyk: fronton przymiotnik albo orzecznik na początku, czasem zdanie
bez czasownika osobowego. Po polsku zdanie potrzebuje czasownika i naturalnego szyku.

- Fronted przymiotnik: "Najcenniejsza w internecie jest Twoja sytuacja." -> "W internecie najcenniejsza
  jest Twoja konkretna sytuacja." (albo "Twoja konkretna sytuacja jest w sieci najcenniejsza.")
- Urwane bez czasownika: "Piękne. I kompletnie paraliżujące." -> "Wygląda pięknie, a kompletnie
  paraliżuje."
- Rzeczownik-etykieta zamiast zdania: "Najpierw brief z AI, specyfikacja, MoSCoW, prompt." (lista bez
  orzeczenia jest OK jako lista, ale nie jako "zdanie") -> upewnij się, że zdanie wokół niej ma
  czasownik.
- Urwany dopełniacz bez czasownika: "Od rozwiązywania problemów z agentem u boku." (samo "Od..." to
  nie jest polskie zdanie) -> scal z poprzednim zdaniem w jedno złożone (patrz sekcja 5).

Zasada: jeśli zdanie nie ma czasownika osobowego, dopisz go albo scal z sąsiednim. Wyjątek: jeden
świadomy, krótki wykrzyknik dla emfazy ("No i pięknie.").

## 3. Rozwiń kalki-przymiotniki

Angielski upycha znaczenie w przymiotnik; polski woli zdanie względne albo dopełniacz.

- "zawody automatyzacyjne" -> "zawody, które można zautomatyzować"
- "rozwiązania chmurowe" (gdy to kalka) -> "rozwiązania w chmurze"
- "treści generowane AI" -> "treści generowane przez AI"

Zasada: rzeczownik plus sztuczny przymiotnik z angielskiego -> rozwiń w "który / do / z / przez".

## 4. Ukryty "nie X, to Y"

To ten sam negatywny paralelizm co w patterns-pl, tylko z czasownikiem, więc łatwo go przeoczyć.
Schemat "Nie robię X, robię Y" / "Nie uczę X, uczę Y". Przepisz na "Zamiast X, Y".

- "Nie uczę promptowania, uczę myślenia." -> "Zamiast uczyć promptowania, skupiam się na myśleniu."
- "Nie sprzedajemy produktu, sprzedajemy efekt." -> "Sprzedajemy efekt, nie sam produkt." (albo
  "Zamiast produktu dajemy efekt.")
- "To nie kurs o narzędziach, to kurs o decyzjach." -> "Ten kurs jest o decyzjach, nie o narzędziach."

Reguła z patterns-pl obowiązuje: zostaw najwyżej jedno takie wystąpienie na tekst, resztę przepisz.
Uwaga: najgorsza i najczęściej przeoczana forma to DWA urywane zdania ("To nie jest 'wpis do CV'.
To jest nowa drabina."). Tu problemem jest nie tyle kontrast, co staccato - rozbraja go scalenie w
jedno zdanie złożone (patrz sekcja 5).

## 5. Scalaj urywane zdania w zdanie złożone

To najsilniejszy polski tell, którego sam de-slop nie łapie. AI po polsku (kalka z angielskiego)
sieka treść na krótkie, osobne zdania (parataksa). Polski znacznie częściej woli jedno zdanie
złożone, podrzędne albo współrzędne (hipotaksa). Gdy dwa-trzy sąsiednie krótkie zdania są ze sobą
logicznie powiązane, scal je w jedno płynne.

To jest też właściwy sposób na "to nie X, to Y": problemem bywa nie kontrast, lecz jego urywana,
dwuzdaniowa forma. Złożenie w jedno zdanie usuwa tell i brzmi naturalnie.

- "Dlatego AI Literacy to nie jest 'wpis do CV'. To jest nowa drabina." ->
  "Dlatego AI Literacy to nie jest już tylko 'wpis do CV', ale dostawienie nowej drabiny w ścieżce
  kariery."
- "A ta nowa zaczyna się od budowania z AI od dnia pierwszego. Od rozwiązywania problemów z agentem
  u boku." ->
  "Nowa droga zaczyna się od budowania z AI każdego dnia od początku i od regularnego rozwiązywania
  problemów z agentem u boku."

Balans: nie scalaj WSZYSTKIEGO w jedno mega-zdanie. Jedno krótkie zdanie dla emfazy jest dobre. Tell
to SERIA urywanych zdań, które proszą się o złożenie. Szukaj sąsiadów, które łączy "ale / bo / więc
/ i / który", i połącz je tym spójnikiem.

## Jak używać

Po przebiegu de-slop puść tekst jeszcze raz pod kątem punktów 1-5. W trybie workflow zrób z tego
osobnego subagenta "recenzent polszczyzny": czyta gotowy wynik i flaguje (a) anglicyzmy do
przetłumaczenia, (b) zdania bez czasownika osobowego albo z frontem przymiotnika, (c)
kalki-przymiotniki, (d) ukryty "nie X, to Y", (e) serie urywanych zdań do scalenia. Żargon autora i
terminy bez polskiego odpowiednika zostają.
