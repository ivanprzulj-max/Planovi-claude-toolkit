# KPI Definitions and Regulatory Compliance Framework

## 1. EED (EU) 2023/1791, Article 26 — "efficient district heating and cooling" trajectory

This is usually the binding KPI ladder for CTS scenarios. Shares are measured **at the handover point into the network** (per Commission Recommendation (EU) 2024/2395, the official interpretation guidance — consult it for edge cases). Two compliance paths exist:

**Path 1 — source-mix criteria, Art. 26(1), tightening by period:**

| Period | Minimum requirement (any one option) |
|---|---|
| until 31 Dec 2027 | ≥50% RES; or ≥50% waste heat; or ≥75% cogenerated heat; or ≥50% combination |
| from 1 Jan 2028 | ≥50% RES; or ≥50% waste heat; or ≥50% RES+waste heat; or ≥80% high-efficiency CHP heat; or a combination where RES ≥ 5% and RES+WH+HECHP ≥ 50% |
| from 1 Jan 2035 | ≥50% RES; or ≥50% waste heat; or ≥50% RES+waste heat; or a combination where RES+WH+HECHP ≥ 80% with RES+WH ≥ 35% |
| from 1 Jan 2040 | ≥75% RES; or ≥75% waste heat; or ≥75% RES+waste heat; or a combination where RES+WH+HECHP ≥ 95% with RES+WH ≥ 35% |
| from 1 Jan 2045 | ≥75% RES + waste heat (HECHP no longer qualifies a system) |
| from 1 Jan 2050 | only RES and waste heat (100%) |

**Path 2 — GHG-intensity alternative, Art. 26(2):** a system also qualifies if emissions per unit of delivered heat/cold stay under a declining cap (approx.: 200 g CO₂/kWh from 2026 → 150 from 2035 → 100 from 2045 → 50 from 2050).

⚠️ Before publishing a deliverable, verify exact threshold wording against the consolidated EED text and Recommendation (EU) 2024/2395 (a Commission review of thresholds was due by Oct 2027 — check for amendments). Also apply: **no new fossil-fuel heat generation capacity** in efficient DH systems (gas HECHP support only until 2030); DH systems > 5 MW output that are not efficient need a transformation plan (Art. 26(5)).

## 2. RES share — accounting rules (RED, Directive (EU) 2018/2001 as amended by 2023/2413)

- **Heat pumps:** renewable (ambient/geothermal) energy captured = E_RES = Q_usable × (1 − 1/SPF) per RED Annex VII. Only HPs with SPF above the eligibility threshold count (threshold derived from 1.15 × 1/η; in practice SPF ≳ 2.5 for electric HPs — verify the current Commission decision value). The electricity input is NOT renewable heat (its renewable character sits in the electricity statistics — do not double-count).
- **Biomass:** counts as RES subject to RED III sustainability & GHG-saving criteria (thresholds by plant size); flag if a proposed plant exceeds the size where criteria/documentation apply.
- **Waste heat** is NOT RES — it is a separate category in EED Art. 26 (definition per RED Art. 2(9): unavoidable heat as by-product, would be dissipated unused). Heat from an industrial process burning fossil fuel can be "waste heat"; heat produced deliberately for the network cannot. Booster-HP-upgraded waste heat: the HP ambient-equivalent share follows Annex VII logic; keep waste heat vs. RES bookkeeping separate.
- **RED Art. 23/24 targets:** indicative +1.1 pp/yr average annual RES-H&C increase (with top-ups), and indicative +2.2 pp/yr for DH systems' RES+WH share (Art. 24(4)) — use as reasonableness cross-checks for the scenario trajectory.

## 3. Savings KPIs

- Define the baseline explicitly (base year, climate-normalized) and the metric: final energy savings % vs. baseline, or cumulative savings (EED Art. 8 style). Plan-level default: delivered heat demand reduction vs. frozen-efficiency baseline.
- Distinguish demand-side savings (renovation) from supply-side efficiency gains (loss reduction, higher plant efficiency) — report both, never sum silently.

## 4. Croatian national framework (verify current status — moves frequently)

- Transposition of EED 2023/1791 into HR law (ZTEE amendments / novi Zakon) — verify the current transposition state and whether Art. 26 criteria are transposed verbatim or stricter.
- Zakon o tržištu toplinske energije (ZTTE) — network development obligations, supplier/distributor roles; HERA tariff methodology for translating costs to tariffs.
- Integrirani NECP RH: national RES-H&C trajectories to cross-check municipal ambition.
- Local heating & cooling plans obligation: municipalities > 45,000 inhabitants (EED Art. 25(6)).
- Prostorni planovi (županijski/gradski/UPU): every supply-site and pipeline-corridor claim must state planning conformity or the amendment need.

## 5. Compliance matrix — required output format

One table per scenario:

| KPI | 2030 | 2035 | 2040 | 2045 | 2050 |
|---|---|---|---|---|---|
| Energy adequacy (production ≥ requirement) | ✔/✘ + margin % | … | | | |
| Capacity adequacy incl. reserve | ✔/✘ | | | | |
| RES share [%] (min. required) | value (min) | | | | |
| Waste-heat share [%] | | | | | |
| Efficient-DH status (Art. 26 option used) | option (b)… | option (c)… | | | |
| GHG intensity [g/kWh] (if Path 2 relevant) | | | | | |
| Savings vs. baseline [%] | | | | | |

Mark the **binding constraint** per milestone (the KPI that forced the last, most expensive addition) — this is the analytical headline.
