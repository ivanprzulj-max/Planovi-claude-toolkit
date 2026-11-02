---
title: "PGH toolkit — upute za korištenje"
subtitle: "Skillovi i agenti za izradu, reviziju i analitiku Planova grijanja i hlađenja"
author: "REGEA — Odjel OIE"
date: "Studeni 2026., verzija 1.0"
lang: hr
toc-title: "Sadržaj"
---

# Čemu služi ovaj paket

PGH toolkit je skup **skillova** (pisanih uputa koje Claude učitava kad radi određeni posao) i
**agenata** (specijaliziranih pomoćnika koji rade jedan dio plana) za izradu Planova grijanja i
hlađenja prema čl. 25. Direktive (EU) 2023/1791, metodologiji projekta ESCALATE i REGEA predlošku.

Sve u paketu nastalo je na **Planu G&H Grada Karlovca** (prvi plan te vrste u Hrvatskoj). Paket
prenosi *način rada*, a ne brojke: svaki grad ima vlastitu Master tablicu i vlastite podatke.

Paket ne zamjenjuje stručnu prosudbu. Claude priprema, računa, piše i kontrolira — vi odlučujete
na tri kapije (K1, K2, K3) i odobravate svaki upis u Master tablicu.

## Što je u paketu

**Skillovi** (mapa `.claude/skills/`):

| Skill | Čemu služi |
|---|---|
| `hc-plan-creator` | izrada (DRAFT), revizija (REVISE) i provjera (AUDIT) plana; kanonska struktura; EED kontrolna lista |
| `hc-scenario-analysis` | scenariji A/B/C, tehnički potencijal, LCOH, optimizacija najmanjeg troška, KPI i status učinkovitog CTS-a; Python model `lcoh_model.py` |
| `pgh-protokol` | zajednička pravila lanca agenata: radni direktorij, shema artefakta, oznake [M]/[P]/[O], kapije, pravila pisanja u Master |
| `revizija-dokumenata` | forenzička provjera brojki, izračuna, pretpostavki i izvora |
| `formatiranje-studije` | REGEA Word predložak (Calibri, numerirani naslovi, natpisi) i skripta za provjeru formatiranja |

Opcionalno (`skills-opcionalno/`): `project-graph` i `graphify` — graf znanja nad mapom projekta
(*iz kojeg dokumenta je ovaj broj?*).

**Agenti** (mapa `.claude/agents/`):

| Agent | Područje | Poglavlja kanona |
|---|---|---|
| `pgh-podaci` | ulazi, rupe u podacima, snapshot i **jedini upis u Master tablicu** | podloga za sve |
| `pgh-tehnicki` | potražnja, potencijali OIE i otpadne topline, kartice mjera, scenariji, bilanca CTS-a, el. mreža | 3, 4, 5 |
| `pgh-financijski` | CAPEX/OPEX, sistemski LCOH, tarifa, potpore, modeli financiranja, CBA | 6 |
| `pgh-pravnik` | EU i nacionalna legislativa, status učinkovitog CTS-a, pravna izvedivost | 1.3, 1.4, 2 |
| `pgh-prostorni` | GIS: slojevi, zone, trase i optimizacija mreže, ograničenja, karte | 3.2, 4.4 |
| `pgh-pisac` | sastavljanje `.docx` plana, sažeta verzija, primjerak za isporuku | cijeli plan |
| `pgh-kontrolor` | kapija K3: neovisna provjera svake brojke, presuda | cijeli plan |

**Ostalo:** `CLAUDE.md` (upute glavnoj sesiji), `reference/sharepoint-lokacije.md` (gdje su
kanonske podloge), `reference/lekcije-karlovac.md` (pravila nastala iz grešaka na Karlovcu),
`predlosci/gradovi/_PREDLOZAK/` (radni direktorij novog grada), `skripte/` (instalacija i pakiranje).

# Tri nužne podloge na SharePointu

Svi radimo na istom SharePointu (site **EUProjekti**, mapa
`LIFE 2021-2027/LIFE 2023-CET-LOCAL-ESCALATE/2_Planovi/`). Prije rada na bilo kojem planu
Claude mora imati pristup ovim trima podlogama:

1. **Plan G&H Karlovac — proširena verzija**
   `1_Karlovac/5_Plan_G&H/Plan_G&H_Karlovac_finalno_v3.0.docx`
   Ključna za razumijevanje *logike* izrade plana i kanonske strukture poglavlja.
2. **Plan G&H Karlovac — sažeta verzija**
   `1_Karlovac/6_Plan_G&H_komprimirano/Plan_G&H_Karlovac_sazeto.docx`
   Podloga za dokument koji ide gradu.
3. **Master tablica**
   `1_Karlovac/5_Plan_G&H/MasterSheet_Karlovac.xlsx`
   Podloga za svu analitiku. **Svaki plan mora imati vlastitu Master tablicu** — za novi grad ona
   nastaje po strukturi Karlovčeve, ali s podacima tog grada.

> Ako Claude ne može pronaći neku od ovih podloga, mora to reći i stati. Ako umjesto toga
> „pretpostavi” sadržaj, prekinite rad i ispravite pristup.

# Preduvjeti

| Što | Zašto | Napomena |
|---|---|---|
| Claude licenca (Team/Enterprise ili Pro/Max) | Claude Code i skillovi | provjerite s AI ambasadorom koja vam je licenca dodijeljena |
| **Claude Code** (preporučeno) ili Claude Desktop | puni lanac agenata radi u Claude Codeu | upute za instalaciju: službena dokumentacija Anthropica (code.claude.com) |
| Pristup SharePointu EUProjekti | kanonske podloge | isti pristup kao za ručni rad |
| Microsoft 365 konektor u Claudeu | da Claude čita SharePoint | uključuje se u postavkama konektora |
| Python 3.11+ s bibliotekama | izračuni, čitanje .xlsx/.docx | vidi niže |
| Windows + Microsoft Excel | **upis** u Master tablicu (Excel COM) | samo za onoga tko upisuje u Master |

Python biblioteke (jednom, u naredbenom retku):

```bash
pip install openpyxl python-docx pandas numpy scipy pywin32
```

Za GIS (samo ako radite prostornu analizu):

```bash
pip install geopandas shapely networkx pyogrio
```

> Nazive instalacijskih koraka i izbornika u Claude aplikacijama Anthropic povremeno mijenja.
> Ako se nešto iz ovih uputa ne podudara s onim što vidite, ravnajte se po aktualnoj službenoj
> dokumentaciji i javite to da se upute ažuriraju.

# Preuzimanje paketa

**Varijanta A — Git (preporučeno, lako ažuriranje):**

```bash
git clone https://github.com/ivanprzulj-max/Planovi-claude-toolkit.git
```

Ažuriranje kasnije: u mapi repozitorija `git pull`.

**Varijanta B — bez Gita:** na GitHub stranici repozitorija *Code → Download ZIP*, raspakirati
u npr. `C:\Users\<ime>\Planovi-claude-toolkit`.

# Kako učitati skillove i agente

Postoje tri načina. Odaberite jedan.

## Način 1 — Claude Code, rad iz mape repozitorija (preporučeno)

Najjednostavnije i najpouzdanije: ništa se ne instalira, sve se učitava iz mape.

1. Otvorite naredbeni redak (PowerShell) u mapi repozitorija.
2. Pokrenite `claude`.
3. Claude Code automatski učitava `CLAUDE.md`, skillove iz `.claude/skills/` i agente iz
   `.claude/agents/`.
4. Provjera: upišite `/agents` — morate vidjeti sedam `pgh-*` agenata. Upišite
   *Koje skillove imaš za planove grijanja i hlađenja?* — Claude mora navesti pet skillova.

## Način 2 — Claude Code, instalacija na korisničku razinu

Ako želite da skillovi i agenti budu dostupni u **svakoj** mapi u kojoj radite:

```bash
powershell -ExecutionPolicy Bypass -File skripte\instaliraj.ps1
```

(macOS/Linux: `bash skripte/instaliraj.sh`; dodajte `-Opcionalno` / `--opcionalno` za
project-graph i graphify.) Skripta kopira datoteke u `%USERPROFILE%\.claude\agents` i
`%USERPROFILE%\.claude\skills`. Nakon svakog `git pull` pokrenite je ponovno.

## Način 3 — Claude Desktop / claude.ai (samo skillovi)

Ako ne koristite Claude Code:

1. Zapakirajte skillove: `python skripte/zapakiraj_skillove.py` — u mapi `dist/` nastaje po
   jedna `.zip` datoteka za svaki skill.
2. U Claude aplikaciji otvorite postavke skillova (*Settings → Capabilities → Skills* ili
   ekvivalent u vašoj verziji) i učitajte svaku `.zip` datoteku.
3. Napravite **Projekt** po gradu i u njegovo znanje (Project knowledge) stavite: sažetu i
   proširenu verziju Plana Karlovac (ili poveznicu preko SharePoint konektora), Master tablicu grada
   te sadržaj `CLAUDE.md` i `reference/lekcije-karlovac.md` kao upute projekta.

> **Ograničenje načina 3:** definicije agenata (`.claude/agents/`) namijenjene su Claude Codeu.
> U Claude Desktopu / claude.ai lanac agenata ne radi automatski; korake K1→K3 vodite ručno, po
> jedan razgovor po koraku, a artefakte spremate kao datoteke. Je li u vašoj verziji Claude
> Desktopa (Cowork) moguće učitati i agente, provjerite u aktualnoj dokumentaciji.

# Povezivanje sa SharePointom

1. U Claudeu uključite **Microsoft 365** konektor i prijavite se svojim REGEA računom.
2. Provjera — upišite: *Pronađi na SharePointu MasterSheet_Karlovac.xlsx i reci mi broj listova.*
3. Ako koristite OneDrive sinkronizaciju mape `2_Planovi`, Claude Code može raditi i nad lokalnom
   sinkroniziranom kopijom — ali pazite: sinkronizacija mijenja datoteke i bez vaše izmjene, a
   **pisanje na SharePoint bez odobrenja nije dopušteno** ni Claudeu ni agentima.

# Rad na novom planu — korak po korak

## Korak 0 — priprema

1. Na SharePointu napravite mapu grada po uzoru na Karlovac (`1_Ulazni_podaci`, …, `8_Radno`;
   vidi `reference/sharepoint-lokacije.md`).
2. Lokalno: kopirajte `predlosci/gradovi/_PREDLOZAK` u `gradovi/<grad>` (npr. `gradovi/rijeka`).
   Mapa `gradovi/` se ne šalje na GitHub — kanon ostaje na SharePointu.
3. Pokrenite `claude` u mapi repozitorija.

Primjer prve poruke:

> Radimo Plan grijanja i hlađenja za Grad Rijeku. Radni direktorij je `gradovi/rijeka`.
> SharePoint mapa grada je `2_Planovi/3_Rijeka`. Učitaj pgh-protokol i hc-plan-creator, provjeri
> dostupnost triju kanonskih podloga i reci mi što nedostaje.

## Korak 1 — ulazi (kapija K1)

> Pokreni agenta pgh-podaci: inventar svih ulaza za Rijeku, popis rupa s predloženim metodama
> kompenzacije i nacrt zahtjeva prema gradu. Stani na K1.

Pregledajte inventar. Odlučite koje se metode kompenzacije prihvaćaju i što se traži od grada.
Odluku izgovorite izričito — glavna sesija je upisuje u `ODLUKE.md`.

## Korak 2 — analitika (kapija K2)

> Prema odluci K1, pokreni paralelno pgh-tehnicki, pgh-financijski, pgh-pravnik i pgh-prostorni
> za poglavlja 1–6. Na kraju mi daj sažetak za K2: scenarije, kombinaciju izvora po kontrolnim
> godinama, matricu usklađenosti s kriterijima učinkovitog CTS-a, prag potpore i pravnu izvedivost.

Na K2 birate ciljni scenarij i kombinaciju mjera. Ništa se ne piše u plan prije ove odluke.

## Korak 3 — pisanje

> Pokreni pgh-pisac: sastavi radni Plan prema strukturi proširenog Plana Karlovac, iz odobrenih
> artefakata. Zatim izradi sažetu verziju prema uzoru na Plan_G&H_Karlovac_sazeto.

## Korak 4 — kontrola (kapija K3)

> Pokreni pgh-kontrolor nad radnim Planom i Master tablicom — puni prolaz K3.

Plan smije gradu tek kad nalaz kontrole ima **0 blokirajućih stavki** i kad je izrađen čisti
primjerak za isporuku (bez komentara i praćenih izmjena — provjereno brojanjem).

## Korak 5 — ispravci u Master tablici

Kad agent uoči grešku u Masteru, on je **predlaže** (`radni/podaci/master-sheet-prijedlozi.md`).
Glavna sesija vam sažme: što se mijenja, zašto i što se u planu pomiče. Tek nakon vašeg izričitog
*Da, upiši* `pgh-podaci` izvodi upis (Excel COM, s zapisom u list `LOG_IZMJENA`). Redoslijed je
uvijek: **Master → radni plan → primjerak za isporuku**.

# Ostali tipični zadaci

**Revizija plana nakon komentara grada:**

> Grad je poslao komentare (datoteka …). Primijeni hc-plan-creator, workflow REVISE: najprije
> utvrdi koje komentare treba provesti u Master tablici, predloži mi izmjene, pa nakon odobrenja
> ažuriraj radni plan, sažetu verziju i prezentaciju. Svaku izmjenu zapiši u Evidenciju izmjena.

**Samo provjera (audit):**

> Primijeni hc-plan-creator, workflow AUDIT, nad Planom … i Master tablicom … Daj mi strukturirani
> nalaz: neslaganja plan↔Master, interne nekonzistentnosti, EED praznine, odstupanja od predloška.

**Samo analitika:**

> Primijeni hc-scenario-analysis: za CTS grada … izračunaj LCOH opcija (biomasa, dizalica topline
> na otpadnim vodama, geotermija) s i bez potpora i provjeri status učinkovitog CTS-a 2028.–2050.

**Formatiranje:**

> Primijeni formatiranje-studije na `plan/Plan_G&H_<grad>.docx` i pokreni provjeru.

# Zlatna pravila

1. **Master tablica je jedini izvor brojčane istine.** Svaka brojka u planu mora se dati pratiti
   do ćelije Mastera, ID-a pretpostavke ili citiranog izvora s godinom.
2. **Prvo Master, pa plan.** Nikad obrnuto, nikad samo jedno.
3. **Master mijenja samo `pgh-podaci`, samo uz vaše izričito odobrenje** — i nikad spremanjem kroz
   `openpyxl` (briše grafikone).
4. **Gradovi su strogo odvojeni.** Karlovac je predložak logike i strukture, ne izvor brojki.
5. **Oznake kvalitete:** [M] mjereno · [P] modelirano (s metodom) · [O] otvorena stavka.
   Otvorena stavka se nikad ne popunjava „uvjerljivom” vrijednošću.
6. **Kapije su obvezne.** Agent koji dođe do kapije staje i čeka vašu odluku.
7. **Bez odobrenja ništa se ne piše na SharePoint.**
8. **Radni dokument ≠ primjerak za isporuku.** Gradu ide samo čisti izvod.
9. Pravne navode, pragove i cijene uvijek provjeriti u **primarnom izvoru s datumom** —
   propisi se mijenjaju.

# Česti problemi

| Problem | Uzrok / rješenje |
|---|---|
| `/agents` ne prikazuje pgh agente | Claude Code nije pokrenut iz mape repozitorija, ili niste pokrenuli instalacijsku skriptu (način 2). Ponovno pokrenite Claude Code. |
| Claude ne nalazi datoteke na SharePointu | Microsoft 365 konektor nije uključen ili nemate pristup mapi. |
| Nakon upisa u Master nestali grafikoni | Datoteka je spremljena kroz openpyxl. Vratite sigurnosnu kopiju; upis ponoviti Excel COM-om. |
| Agent „izmišlja” brojku | Prekinite. Brojka bez podrijetla je greška; tražite oznaku `[O]` i upit gradu. |
| Plan i Master se ne slažu | Utvrdite koji je ispravan; ispravak ide **najprije u Master**, pa u plan. |
| `pywin32` / Excel COM ne radi | Radi samo na Windowsu s instaliranim Excelom; upis u Master prepustite kolegi koji to ima. |
| Natpisi slika *Slika 44.6* | Dvostruko polje STYLEREF — ukloniti drugo polje (F9 ne pomaže). |

# Održavanje paketa

- Paket se održava na GitHubu. Prijedlog izmjene skilla ili agenta: nova grana i *pull request*,
  uz kratak opis *što i zašto* (npr. nova lekcija iz kontrole nekog plana).
- Nove lekcije upisujte u `reference/lekcije-karlovac.md` (ili novu datoteku po gradu).
- Ne stavljajte u repozitorij podatke gradova, Master tablice ni planove — oni žive na SharePointu.
- Svaku promjenu zapišite u `CHANGELOG.md`.

# Prilog — kratki podsjetnik

```
claude            pokretanje u mapi repozitorija
/agents           popis agenata

K1  pgh-podaci    inventar ulaza, rupe
    -> VAŠA ODLUKA
K2  tehnicki / financijski / pravnik / prostorni
    -> scenariji, mjere -> VAŠA ODLUKA
    pgh-pisac     radni plan + sažeta verzija
K3  pgh-kontrolor presuda (0 blokirajućih)
    -> VAŠA ODLUKA
    pgh-podaci    upis u Master + LOG_IZMJENA
                  (samo uz odobrenje)

Ispravak: Master -> radni plan -> primjerak za isporuku
```
