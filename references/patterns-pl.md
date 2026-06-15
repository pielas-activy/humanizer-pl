# Wzorce AI po polsku (PL)

> Ładowane przez router, gdy tekst wejściowy jest po polsku. Polski AI-slop to NIE
> przetłumaczony angielski. GPT i Claude po polsku mają własne tells: kalki z angielskiego,
> nadmiar imiesłowów, bezosobowe przegięcie, klisze otwarcia epoki. Kategoria 6 (kalki i
> klisze) jest najsilniejszym różnicownikiem PL vs EN - bez niej to tylko tłumaczenie listy
> angielskiej.
>
> Źródła: SmartLetter ("Zakazane zwroty dla AI", 500+ fraz), katsin.pl, Mikołaj Abramczuk
> ("ChatGPT który nie wkurza"), Senuto / Top Online. Bank par PRZED/PO: zobacz
> [przyklady.md](./przyklady.md).
>
> Twarde zasady wyjścia: zero myślnika długiego (U+2014) i półpauzy (U+2013), zawsze zwykły
> myślnik ASCII `-`; polskie znaki zachowane; output nie dłuższy niż input; pierwsza linia
> nie jest wypełniaczem.

## Spis treści

- [Jak czytać tę listę](#jak-czytać-tę-listę)
- [Kategoria 1: CONTENT - inflacja znaczenia, name-dropping, mgliste atrybucje](#kategoria-1-content)
- [Kategoria 2: LANGUAGE - AI-słownictwo, nadmiar imiesłowów, kalki](#kategoria-2-language)
- [Kategoria 3: STYLE - myślnik długi, sztuczne pary, anafora dla efektu](#kategoria-3-style)
- [Kategoria 4: COMMUNICATION - artefakty chatbota, wazelina, meta-zapowiedzi](#kategoria-4-communication)
- [Kategoria 5: FILLER / HEDGING - wypełniacze, asekuracja, generyczne konkluzje](#kategoria-5-filler--hedging)
- [Kategoria 6: PL-SPECYFICZNE - kalki z angielskiego + klisze otwarcia](#kategoria-6-pl-specyficzne)
- [Czego NIE flagować (false positives)](#czego-nie-flagować-false-positives)
- [Heurystyka humanizacji po polsku](#heurystyka-humanizacji-po-polsku)

---

## Jak czytać tę listę

Sześć kategorii. Pierwsze pięć mapuje się 1:1 na kategorie blader/humanizer (Content / Language /
Style / Communication / Filler-hedging), więc EN i PL trzymają tę samą strukturę. Szósta jest
tylko polska. Format każdej tabeli: TELL -> AKCJA, gdzie akcja to konkretny zamiennik albo `USUŃ`.

Zasada nadrzędna jak w wersji EN: **przepisuj, nie wycinaj treści**. Usuwasz tell, nie myśl.
Jeśli oryginał ma pięć akapitów, przepisana wersja ma pięć akapitów. Zachowujesz sens, fakty,
liczby i głos autora. Dodajesz konkret tam, gdzie była wata.

---

## Kategoria 1: CONTENT

Inflacja znaczenia, dorabianie wagi, mgliste atrybucje. Model puszy ważność i podpiera się
autorytetem bez nazwiska.

| Tell | Akcja |
|---|---|
| przełomowy, rewolucyjny, innowacyjny, transformacyjny | USUŃ lub zastąp konkretem (co dokładnie robi) |
| kluczowy, istotny, niezwykły, fascynujący | USUŃ (wata bez treści) |
| game-changer, "to zmienia wszystko", "zmiana paradygmatu" | USUŃ, podaj realny efekt z liczbą |
| "Jak pokazują badania" / "liczne badania pokazują" (bez źródła) | USUŃ lub podaj własny konkretny case |
| "Eksperci są zgodni" / "eksperci twierdzą" (bez nazwiska) | USUŃ lub zastąp własną opinią ("Myślę, że") |
| "Content is king", "autentyczność buduje zaufanie" (ogólnik) | USUŃ, zastąp konkretną obserwacją |
| "Według badań 78%..." (zmyślona statystyka) | USUŃ albo podaj realne, źródłowane liczby |

**PRZED:** Jak pokazują liczne badania, firmy wykorzystujące AI osiągają znacząco lepsze wyniki.
Eksperci są zgodni, że to właśnie teraz jest najlepszy moment na inwestycję.

**PO:** U nas wdrożenie AI w obsłudze klienta ścięło czas odpowiedzi z 8 godzin do 40 minut.
Myślę, że u Was efekt byłby podobny, bo macie ten sam wąski gardłowy etap.

---

## Kategoria 2: LANGUAGE

AI-słownictwo, nadmiar imiesłowów, cyklowanie synonimów, kalki leksykalne. Po polsku najmocniej
widać tu nawarstwione imiesłowy ("mając na uwadze", "wykorzystując") i kalki typu "dedykowany".

| Tell | Akcja |
|---|---|
| holistyczny | USUŃ lub "całościowy" tylko jeśli naprawdę potrzebne |
| dedykowany (kalka z "dedicated to") | "skierowany do" / "dla" / USUŃ |
| kompleksowy | "pełny" lub USUŃ |
| niezawodny, ultra-, zaawansowany | USUŃ (słownik promocyjny GPT) |
| "Odkryj...", "Zanurz się...", "Zapomnij o..." | USUŃ (tryb rozkazujący reklamy GPT), przepisz na 1. osobę |
| "dzięki zaawansowanej technologii" | USUŃ, powiedz konkretnie jaka technologia i co robi |
| nadmiar imiesłowów: "mając na uwadze", "wykorzystując", "będąc", "biorąc pod uwagę" | rozbij na osobne zdanie z czasownikiem osobowym |
| "skrojone / szyte na miarę" (kalka "tailored") | "pod Wasz przypadek" lub USUŃ |

**PRZED:** Mając na uwadze Państwa potrzeby i wykorzystując nasze wieloletnie doświadczenie,
pragniemy zaproponować rozwiązanie skrojone na miarę.

**PO:** Mamy propozycję. Patrząc na to, co opisaliście na spotkaniu, największy zysk da Wam
automatyzacja obiegu faktur, bo to ona zjada Wam teraz najwięcej czasu.

---

## Kategoria 3: STYLE

Myślnik długi, sztuczne pary, anafora dla rytmu, ściana zdań wielokrotnie złożonych, nadmiar emoji.

| Tell | Akcja |
|---|---|
| myślnik długi (em-dash, U+2014) i półpauza (en-dash, U+2013) | ZAWSZE zwykły myślnik `-` lub przecinek (twarda zasada) |
| anafora "Bez stresu. Bez wysiłku. Bez ryzyka." / "Bez planu. Bez analizy." | rozbij, zostaw jeden konkret zamiast rytmicznej pustki |
| zdania ciągnące się przez kilka wierszy, wielokrotnie złożone | potnij na krótkie zdania |
| nadmierna, "do bólu" poprawność i symetria | dodaj dygresję, zmianę tempa, potoczny zwrot |
| nadmiar emoji (rakieta, iskierki, ogień, niebieskie romby) | usuń lub zostaw max jeden, jeśli pasuje do głosu |

**PRZED:** Schudnij na lato. Bez diety. Bez wyrzeczeń. Bez wysiłku.

**PO:** Na lato zrzuciłem 6 kilo. Nie katowałem się dietą, po prostu codziennie chodziłem na
godzinny spacer.

### Manufaktura rytmu - dalsze siostry "to nie X, to Y"

Cała rodzina konstrukcji, które brzmią jak AI, bo są mechaniczne. Traktuj je jak "to nie X, to Y":
zacznij od twierdzenia, rozbij powtórzenie, zostaw najwyżej jedno wystąpienie dla emfazy.

| Tell | Akcja / przykład |
|---|---|
| "Nie tylko X, ale (też / również) Y" (ten sam paralelizm) | proste "X i Y": "Nie tylko buduje, ale uczy" -> "Buduje i uczy" |
| doklejona negacja na końcu ("..., bez zgadywania", "..., zero kombinowania") | wpisz w pełne zdanie: "Masz wynik, bez zgadywania" -> "Masz wynik od razu" |
| staccato / sztuczne punchline'y (seria urywanych fragmentów dla dramatu) | scal w 1-2 zdania z treścią: "Wtedy przyszło AI. Bez litości. Koniec." -> "Wtedy przyszło AI i stare założenia przestały działać" |
| unikanie "jest/są" ("stanowi", "służy jako", "jawi się jako", "prezentuje się jako") | wróć do "jest/ma": "Platforma stanowi rozwiązanie" -> "Platforma jest narzędziem do X" |
| formuły-aforyzmy ("X to nowa Y", "X to waluta / język / architektura Z") | zastąp konkretem: "Dane to nowa ropa" -> co dokładnie dają te dane |
| tropy autorytetu ("Prawdziwe pytanie brzmi", "tak naprawdę", "w gruncie rzeczy", "u podstaw leży", "sedno sprawy") | wytnij ceremonię, powiedz wprost |
| fałszywe zakresy ("od X po Y", gdy X i Y nie są skalą: "od startupów po korporacje") | wymień konkrety zamiast udawanego spektrum |
| teatralny otwieracz ("Serio?", "No właśnie.", "Czy warto? Zależy.") | bez pauzy-rewelacji: "To, czy warto, zależy od..." |

---

## Kategoria 4: COMMUNICATION

Artefakty rozmowy z chatbotem wklejone jako treść, wazelina, meta-zapowiedzi zamiast treści.

| Tell | Akcja |
|---|---|
| "Świetne pytanie!" / "Doskonałe pytanie!" | USUŃ |
| "Mam nadzieję, że to pomoże" / "Mam nadzieję, że powyższe okaże się pomocne" | USUŃ |
| "Z przyjemnością się podzielę" / "Oczywiście!" | USUŃ |
| "pozostaję do Państwa pełnej dyspozycji", "dołożymy wszelkich starań" | "jakby co, proszę pisać" / konkret |
| "Celem niniejszego artykułu jest..." / "W niniejszym artykule przyjrzymy się" | USUŃ, zacznij od treści |
| "W kolejnych akapitach postaramy się omówić" (meta-zapowiedź) | USUŃ, po prostu omów |
| "Czy zastanawiałeś się kiedyś, jak..." (ograne pytanie otwierające) | zacznij od konkretu lub mikro-historii |

**PRZED:** Świetne pytanie! Z przyjemnością się tym podzielę. Otóż budowanie agentów AI jest proste,
skuteczne i przyjemne. Mam nadzieję, że to pomoże!

**PO:** Budowanie agentów nie jest trudne, ale wymaga cierpliwości. Pierwszego stawiałem trzy dni
i raz chciałem rzucić monitorem. Czwartego zrobiłem w godzinę.

---

## Kategoria 5: FILLER / HEDGING

Wypełniacze-łączniki, asekuracja, podwójne podsumowania, generyczne konkluzje "ku pamięci".

| Tell | Akcja |
|---|---|
| "Warto zauważyć, że" / "Należy zauważyć, że" / "Należy podkreślić, że" | USUŃ, przejdź do rzeczy |
| "Co więcej", "Co ciekawe", "Ponadto", "Dodatkowo", "Kolejnym aspektem jest" | "Plus", "Poza tym", "I jeszcze jedno", albo USUŃ |
| "W związku z powyższym" / "Ze względu na fakt, że / iż" | "dlatego" / "bo" / USUŃ |
| "Podsumowując" / "Reasumując" / "Reasumując, należy stwierdzić" | USUŃ albo "Wniosek:" + konkret |
| "Podsumowując, warto o tym pamiętać" (banalne zakończenie) | USUŃ, zostaw konkretną radę |
| "Bez wątpienia" / "Nie sposób nie zauważyć, że" | USUŃ |
| asekuracja: "Wydaje się, że", "można przypuszczać", "potencjalnie mogłoby", "w sumie", "realnie" | wytnij hedging, powiedz wprost ("Myślę, że" / stwierdzenie) |
| "wybór, który warto rozważyć" (słaba konkluzja) | USUŃ albo konkretne CTA |

**PRZED:** Podsumowując, warto o tym pamiętać. Reasumując, należy stwierdzić, że omówione kwestie
mają istotne znaczenie. W związku z powyższym, rekomendujemy holistyczne podejście.

**PO:** Wniosek jest jeden: zacznij od jednego procesu, nie od dziesięciu. Zmierz efekt po tygodniu,
potem dokładaj kolejne.

---

## Kategoria 6: PL-SPECYFICZNE

Kalki z angielskiego + klisze otwarcia epoki. **Najważniejsza kategoria dla polskiego.** To ona
odróżnia humanizer-pl od zwykłego tłumaczenia listy angielskiej.

| Tell | Akcja |
|---|---|
| "W dzisiejszych czasach" / "W dzisiejszym świecie" / "We współczesnym świecie" | USUŃ, zacznij od konkretu |
| "W erze cyfrowej" / "W dobie cyfryzacji" / "W dzisiejszym cyfrowym świecie" | USUŃ |
| "W dynamicznie rozwijającym się świecie" / "W dynamicznie zmieniającej się rzeczywistości" | USUŃ |
| "Rosnąca popularność" / "coraz większą rolę odgrywa" | USUŃ lub konkret (o ile wzrosło) |
| kalka "to nie X, to Y" ("to nie luksus, to konieczność"), zwłaszcza gdy POWTARZA się w tekście | przepisz na twierdzenie (zacznij od Y, zdegraduj negację); zostaw max 1 raz na tekst |
| kalka "na koniec dnia" (z ang. "at the end of the day") | "ostatecznie" / "w praktyce" / USUŃ |
| kalka "w tym kontekście" / "w tym zakresie" | USUŃ lub konkretnie o czym mowa |
| kalka "dedykowany", "szyty na miarę", "wartość dodana", "synergistyczny" | polski odpowiednik lub USUŃ |
| rule of three: trzy przymiotniki w rzędzie ("prosty, skuteczny i przyjemny") | zostaw jeden najmocniejszy |
| "Z jednej strony... z drugiej strony" (gdy nie ma realnej kontry) | USUŃ, zajmij stanowisko |
| "Po pierwsze... Po drugie... Po trzecie" (porządek dla porządku) | numeruj tylko gdy kolejność ma znaczenie |
| brak lokalnego kontekstu (przykłady oderwane od polskich realiów) | podmień na polski kontekst (PLN, polskie firmy, polskie systemy) |

**PRZED:** W dzisiejszych czasach, w dynamicznie rozwijającym się świecie gastronomii, jakość
obsługi staje się kluczowym elementem sukcesu każdej restauracji. To nie luksus, to konieczność.

**PO:** Wczoraj skróciłem czas wydania dania z 25 do 12 minut, zmieniając kolejność pracy na
kuchni. I to dopiero pierwsza z pięciu zmian, które mam w planie.

**Powtórzony "to nie X, to Y" (zacznij od twierdzenia):** gdy ten sam szablon wraca 3-4 razy w
tekście, to manufaktura rytmu, nie głos. Przepisz większość, zostaw najwyżej jeden raz.

- "Trudna część to nie gotowanie. To wiedza, CO ugotować." -> "Najtrudniej jest wiedzieć, CO
  ugotować. Samo gotowanie jest łatwe."
- "Dobry trening to nie ciężary. To regularność." -> "Dobry trening robi przede wszystkim
  regularność, nie same ciężary."
- "W sprzedaży najważniejsza nie jest cena, to zaufanie." -> "W sprzedaży najważniejsze jest
  zaufanie, nie cena."

---

## Czego NIE flagować (false positives)

Czysty, ludzki polski tekst potrafi trafić w kilka wzorców z tej listy bez udziału AI. Zanim
przepiszesz, sprawdź, czy nie psujesz dobrej prozy. Same w sobie NIE są dowodem na AI:

- **Poprawna gramatyka i ogonki.** Ktoś po prostu dba o język albo był redagowany. Poprawność to
  nie AI.
- **Formalny rejestr w mailu do klienta.** "Dzień dobry", "Pozdrawiam", "Państwo" to normy
  grzecznościowe, nie tells. Tellem jest dopiero wazelina ("dołożymy wszelkich starań", "pozostaję
  do pełnej dyspozycji").
- **Jeden imiesłów albo jeden łącznik.** "Patrząc na to" raz w tekście jest OK. Tellem jest
  nawarstwienie ("mając na uwadze... wykorzystując... biorąc pod uwagę").
- **Pojedynczy konkret branżowy albo liczba.** To sygnał człowieka, nie wata. Nie wycinaj.
- **Krótkie, urwane zdanie dla emfazy.** Jedno jest ludzkie. Tellem jest dopiero seria ("Bez
  stresu. Bez wysiłku. Bez ryzyka.").
- **Fachowe słownictwo.** AI nadużywa KONKRETNYCH słów-waty (holistyczny, dedykowany), nie każdego
  trudnego słowa. Nie spłaszczaj "amortyzacja" czy "ekspozycja" tylko dlatego, że brzmią mądrze.

Szukaj SKUPISK tells, nie pojedynczych. Jeden imiesłów nic nie znaczy; imiesłów plus rule of three
plus "w dzisiejszych czasach" plus "holistyczne podejście" to już przyznanie się. Pełny guard z
sygnałami ludzkiego pisania jest w [patterns-en.md](./patterns-en.md) w sekcji "What NOT to flag"
i obowiązuje też dla polskiego.

---

## Heurystyka humanizacji po polsku

Widoczna w każdej parze PO z banku. Cztery ruchy, które robią z polskiego AI-slopu tekst ludzki:

1. **Konkret + liczba zamiast waty.** "Skrócił czas z 3 godzin do 20 minut" zamiast "znacząco
   usprawnia procesy".
2. **Pierwsza osoba zamiast bezosobowego.** "Wdrożyłem", "Myślę, że" zamiast "zostało wdrożone",
   "można przypuszczać".
3. **Szczerość zamiast gładkiej promocji.** Przyznanie porażki ("raz chciałem rzucić monitorem"),
   uczciwe "reszta podobna, nie będę ściemniać".
4. **Polski kontekst.** PLN zamiast dolarów, Fakturownia / wFirma zamiast generycznych nazw,
   polskie realia zamiast kalek.

Nie zmieniaj języka tekstu, nie tłumacz. Jeśli ktoś prosi o humanizację polskiego tekstu, wynik
jest po polsku, z pełnymi ogonkami i bez myślnika długiego.
