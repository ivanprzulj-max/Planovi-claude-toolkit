# Pravila formatiranja studije — potpuna referenca

Ova pravila proizlaze iz REGEA predloška (`assets/Studija_predlozak.docx`). Cilj je da svaka studija izgleda konzistentno i profesionalno, spremna za dvostrani ispis i predaju naručitelju. Uz svako pravilo navedeno je i *zašto*, da se ispravno postupi i u rubnim situacijama.

## 1. Stilovi teksta

Svi stilovi postoje SAMO u predlošku. Tehnički detalji (kako su definirani u styles.xml):

| Style | Font | Veličina | Ostalo |
|---|---|---|---|
| Normal | Calibri | 11 pt | prored 1,0 (`line=240`), `spacing after=0`, poravnanje obostrano (justify) |
| Heading 1 | Calibri | 14 pt | bold, numeriran (razina 0, numId 13), `spacing after=240` (razmak prema tekstu), keepNext |
| Heading 2 | Calibri | 12 pt | bold, numeriran (razina 1 → npr. 4.2), `before=200 after=240` |
| Heading 3 | Calibri | 11 pt | bold, numeriran (razina 2 → npr. 4.2.1), `after=240` |
| Caption | Calibri | 11 pt | bold (samo dio "Slika X.Y" ostaje bold — naziv se piše u ne-bold runu) |
| Small | Calibri | 10 pt | za izvore podataka ispod tablica i slika |
| Naslov studije | Arial | 24 pt | samo za naslovnicu (izdavač, adresa) |
| List Paragraph | Calibri | 11 pt | za bulete i numerirane liste |

Nikad ne primjenjuj izravno formatiranje (ručni bold/size) tamo gdje postoji stil — stilovi omogućuju TOC, STYLEREF i konzistentne izmjene.

## 2. Naslovi i numeracija poglavlja

- Heading 1–3 su automatski numerirani kroz višerazinsku listu predloška (numId 13). NE upisuj brojeve poglavlja ručno u tekst naslova ("4. Analiza" je pogrešno — samo "Analiza" sa stilom Heading 1).
- Svaki Heading 1 mora početi na **neparnoj stranici** (radi dvostranog ispisa). Tehnika: section break tipa *Odd Page* prije naslova (`w:sectPr` s `w:type w:val="oddPage"`), ili zadržati postojeće prazne stranice predloška. Helper `h1_na_neparnoj()` to radi automatski.
- Iza svakog naslova slijedi razmak prema tekstu — to rješava `spacing after` u stilu, ne prazan odlomak. Ne umeći prazne Normal odlomke iza naslova.

## 3. Slike i captioni

- Caption ide **ISPOD** slike (Wordova opcija *Below selected item*).
- Format: `Slika X.Y Naziv slike` — "Slika X.Y" **bold**, naziv **ne-bold**, sve Calibri 11.
- X = broj poglavlja (Heading 1), Y = redni broj slike u tom poglavlju. Npr. četvrta slika u 2. poglavlju = *Slika 2.4*.
- Tehnička izvedba poljima (identično Insert Caption s "Include chapter number"):
  - `{ STYLEREF 1 \s }` — dohvaća broj tekućeg Heading 1
  - `.`
  - `{ SEQ Slika \* ARABIC \s 1 }` — brojač koji se resetira na svakom Heading 1
- Slika mora biti centrirana; caption također centriran ili lijevo — slijedi predložak (Caption je baziran na Normal → obostrano; za caption postavi lijevo poravnanje).
- Ispod captiona (ili ispod slike ako nema izvora u captionu) ide izvor u stilu **Small**: `Izvor: …`.

## 4. Tablice i captioni tablica

- Caption ide **IZNAD** tablice (*Above selected item*), inače sve isto kao za slike; SEQ brojač je `Tablica`.
- Font u tablici: **Calibri 10**. Za velike tablice koje ne stanu dopušteno 9 ili 8 pt — nikad ne dopusti da tablica izlazi izvan margina.
- Poravnanje ćelija: **brojevi centrirano**, **opisni tekst lijevo**. Heuristika za autodetekciju: ćelija čiji sadržaj (nakon uklanjanja razmaka, %, €, kn) odgovara hrvatskom formatu broja → centriraj; ostalo lijevo. Zaglavlje tablice: bold, centrirano.
- Ispod tablice: izvor u stilu **Small**.
- Redak zaglavlja označi kao "repeat as header row" ako se tablica proteže na više stranica.

## 5. Brojevi

- Hrvatski poslovni format **bez točke za tisućice**: razmak kao separator tisućica, zarez za decimale.
  - Ispravno: `1 586 278,85` · `12 500` · `3,14`
  - Pogrešno: `1.586.278,85` · `1,586,278.85` · `1586278.85`
- U idealnom slučaju koristiti neprelomivi razmak (U+00A0) između tisućica da se broj ne prelomi na kraju retka.
- Pravilo vrijedi u tekstu, tablicama i captionima. Postoci: `25 %` ili `25%` — slijedi postojeću praksu dokumenta, budi konzistentan.

## 6. Navodnici i isticanje

- Navodni znakovi („primjer", "primjer", »primjer«) se **ne koriste**. Nazivi programa, dokumenata, projekata, citirani pojmovi → *Italic*.
- Iznimke: navodnici unutar doslovnih citata propisa/zakona mogu ostati ako je riječ o pravnom citatu — u dvojbi pitaj korisnika.

## 7. Buleti i liste

- Sve razine buleta/numeracija moraju biti **poravnate** (konzistentne uvlake kroz cijeli dokument — koristi List Paragraph stil, ne ručne uvlake).
- Bulete koristiti samo ako lista ima **3 ili više** točaka; za 1–2 točke preformuliraj u rečenicu.
- Lista ne smije ružno prelamati preko stranice: po potrebi `keep with next` na točkama liste.

## 8. Struktura dokumenta i numeracija stranica

Redoslijed: **Naslovnica → (prazna str. za dvostrani ispis) → Sadržaj → [Popis tablica, Popis slika, Popis kratica po potrebi] → SECTION BREAK → Sažetak → Uvod → poglavlja…**

- Numeracija stranica **počinje od Uvoda** (odnosno prve sekcije nakon section breaka; u predlošku footer s brojem stranice postoji tek u kasnijim sekcijama). Naslovnica i Sadržaj nemaju brojeve stranica.
- Iza Sadržaja obavezan **Section break** — bez njega numeracija ne može krenuti od Uvoda.
- **Studije > 100 stranica**: iza Sadržaja dodaj *Popis tablica* i *Popis slika* (generiraju se TOC poljima nad SEQ Tablica / SEQ Slika: `{ TOC \h \z \c "Tablica" }` odnosno `\c "Slika"`).
- **Veći broj kratica**: iza Sadržaja dodaj *Popis kratica* (dvostupčana tablica bez obruba: kratica | puni naziv, abecedno).
- Sadržaj (TOC) i sva polja korisnik mora osvježiti u Wordu: Ctrl+A → F9, odnosno desni klik na Sadržaj → *Update Field → Update entire table*. To UVIJEK napomeni pri isporuci.

## 9. Naslovnica

Zadrži elemente predloška: Naručitelj (Republika Hrvatska / Županija / Grad / Općina), Veza (broj ugovora i datum), NAZIV STUDIJE, blok izdavača (REGEA, Andrije Žaje 10, 10 000 Zagreb, http://www.regea.org, stil *Naslov studije*), mjesto i datum ("Zagreb, mjesec godina."). Popuni stvarnim podacima iz zadatka; ako podaci nedostaju, ostavi predloškove oznake i upozori korisnika.

## 10. Kontrola kvalitete prije isporuke

Pokreni `scripts/provjeri_studiju.py`. Kritični nalazi (moraju biti 0):
- korišten stil izvan predloška / ručno numeriran naslov
- navodnici u tekstu
- broj s točkom-tisućicama
- caption tablice ispod tablice ili caption slike iznad slike
- nedostaje section break iza Sadržaja
- tablica s fontom > 10 pt

Upozorenja (razmotri, ne blokiraju): liste s < 3 točke, dugi naslovi, tablice bez izvora, H1 koji možda nije na neparnoj stranici.
