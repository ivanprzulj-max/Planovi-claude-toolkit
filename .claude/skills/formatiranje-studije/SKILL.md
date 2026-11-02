---
name: formatiranje-studije
description: Izrada i formatiranje studija, elaborata i stručnih izvještaja u Word (.docx) formatu prema REGEA predlošku i pravilima formatiranja (Calibri, numerirani Heading 1-3, captioni slika i tablica vezani uz poglavlja, Section break iza Sadržaja, numeracija stranica od Uvoda). Koristi OBAVEZNO kad korisnik traži izradu nove studije, formatiranje ili preformatiranje postojećeg dokumenta studije, provjeru usklađenosti s predloškom, ili spominje "studija", "elaborat", "REGEA predložak", "formatiraj prema predlošku", "prebaci u naš format", "sredi dokument za predaju", "captioni slika/tablica", i slično — čak i ako ne kaže izričito "formatiranje". Vrijedi i za nove dokumente i za doradu postojećih .docx datoteka.
---

# Formatiranje studije (REGEA predložak)

Ovaj skill osigurava da svaka studija/elaborat nastane **unutar predloška** `assets/Studija_predlozak.docx` i poštuje sva pravila formatiranja. Stilovi (Heading 1–3, Normal, Small, Caption, Naslov studije), višerazinska numeracija naslova i struktura sekcija definirani su **samo u tom predlošku** — izrada studije u novom/praznom Word dokumentu NEĆE zadržati stilove. Zato je prvo pravilo:

> **Uvijek kopiraj predložak i radi u kopiji. Nikad ne kreiraj `Document()` ispočetka.**

## Tijek rada

### A) Nova studija iz sadržaja

1. Pročitaj `references/pravila-formatiranja.md` (kompletna pravila s obrazloženjima).
2. Kopiraj `assets/Studija_predlozak.docx` u radni direktorij pod ciljanim imenom.
3. Otvori kopiju s python-docx i koristi pomoćne funkcije iz `scripts/studija_helpers.py` (import ili copy-paste funkcija). One rješavaju: captione s poljima STYLEREF/SEQ, hrvatski format brojeva, formatiranje tablica, izvore (style Small), section break i H1 na neparnoj stranici.
4. Popuni naslovnicu (Naručitelj, naziv studije, datum), zadrži strukturu sekcija predloška (naslovnica → Sadržaj → section break → Sažetak → glavni dio).
5. Ukloni instrukcijski tekst predloška ("Upute kako formatirati studiju" i povezane bulete) — to su upute autoru, ne sadržaj studije.
6. Dodaj sadržaj koristeći ISKLJUČIVO stilove predloška: `Heading 1/2/3`, `Normal`, `Small`, `Caption`, `List Paragraph`.
7. Pokreni `python scripts/provjeri_studiju.py <datoteka.docx>` i ispravi sve nalaze prije isporuke.

### B) Preformatiranje postojećeg dokumenta

Postojeći dokument gotovo sigurno NEMA ispravne stilove, pa prebacivanje "in-place" ne funkcionira. Umjesto toga:

1. Pročitaj `references/pravila-formatiranja.md`.
2. Ekstrahiraj sadržaj izvornog dokumenta (tekst, hijerarhiju naslova, tablice, slike iz `word/media/`).
3. Kopiraj predložak i **prenesi sadržaj u kopiju predloška**, mapirajući: naslovi poglavlja → Heading 1, podnaslovi → Heading 2/3, tekst → Normal, izvori → Small.
4. Pri prijenosu primijeni transformacije: makni navodnike → Italic, formatiraj brojeve, centriraj brojeve u tablicama, dodaj/popravi captione.
5. Pokreni provjeru (`provjeri_studiju.py`) i ispravi nalaze.

### C) Provjera usklađenosti (bez izmjena)

Pokreni `scripts/provjeri_studiju.py` na dokumentu i prezentiraj izvještaj korisniku po kategorijama (kritično / upozorenje), s brojem stranice/odlomka gdje je problem.

## Sažetak pravila (potpuna verzija u references/)

| Element | Pravilo |
|---|---|
| Osnovni tekst | style **Normal** — Calibri 11, prored 1,0, obostrano poravnanje |
| Glavni naslov | style **Heading 1** — bold, Calibri 14, numeriran, razmak nakon naslova; svaki H1 na **neparnoj stranici** |
| Podnaslov | style **Heading 2** — bold, Calibri 12, numeracija podređena H1 (npr. 4.2) |
| Dodatni podnaslov | style **Heading 3** — bold, Calibri 11, numeracija podređena H2 (npr. 4.2.1) |
| Caption slike | **ISPOD** slike; "Slika X.Y" bold + naziv ne-bold, Calibri 11; X = broj poglavlja (STYLEREF), Y = SEQ |
| Caption tablice | **IZNAD** tablice; ista pravila kao slike, SEQ "Tablica" |
| Izvor podataka | uvijek ispod tablice/slike, style **Small** (Calibri 10), npr. *Izvor: DZS, 2025.* |
| Tablice | font Calibri 10 (manji ako ne stane); brojevi **centrirani**, opisni tekst **lijevo** |
| Brojevi | bez točke za tisućice, razmak kao separator, zarez za decimale: `1 586 278,85` |
| Navodnici | ne koriste se — umjesto „primjer" piši *primjer* (Italic) |
| Buleti | poravnati, izbjegavati ako nema ≥ 3 točke; ne razlamati listu preko stranica |
| Numeracija stranica | počinje od **Uvoda**; iza Sadržaja obavezan **Section break** |
| Opseg > 100 str. | iza Sadržaja dodati Popis tablica i Popis slika (s br. stranica) |
| Puno kratica | iza Sadržaja dodati Popis kratica |

## Pomoćne skripte

`scripts/studija_helpers.py` — funkcije za rad s python-docx unutar predloška:

- `kopiraj_predlozak(odrediste)` — kopira predložak (jedini ispravan početak)
- `hr_broj(x, decimale=2)` — `1586278.85` → `"1 586 278,85"`
- `dodaj_caption_slike(doc_ili_parent, naziv)` / `dodaj_caption_tablice(...)` — umeće odlomak stila Caption s poljima `STYLEREF 1 \s` + `SEQ Slika/Tablica \* ARABIC \s 1` (identično Wordovom Insert Caption vezanom uz poglavlje); "Slika X.Y" bold, naziv ne-bold
- `dodaj_izvor(parent, tekst)` — odlomak stila Small ("Izvor: …")
- `formatiraj_tablicu(table)` — Calibri 10, brojevi centrirani / tekst lijevo (autodetekcija po ćeliji), header bold
- `h1_na_neparnoj(doc)` — umeće section break (odd page) prije svakog Heading 1
- `italic_umjesto_navodnika(paragraph)` — zamjenjuje „…"/"…" kurzivom

Nakon svake izrade/izmjene:

```bash
python scripts/provjeri_studiju.py izlaz.docx
```

Skripta provjerava: korištenje predloškovih stilova, fontove i veličine, navodnike u tekstu, format brojeva (točka-tisućice), poziciju captiona (slika ispod / tablica iznad), postojanje section breaka iza Sadržaja, H1 na neparnim stranicama (aproksimativno preko section breakova) i poravnanje tablica. Ispisuje nalaze s lokacijom. **Nijedan dokument ne isporučuj s kritičnim nalazima.**

## Važne napomene

- Polja (TOC, STYLEREF, SEQ) python-docx ne izračunava — u dokumentu su ispravna, ali brojevi se prikazuju tek nakon što korisnik u Wordu napravi *Update Field / Update entire table* (Ctrl+A → F9). Uvijek to napomeni korisniku pri isporuci, uključujući "Update entire table" za Sadržaj.
- Prazne stranice u predlošku ("Ova prazna stranica dodana je…") služe dvostranom ispisu — zadrži logiku neparnih stranica, ali ukloni instrukcijski tekst.
- Ako korisnik da sadržaj bez jasne hijerarhije, predloži strukturu poglavlja prije generiranja umjesto da pogađaš.
- Za velike tablice smanji font (9 ili 8 pt) umjesto da tablica prelomi margine.
- Sve dorade rade se na kopiji predloška ili na već usklađenoj studiji — nikad ne "prepravljaj stilove" tuđeg dokumenta jer numeracija naslova (numId 13) postoji samo u predlošku.
