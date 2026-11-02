# PGH toolkit — Planovi grijanja i hlađenja (Claude skillovi i agenti)

Skillovi i agenti za **izradu, reviziju i analitiku Planova grijanja i hlađenja (PGH)** prema čl. 25. i
Prilogu X. Direktive (EU) 2023/1791, metodologiji projekta ESCALATE i REGEA predlošku.
Nastalo na Planu G&H Grada Karlovca.

📘 **Upute za korištenje (samostalan dokument):** [`docs/UPUTE_ZA_KORISTENJE.docx`](docs/UPUTE_ZA_KORISTENJE.docx)
· [Markdown verzija](docs/UPUTE_ZA_KORISTENJE.md)

## Brzi početak (Claude Code)
```bash
git clone <URL ovog repozitorija>
cd pgh-claude-toolkit
claude
```
U Claude Codeu: `/agents` → mora prikazati sedam `pgh-*` agenata. Detalji i alternative (Claude Desktop,
claude.ai) su u uputama.

## Sadržaj
| Mapa | Što |
|---|---|
| `CLAUDE.md` | upute glavnoj sesiji: lanac agenata, kapije K1–K3, nepovrediva pravila |
| `.claude/skills/` | `hc-plan-creator`, `hc-scenario-analysis`, `pgh-protokol`, `revizija-dokumenata`, `formatiranje-studije` |
| `.claude/agents/` | `pgh-podaci`, `pgh-tehnicki`, `pgh-financijski`, `pgh-pravnik`, `pgh-prostorni` (GIS), `pgh-pisac`, `pgh-kontrolor` |
| `skills-opcionalno/` | `project-graph`, `graphify` (graf znanja nad mapom projekta) |
| `reference/` | SharePoint lokacije kanonskih podloga; lekcije iz izrade Plana Karlovac |
| `predlosci/gradovi/_PREDLOZAK/` | radni direktorij novog grada |
| `skripte/` | instalacija (Windows/macOS/Linux), pakiranje skillova u .zip, izrada uputa u .docx |
| `docs/` | upute za korištenje |

## Kanonske podloge (SharePoint, site EUProjekti)
`LIFE 2021-2027/LIFE 2023-CET-LOCAL-ESCALATE/2_Planovi/1_Karlovac/`
- `5_Plan_G&H/Plan_G&H_Karlovac_finalno_v3.0.docx` — proširena verzija (logika i struktura plana)
- `6_Plan_G&H_komprimirano/Plan_G&H_Karlovac_sazeto.docx` — sažeta verzija (podloga za grad)
- `5_Plan_G&H/MasterSheet_Karlovac.xlsx` — Master tablica (svaki plan mora imati svoju)

Podaci gradova, planovi i Master tablice **ne idu u ovaj repozitorij** — kanon je na SharePointu.

## Tri pravila koja se ne krše
1. Master tablica je jedini izvor brojčane istine — ispravak ide **prvo u Master, pa u plan**.
2. Master mijenja samo `pgh-podaci`, samo uz izričito odobrenje, nikad spremanjem kroz `openpyxl`.
3. Gradovi su strogo odvojeni; Karlovac je predložak logike, ne izvor brojki.
