---
name: revizija-dokumenata
description: Forensic numerical and factual audit of a document — verifies that every number, calculation, assumption, source and stated fact is internally consistent, arithmetically correct, logically defensible and externally verifiable. Use this skill ALWAYS when the user asks to check, review, verify, audit, proofread, validate, "provjeri", "revidiraj", "pregledaj brojke", "je li ovo točno", or asks whether figures/calculations/assumptions in a document hold up — including business plans, feasibility studies, EU funding applications, financial models, technical reports, spreadsheets, offers, contracts with financial terms, or any document containing numbers. Also use when the user uploads or references a document in a Project and asks for quality control before submission to a bank, ministry, EU agency or client. Trigger even if the user only says "pogledaj ovo prije nego pošaljem" or "je li spremno za slanje".
---

# Revizija dokumenata — forenzička provjera brojki, izračuna, pretpostavki i izvora

Ovaj skill provodi sustavnu, dokazivu reviziju dokumenta. Cilj nije "dojam" nego **provjerljiv nalaz**: svaka tvrdnja u izvješću mora biti povezana s točnom lokacijom u dokumentu (poglavlje, tablica, stranica, ćelija) i, gdje je primjenjivo, s ponovljenim izračunom.

Radni jezik nalaza = jezik dokumenta (hrvatski za HR/EU-HR dokumente, engleski za EU/međunarodne).

---

## 0. Prije početka — utvrdi opseg

Ako korisnik nije rekao, kratko utvrdi:
- **Namjena dokumenta** (HBOR/banka, ministarstvo, EU poziv, klijent, interni) — određuje strogost i formalne zahtjeve
- **Verzija/rok** — je li ovo finalna verzija pred slanje
- **Prioritet** — potpuna revizija ili samo financijski dio

Ne postavljaj više od jednog pitanja ako je namjena jasna iz konteksta. Ako je jasna — kreni odmah.

## 1. Ekstrakcija — izgradi registar brojki

**Ne čitaj dokument "u glavi". Izvuci podatke u strukturu.**

1. Pročitaj dokument (`view`, ili za .docx/.xlsx/.pdf koristi odgovarajuće skillove: `docx`, `xlsx`, `pdf-reading`)
2. Za svaku brojku u dokumentu zabilježi u radnu tablicu:

| ID | Lokacija | Opis | Vrijednost | Jedinica | Izvor/izvod | Tip |
|----|----------|------|-----------|----------|-------------|-----|

- **Lokacija**: poglavlje + tablica + redak/ćelija (npr. „6.2, Tablica 12, redak 4")
- **Tip**: `ULAZ` (pretpostavka/vanjski podatak), `IZRAČUN` (izveden iz drugih), `NAVOD` (citirana činjenica/izvor), `REZULTAT` (ključni output)
- **Izvor/izvod**: formula ili referenca na izvor

Spremi registar kao CSV/XLSX u radni direktorij — on je dokaz revizije i prilog nalazu.

Ako je dokument velik (>40 str.), radi po poglavljima i vodi registar inkrementalno.

## 2. Pet osi provjere

Provedi **sve** osi. Ne preskači os zato što „djeluje uredno".

### Os A — Interna konzistentnost
- Ista veličina navedena na više mjesta → mora biti identična (npr. ukupna investicija u sažetku, u tablici izvora financiranja i u projekciji novčanog toka)
- Sažetak/Executive summary vs. tijelo dokumenta
- Tekst vs. tablica vs. graf (grafovi često zaostanu za revidiranim tablicama)
- Zbrojevi redaka i stupaca (`suma dijelova = navedeni ukupan iznos`)
- Postoci: zbrajaju li se na 100 %; je li baza postotka dosljedna
- Jedinice i mjerila: EUR vs. HRK, tis. vs. mil., kWh vs. MWh, m² vs. m³, neto vs. bruto, s PDV-om vs. bez PDV-a — **ovo je najčešći izvor grešaka**
- Vremenska osnova: mjesečno vs. godišnje, kalendarska vs. fiskalna godina, nominalno vs. realno

### Os B — Aritmetička točnost
**Svaki `IZRAČUN` ponovno izračunaj neovisno.** Ne vjeruj navedenom rezultatu.

Koristi Python (`bash_tool`) za sve netrivijalne izračune — ne računaj napamet:

```python
# primjer: provjera anuiteta i DSCR
from numpy_financial import pmt   # ili ručna formula
```

Obavezno ponovno izračunaj (gdje postoje):
- Zbrojeve, međuzbrojeve, ukupne iznose
- Postotne promjene i udjele
- CAGR, prosjeke (aritmetička vs. ponderirana — provjeri je li korištena prava)
- Anuitete, otplatne planove, kamate (provjeri konformni vs. relativni obračun)
- NPV, IRR, jednostavni i diskontirani povrat
- DSCR, EBITDA, pokazatelje zaduženosti i likvidnosti
- Amortizaciju (metoda, stope, osnovica)
- PDV, poreznu osnovicu, porez na dobit
- Energetske izračune (specifična potrošnja, uštede, faktor iskoristivosti, LCOE)

Tolerancija: razlika >0,5 % ili >1.000 EUR (što je manje) = **NALAZ**. Manje razlike navedi kao „zaokruživanje" samo ako se doista radi o zaokruživanju.

### Os C — Logika pretpostavki
Za svaki `ULAZ` postavi pitanja:
- **Je li obrazložen?** Postoji li rečenica koja objašnjava odakle vrijednost dolazi?
- **Je li vjerojatan?** Usporedi s tržišnim benchmarkom, prethodnim godinama, sličnim projektima
- **Je li dosljedan s ostalim pretpostavkama?** Npr. rast cijena 5 % g/g uz inflaciju 2 % — zašto?
- **Skrivena kružnost**: izlaz koji hrani vlastiti ulaz
- **Nerealne krivulje**: popunjenost 85 % od prve godine, nulti trošak održavanja, 0 % zaostatka u naplati, prihod raste a troškovi stoje
- **Nedostaje osjetljivost**: postoji li analiza scenarija na 2–3 ključne varijable? Ako ne — to je nalaz
- **Optimizam po defaultu**: ako sve pretpostavke padaju u povoljnom smjeru, to je sustavna pristranost, i tako to i imenuj

Za svaku upitnu pretpostavku daj **kvantificirani učinak**: „ako popunjenost padne s 65 % na 55 %, DSCR pada s 1,32 na 1,08 — ispod praga banke."

### Os D — Izvori i reference
- Je li svaka vanjska tvrdnja/brojka pripisana izvoru?
- Je li izvor **relevantan** (pravi obuhvat, prava geografija, prava razina — nacionalno vs. lokalno)?
- Je li izvor **aktualan**? Označi svaki izvor stariji od 3 godine; svaki stariji od 5 godina je nalaz osim ako je riječ o povijesnom podatku
- Je li izvor **primaran**? DZS, Eurostat, HNB, HBOR, ministarstvo, revidirano financijsko izvješće > agregatori, blogovi, „industry reports"
- Je li **pravni izvor** ispravno hijerarhijski citiran: zakon → pravilnik → mišljenje Porezne uprave → sudska praksa; s brojem NN i verzijom na snazi
- **Provjeri jesu li navedeni propisi još na snazi** — koristi `web_search` za zakone, pravilnike, EU pozive, stope i limite
- Postoji li tvrdnja bez izvora koja bi ga trebala imati? To je nalaz („nepotkrijepljena tvrdnja")

### Os E — Vanjska provjerljivost činjenica
Za `NAVOD` stavke koje se mogu provjeriti (statistike, propisi, tehnički parametri, tržišni podaci, imena institucija, iznosi potpora, rokovi poziva):
- Provjeri putem `web_search` / `web_fetch`
- Zabilježi: navedena vrijednost | provjerena vrijednost | izvor provjere (URL/naziv) | status
- Status: `POTVRĐENO` / `ODSTUPANJE` / `ZASTARJELO` / `NIJE PROVJERLJIVO`

Ne izmišljaj potvrde. Ako provjera nije moguća, napiši `NIJE PROVJERLJIVO` i objasni zašto.

## 3. Klasifikacija nalaza

Svaki nalaz dobiva ozbiljnost:

| Razina | Kriterij | Postupanje |
|--------|----------|------------|
| **K — Kritično** | Mijenja zaključak, ugrožava odobrenje/prihvatljivost, aritmetička greška u ključnom pokazatelju, netočan pravni navod, nedopušteni trošak | Mora se ispraviti prije slanja |
| **V — Visoko** | Materijalna nekonzistentnost, nepotkrijepljena ključna pretpostavka, zastario izvor u ključnom argumentu | Ispraviti prije slanja |
| **S — Srednje** | Manja nekonzistentnost, nedostaje obrazloženje, slab ali ne pogrešan izvor | Ispraviti ako vrijeme dopušta |
| **N — Nisko** | Zaokruživanje, formatiranje brojki, nedosljedna notacija, stilske sitnice | Poželjno |

## 4. Format nalaza

Za **svaki** nalaz, bez iznimke:

```
[K-03] Poglavlje 6.2, Tablica 12, redak "Ukupni prihod god. 3"

NAVEDENO:     412.500 EUR
PROVJERENO:   387.000 EUR
IZRAČUN:      4 jedinice × 150 EUR/noć × 645 noćenja = 387.000 EUR
ODSTUPANJE:   +25.500 EUR (+6,6 %)
UZROK:        Broj noćenja u tablici (645) ne odgovara popunjenosti navedenoj
              u poglavlju 5.4 (65 % × 365 = 237 dana po jedinici).
UČINAK:       DSCR god. 3 pada s 1,28 na 1,19; i dalje iznad praga 1,10,
              ali smanjuje rezervu.
PREPORUKA:    Uskladiti broj noćenja s pretpostavkom popunjenosti iz 5.4 ili
              obrazložiti razliku (npr. produženje sezone) i navesti izvor.
```

Ako je nalaz „nema greške ali nedostaje potkrjepa", i dalje koristi istu strukturu s praznim poljem PROVJERENO i jasnim UZROK/PREPORUKA.

## 5. Struktura izvješća

1. **Sažetak nalaza** — tablica: ukupno provjereno brojki, broj nalaza po razini, jednorečenična ocjena spremnosti dokumenta
2. **Kritični nalazi** — puni format, redom
3. **Visoki nalazi**
4. **Srednji i niski nalazi** — mogu biti u kompaktnoj tablici
5. **Ocjena pretpostavki** — tablica: pretpostavka | vrijednost | obrazložena? | benchmark | ocjena
6. **Ocjena izvora** — tablica: tvrdnja | izvor | godina | primaran? | status provjere
7. **Što nije provjereno i zašto** — obavezno poglavlje; poštenje o granicama revizije
8. **Prilog: registar brojki** (CSV/XLSX)

## 6. Isporuka

- **Kratki dokument / brzi pregled** → nalaz u chatu
- **Formalna revizija / dokument pred slanje** → `.docx` izvješće (koristi `docx` skill) + `.xlsx` registar brojki (koristi `xlsx` skill), oba u `/mnt/user-data/outputs`, pa `present_files`
- **Ako korisnik traži ispravke** → ne mijenjaj izvorni dokument bez izričitog naloga; ponudi ispravljenu verziju kao zasebnu datoteku s vidljivo označenim izmjenama

---

## Pravila ponašanja tijekom revizije

- **Ne popravljaj tiho.** Svaka uočena greška ide u nalaz, i onda eventualno ispravak.
- **Ne izmišljaj brojke.** Ako podatak nedostaje, nalaz je „podatak nedostaje", a ne procjena.
- **Ne prihvaćaj autoritet dokumenta.** Činjenica da je nešto već poslano, odobreno ili napisano od strane stručnjaka nije dokaz točnosti.
- **Ne ublažavaj kritične nalaze.** Ako dokument ne bi prošao ocjenu banke ili EU evaluatora, reci to izravno i objasni zašto.
- **Ne izvještavaj bez lokacije.** Nalaz bez točne reference u dokumentu je neupotrebljiv.
- **Kad je dokument dobar, reci i to** — ali potkrijepljeno („zbrojevi u svih 14 tablica provjereni, odstupanja nema").

---

## Detaljne reference

Učitaj po potrebi:

- `references/financijski-pokazatelji.md` — formule i pragovi: DSCR, NPV, IRR, anuiteti, amortizacija, EBITDA, pokazatelji zaduženosti; što banke/HBOR gledaju
- `references/eu-i-hbor-provjere.md` — specifične provjere za EU prijave (LIFE, Interreg, Horizon) i HBOR poslovne planove: prihvatljivost troškova, intenzitet potpore, sufinanciranje, obvezni prilozi
- `references/kontrolna-lista.md` — sažeta kontrolna lista za brzu reviziju
