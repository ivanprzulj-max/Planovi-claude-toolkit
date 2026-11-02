# SharePoint lokacije — kanonske podloge

Site: **EUProjekti** (`https://regeadoo.sharepoint.com/sites/EUProjekti`)
Biblioteka: *Shared Documents* → `LIFE 2021-2027/LIFE 2023-CET-LOCAL-ESCALATE/2_Planovi/`

> Stanje utvrđeno 2. 11. 2026. Ako se datoteke premjeste ili preimenuju, ažurirajte ovu datoteku
> (i zapišite to u `CHANGELOG.md`).

## Karlovac — referentni (pilot) plan

| Što | Putanja (unutar `2_Planovi/`) | Namjena |
|---|---|---|
| **Plan — proširena verzija** | `1_Karlovac/5_Plan_G&H/Plan_G&H_Karlovac_finalno_v3.0.docx` (+ `.pdf`, `_EN.docx`) | ključna za razumijevanje **logike izrade** plana; kanonski ToC i struktura poglavlja |
| **Plan — sažeta verzija** | `1_Karlovac/6_Plan_G&H_komprimirano/Plan_G&H_Karlovac_sazeto.docx` (+ `.pdf`) | **podloga za dokument koji ide gradu** (≤ ~50 str., bez priloga) |
| **Master tablica** | `1_Karlovac/5_Plan_G&H/MasterSheet_Karlovac.xlsx` | brojčani kanon; **svaki plan mora imati svoju Master tablicu** |
| Dnevnik verzija | `1_Karlovac/5_Plan_G&H/Radno/VERZIJA.md` | povijest kanona, dvojnike koje se ne smije otvarati, osobitosti Mastera |
| Komentari radne skupine | `1_Karlovac/5_Plan_G&H/Komentari_radne_skupine/` | primjer obrasca za komentare grada |
| Prostorna analiza | `1_Karlovac/7_Prostorna_analiza/` i `1_Karlovac/3_GIS&PP/` | primjer rada `pgh-prostorni` |
| Radni artefakti agenata | `1_Karlovac/8_Radno/` | primjeri artefakata po shemi protokola (nalazi kontrole, upisi, blokovi) |
| Prezentacija | `1_Karlovac/6_Plan_G&H_komprimirano/Prezentacija_Plan_GH_Karlovac.pptx` | primjer prezentacije za grad |

## Preporučena struktura mape novog grada (prema Karlovcu)

```
2_Planovi/<n>_<Grad>/
├── 1_Ulazni_podaci/
├── 2_Excelice_za_Master/
├── 3_GIS&PP/
├── 4_Power_BI/
├── 5_Plan_G&H/                 ← kanon: Plan_G&H_<Grad>.docx + MasterSheet_<Grad>.xlsx
│   ├── Komentari_radne_skupine/
│   └── Radno/                  ← VERZIJA.md
├── 6_Plan_G&H_komprimirano/    ← sažeta verzija + prezentacija
├── 7_Prostorna_analiza/
└── 8_Radno/                    ← radni artefakti agenata
```

## Ostale korisne lokacije
- `2_Planovi/RADNO/Guidelines_template/` — ESCALATE smjernice (Guidelines V4).
- `2_Planovi/HEP_ODS_Plan_ulaganja_Prijedlog_2026-09-30.pdf` — podloga za poglavlje o el. mreži.
- Ostali gradovi u izradi: `2_Slavonski_Brod/`, `3_Rijeka/`, `4_Velika_Gorica/`.
