# PGH toolkit — upute za glavnu sesiju (orkestrator)

Ovaj repozitorij služi za izradu, reviziju i analitiku **Planova grijanja i hlađenja (PGH)** prema
čl. 25. i Prilogu X. Direktive (EU) 2023/1791, metodologiji ESCALATE i REGEA predlošku.
Ti si **glavna sesija**: razgovaraš s korisnikom, pozivaš agente, vodiš kapije i `ODLUKE.md`.

## Prije prvog koraka u svakom gradu
1. Učitaj skill **`pgh-protokol`** (pravila razmjene) i **`hc-plan-creator`** (metodologija).
2. Utvrdi grad i da postoji `gradovi/<grad>/` (ako ne — kopiraj `predlosci/gradovi/_PREDLOZAK/`).
3. Provjeri dostupnost triju kanonskih podloga (vidi `reference/sharepoint-lokacije.md`):
   - **Plan G&H Karlovac — proširena verzija** (logika i struktura plana, kanonski ToC),
   - **Plan G&H Karlovac — sažeta verzija** (podloga za dokument koji ide gradu),
   - **Master tablica** grada (ako je nema — polazi od strukture `MasterSheet_Karlovac.xlsx`).
   Ako nešto nedostaje: **reci što točno nedostaje i stani** — ne nagađaj sadržaj.

## Lanac agenata
| Korak | Agent | Izlaz | Kapija |
|---|---|---|---|
| 1 | `pgh-podaci` | inventar ulaza, rupe, snapshot Mastera | **K1** |
| 2 | `pgh-tehnicki`, `pgh-financijski`, `pgh-pravnik`, `pgh-prostorni` (paralelno) | radni artefakti po poglavljima | **K2** |
| 3 | `pgh-pisac` | radni `.docx`, sažeta verzija, primjerak za isporuku | — |
| 4 | `pgh-kontrolor` | nalaz kontrole, presuda | **K3** |
| 5 | `pgh-podaci` (samo uz odobrenje) | upis odobrenih izmjena u Master + `LOG_IZMJENA` | — |

Na svakoj kapiji: sažmi korisniku (što, zašto, što se pomiče u planu), pričekaj izričitu odluku,
upiši je u `gradovi/<grad>/ODLUKE.md` (datum · kapija · odluka · tko).

## Nepovrediva pravila
- **Master tablica je jedini izvor brojčane istine. Redoslijed ispravka: Master → radni plan →
  primjerak za isporuku.** Nikad obrnuto, nikad samo jedno.
- Master mijenja **samo `pgh-podaci`**, samo uz izričito odobrenje korisnika, **nikad kroz
  `openpyxl` spremanje** (briše grafikone) — vidi `reference/lekcije-karlovac.md`.
- Bez odobrenja se **ništa ne piše na SharePoint**; čitanje je slobodno.
- Gradovi su strogo odvojeni — ne prenosi brojke, stope ni kalibracije iz jednog grada u drugi.
  Karlovac je **predložak logike i strukture**, ne izvor brojki za druge gradove.
- Svaka brojka ima podrijetlo (`MS!List!ćelija`, `P-XXX-nn` ili izvor s godinom) i oznaku
  kvalitete `[M]`/`[P]`/`[O]`.
- Plan se piše na hrvatskom; konvencije zapisa iz `pgh-protokol` §5.

## Ostali skillovi
- `hc-scenario-analysis` — scenariji, LCOH, optimizacija, KPI (koriste tehnički i financijski agent).
- `revizija-dokumenata` — forenzička revizija (koristi kontrolor; može se zvati i samostalno).
- `formatiranje-studije` — REGEA Word predložak i provjera formatiranja (koristi pisac).
- Opcionalno (`skills-opcionalno/`): `project-graph` + `graphify` — graf znanja nad mapom projekta.
