# Raport HTML: side-by-side + lista zmian (tryb opcjonalny)

> Wczytywane tylko gdy user prosi o raport HTML / diff / podświetlenie zmian. Generujesz jeden
> samodzielny plik `.html` (inline CSS, zero zależności), który pokazuje oryginał i wynik obok
> siebie z podświetlonymi zmianami, plus tabelę zmian z powodami. To dodatek, nie zamiennik
> zwykłego before/after w czacie.

## Kiedy

User mówi np.: "raport HTML", "pokaż zmiany side by side", "raport zmian", "diff HTML",
"podświetl zmiany", "zhumanizuj + raport". Bez takiej prośby tego nie generujesz.

## Co generujesz

1. **Nagłówek**: tytuł + meta (wykryty język, liczba zmian).
2. **Side-by-side**: dwie kolumny, akapit w akapit. Lewa = oryginał, prawa = wynik.
   - W oryginale podświetlasz to, co znika albo się zmienia: `<span class="del">...</span>`.
   - W wyniku podświetlasz to, co dochodzi albo się zmienia: `<span class="add">...</span>`.
   - Podświetlaj na poziomie FRAZY, nie całych akapitów. Niezmieniony tekst zostaje bez klasy.
3. **Tabela zmian**: jeden wiersz na zmianę - fragment przed, fragment po, typ tellu
   (np. myślnik długi, "to nie X, to Y", kalka, zdanie bez czasownika, rule of three), krótki powód.

## Zasady

- Plik samodzielny: cały CSS inline w `<style>`, żadnych linków ani fontów z sieci.
- Jasny, czytelny motyw. Podświetlenia stonowane: usunięte = czerwonawe tło + przekreślenie,
  dodane = zielonkawe tło. Bez jaskrawości.
- Zero myślnika długiego w samym raporcie (twarda zasada skilla obowiązuje też tu).
- Treść raportu w języku tekstu (PL dla PL).
- Liczba wierszy tabeli = liczba realnych zmian. Nie dubluj, nie pomijaj.
- Po zapisaniu podaj userowi ścieżkę do pliku.

## Szablon

Wypełnij placeholdery `{{...}}`. Powtórz `<p>` w kolumnach tyle razy, ile akapitów; `<tr>` tyle
razy, ile zmian.

```html
<!DOCTYPE html>
<html lang="{{lang}}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Raport zmian - humanizer-pl</title>
<style>
  :root{
    --bg:#fafafa; --card:#ffffff; --ink:#1a1a1a; --muted:#6b6b6b; --line:#e6e6e3;
    --del-bg:#fbe9e7; --del-ink:#9b2c1a; --add-bg:#e7f4ea; --add-ink:#1e6b3a; --head:#f3f2ef;
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    line-height:1.6;}
  .wrap{max-width:1100px;margin:0 auto;padding:32px 24px 64px;}
  h1{font-size:1.4rem;margin:0 0 4px;}
  .meta{color:var(--muted);font-size:.9rem;margin:0 0 24px;}
  .cols{display:grid;grid-template-columns:1fr 1fr;gap:16px;}
  .col{background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden;}
  .col h2{font-size:.8rem;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);
    margin:0;padding:12px 18px;background:var(--head);border-bottom:1px solid var(--line);}
  .col .inner{padding:6px 18px 18px;}
  .col p{margin:14px 0;}
  .del{background:var(--del-bg);color:var(--del-ink);border-radius:3px;padding:0 2px;
    text-decoration:line-through;}
  .add{background:var(--add-bg);color:var(--add-ink);border-radius:3px;padding:0 2px;}
  h3{font-size:1.05rem;margin:36px 0 10px;}
  table{width:100%;border-collapse:collapse;background:var(--card);
    border:1px solid var(--line);border-radius:12px;overflow:hidden;font-size:.92rem;}
  th,td{text-align:left;padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top;}
  th{background:var(--head);font-size:.78rem;text-transform:uppercase;letter-spacing:.03em;
    color:var(--muted);}
  td.was{color:var(--del-ink);} td.now{color:var(--add-ink);}
  .type{white-space:nowrap;color:var(--muted);}
  @media(max-width:720px){.cols{grid-template-columns:1fr;}}
</style>
</head>
<body>
<div class="wrap">
  <h1>Raport zmian - humanizer-pl</h1>
  <p class="meta">Jezyk: {{lang}} | Zmian: {{liczba_zmian}}</p>

  <div class="cols">
    <div class="col">
      <h2>Oryginal</h2>
      <div class="inner">
        <p>{{akapit z <span class="del">usunietymi</span> fragmentami}}</p>
        <!-- ...kolejne akapity... -->
      </div>
    </div>
    <div class="col">
      <h2>Po humanizacji</h2>
      <div class="inner">
        <p>{{akapit z <span class="add">nowymi</span> fragmentami}}</p>
        <!-- ...kolejne akapity... -->
      </div>
    </div>
  </div>

  <h3>Lista zmian</h3>
  <table>
    <tr><th>#</th><th>Bylo</th><th>Jest</th><th>Typ</th><th>Dlaczego</th></tr>
    <tr>
      <td>1</td>
      <td class="was">{{fragment przed}}</td>
      <td class="now">{{fragment po}}</td>
      <td class="type">{{typ tellu}}</td>
      <td>{{krotki powod}}</td>
    </tr>
    <!-- ...kolejne wiersze... -->
  </table>
</div>
</body>
</html>
```

## Gdzie zapisać

Domyślnie obok źródła albo tam, gdzie user wskaże; nazwa typu `raport-zmian-{slug}.html`.
