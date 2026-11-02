---
name: pgh-protokol
description: Zajednički protokol razmjene za lanac agenata koji izrađuje Plan grijanja i hlađenja (PGH) — struktura radnog direktorija, shema radnog artefakta, registar pretpostavki, oznake kvalitete podataka, kapije odobrenja, pravila pisanja u Master Sheet i SharePoint, hrvatske konvencije zapisa. Učitava se u svakog PGH agenta. Koristi kad se radi na planu grijanja i hlađenja u lancu agenata.
---

# PGH protokol razmjene

Ovaj protokol je zajednički svim agentima u lancu izrade PGH-a. On ne opisuje *što* koji agent
analizira — to je u definiciji svakog agenta — nego **kako se rezultati predaju dalje**.

**Razlog postojanja:** subagenti ne dijele kontekst. Svaki starta prazan i glavnoj sesiji vraća
samo sažetak. Ako bi sljedeći agent radio na osnovi prepričanog sažetka, brojke bi tiho mutirale.
Zato je **jedini kanal razmjene datoteka na disku**, u shemi propisanoj ovdje.

---

## 1. Radni direktorij

```
gradovi/<grad>/
├── ulazi/                    # upitnici i sirovi ulazi grada (read-only za sve agente)
├── master-sheet/             # snapshot Master Sheeta + zapis verzije
├── radni/                    # artefakti agenata (jedini kanal razmjene)
│   ├── podaci/
│   ├── tehnicki/
│   ├── financijski/
│   ├── pravni/
│   └── prostorni/            # GIS: slojevi, karte, trase (pgh-prostorni)
├── plan/                     # radna verzija .docx
├── revizija/                 # nalazi kontrolora, registri brojki
└── ODLUKE.md                 # dnevnik kapija i odluka korisnika
```

Konačni Plan i Master Sheet žive na **dijeljenoj SharePoint lokaciji (Project ESCALATE)**.
Lokalni direktorij je radni prostor, nikad kanon.

### Snapshot Master Sheeta
Master Sheet se s SharePointa povlači **jednom po ciklusu** i sprema kao
`master-sheet/MS_<grad>_<YYYY-MM-DD>_v<n>.xlsx`, uz `master-sheet/VERZIJA.md`
(datum povlačenja, naziv izvorne datoteke, tko ju je zadnji mijenjao).
Svi analitičari rade nad **istim snapshotom**. Nitko ga ne mijenja.
Ako ti snapshot nedostaje — to je zaustavljanje, ne prilika za pretpostavku.

---

## 2. Shema radnog artefakta

Svaki agent piše u `radni/<agent>/<poglavlje>.md` po ovoj shemi. Bez iznimke.

```markdown
# <naziv poglavlja iz predloška>
AGENT:     pgh-tehnicki
GRAD:      <grad>
SNAPSHOT:  MS_<grad>_2026-08-25_v14.xlsx
STATUS:    nacrt | za kapiju | odobreno
DATUM:     2026-08-25

## TEKST
<gotov hrvatski tekst za plan — proza koju pisac preuzima gotovo doslovno>

## TABLICE
### T1 — <naziv>
| ... |
Izvor: <MS!List!raspon ili vanjski izvor s godinom>   Kvaliteta: [M] / [P] / [O]

## PRETPOSTAVKE
| ID | Veličina | Vrijednost | Jedinica | Izvor / metoda | Osjetljivost |
|----|----------|-----------|----------|----------------|--------------|
| P-TEH-07 | ... | ... | ... | ... | ±x % → učinak |

## IZVORI
- <naziv, izdavač, godina, poveznica ili MS referenca>

## OTVORENE STAVKE
- <što nedostaje> | tražiti od: <grad / HEP / HERA> | polje u upitniku: <točan naziv>

## PREDAJA
- <agentu> potrebno: <što točno i gdje se nalazi>
```

### Nepovrediva pravila sheme
- **Nema brojke bez podrijetla.** Svaka brojka u `TEKST` i `TABLICE` mora se dati pratiti do
  ćelije Master Sheeta (`MS!List!ćelija`), do ID-a pretpostavke (`P-XXX-nn`) ili do citiranog
  vanjskog izvora s godinom. Brojka bez toga je *orphan number* i pisac je odbija preuzeti.
- **ID pretpostavke je trajan.** Jednom dodijeljen ID se ne mijenja ni ne reciklira. Prefiksi:
  `P-POD-` (podaci), `P-TEH-` (tehnički), `P-FIN-` (financijski), `P-PRA-` (pravni),
  `P-PRO-` (prostorni / GIS).
- **Oznaka kvalitete uz svaku tablicu i svaku brojku koja nije mjerena:**
  `[M]` mjereni podatak · `[P]` modelirana procjena (uz referencu na metodu)
  `[O]` otvorena stavka (nedostaje, nije popunjeno).
  Modelirana vrijednost prikazana bez oznake je greška, ne stilski propust.
- **Otvorena stavka se nikad ne popunjava uvjerljivom vrijednošću.** Ili je označena kao `[P]`
  s metodom kompenzacije, ili ostaje `[O]`.
- **Nikad ne prepisuješ tuđi artefakt.** Ako trebaš izmjenu tuđeg poglavlja, upiši je u vlastiti
  artefakt pod `PREDAJA` i imenuj agenta.

---

## 3. Kapije odobrenja

Lanac staje na tri mjesta. Agent koji dođe do kapije **ne nastavlja dalje**, nego vraća sažetak
glavnoj sesiji i staje. Odluku korisnika glavna sesija upisuje u `ODLUKE.md`.

| Kapija | Kad | Tko je do tada radio | Što se odobrava |
|---|---|---|---|
| **K1 — Ulazi** | prije modeliranja | pgh-podaci | inventar podataka, popis rupa, predložene metode kompenzacije, zahtjev prema gradu |
| **K2 — Scenariji** | prije pisanja | pgh-tehnicki, pgh-financijski, pgh-pravnik, pgh-prostorni | izbor scenarija, kombinacija izvora, dinamika, pravna izvedivost |
| **K3 — Isporuka** | prije slanja gradu | pgh-pisac, pgh-kontrolor | nalaz kontrolora bez blokirajućih stavki |

---

## 4. Pisanje u Master Sheet i SharePoint

Master Sheet je **jedini izvor brojčane istine**, pa je i redoslijed ispravaka strog:
**prvo Master Sheet, pa plan.** Nikad obrnuto, nikad samo jedno.

Ali nijedan agent ne mijenja Master Sheet po vlastitoj odluci:

1. Agent koji uoči potrebu za izmjenom **ne upisuje** je, nego je predlaže u vlastitom artefaktu
   pod `PREDAJA` i u zbirnoj datoteci `radni/podaci/master-sheet-prijedlozi.md`
   (jedan redak: list · ćelija · stara vrijednost · nova vrijednost · izvor · razlog).
2. Glavna sesija provjerava prijedloge i sažima ih korisniku — **sažeto: što se mijenja, zašto,
   i što se u planu pomiče zbog toga.**
3. Tek nakon izričitog odobrenja korisnika, upis izvodi **isključivo `pgh-podaci`**.
4. Svaki upis dobiva zapis u zasebnom listu `LOG_IZMJENA`:
   `datum · agent · list · ćelija · stara → nova · izvor · odobrio`.
   List se stvara ako ne postoji. Zapis se dodaje, nikad ne prepisuje.
5. Veća izmjena u planu (.docx) označava se **Wordovim komentarom** na mjestu izmjene
   (autor: naziv agenta), a ne izmjenom teksta bez traga.

**Bez odobrenja se ne piše ništa na SharePoint.** Povlačenje (čitanje) je slobodno.

---

## 5. Hrvatske konvencije

- Brojevi: `1 586 278,85` — razmak za tisućice, zarez za decimale. Nikad točka za tisućice.
- Jedinice uvijek uz brojku; energija u MWh ili GWh dosljedno kroz cijeli plan, snaga u MW.
- Razlikuj i uvijek imenuj: **isporučena** vs **proizvedena** toplina; **primarna** vs
  **neposredna (finalna)** energija; **MW toplinski** vs **MW električni**.
- Radni jezik svih artefakata i plana je **hrvatski**. Prijevod je zaseban posao, ne usputni.
- Navodnici se ne koriste — umjesto njih kurziv.

---

## 6. Pamćenje (za agente koji ga imaju)

Pamtiš **pravila i obrasce**, nikad **brojke**.

- Pamti: metode kompenzacije koje su prošle reviziju, izvore koji se pokazali korisnima,
  ponavljajuće greške, lažne pozitive, gdje stoje predlošci i referentne datoteke.
- Ne pamti: nijednu vrijednost iz gradskog dokumenta, nijedan prag propisa ili KPI-a, nijednu
  cijenu, nijedno osobno ime. Zapamti *gdje piše*, nikad *što piše*.
- Zapamćena brojka zastari, a onda je počneš koristiti kao referencu umjesto kanona — to je
  najizravniji put do lažnog nalaza i krivog poglavlja.
- Najviše 3 nove stavke po ciklusu. `MEMORY.md` drži ispod 200 redaka; detalje seli u podmape.

---

## 7. Python okruženje

Netrivijalne izračune radi u Pythonu, ne napamet. **Prije poziva biblioteke provjeri je li
instalirana** i ne izmišljaj nazive funkcija:

```bash
python3 -c "import openpyxl, docx, pandas, numpy, scipy; print('OK')"
```

- `.xlsx` čitaj dvaput: `openpyxl.load_workbook(..., data_only=False)` za formule i
  `data_only=True` za vrijednosti. Razlika među njima je čest izvor nalaza.
- Ako `numpy_financial` ili `pulp` nedostaju: anuitet, NPV i IRR implementiraj izravno,
  a optimizaciju vodi greedy postupkom ili preko `scipy.optimize.linprog`.
