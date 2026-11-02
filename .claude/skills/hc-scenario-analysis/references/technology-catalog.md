# Technology Catalog — Default Technoeconomic Parameters, Lead Times, Spatial Constraints

Use ONLY when the source document does not provide a parameter. Every value taken from here is an Assumption Register entry. Values are indicative EU/Croatia plan-level ranges (real EUR, ~2024–2026 vintage) consistent with Danish Energy Agency "Technology Data for Generation of Electricity and District Heating" and recent EU project experience. For bankable studies, replace with vendor quotes / FEED estimates and, where figures are decision-critical, verify current values via web search.

## 1. Heat generation

| Technology | Specific CAPEX | Fixed O&M | Variable O&M | Efficiency / SPF | Lifetime | Typical role |
|---|---|---|---|---|---|---|
| Large heat pump — ambient/river/sea water | 0.7–1.3 M€/MW_th (excl. grid conn.) | 2–3 €/MWh + 1.5%/yr CAPEX | 1–2 €/MWh | SPF 2.8–3.6 (70/40°C sink) | 25 yr | Base/mid load |
| Large heat pump — sewage/WWTP effluent | 0.8–1.4 M€/MW_th | as above | as above | SPF 3.0–4.0 | 25 yr | Base load |
| Deep geothermal doublet (HR Pannonian basin) | 1.8–4.5 M€/MW_th incl. wells; well risk material | 2–4%/yr CAPEX | low | thermal output = f(flow l/s, ΔT); parasitic el. 5–10% | 30 yr (wells 25–50) | Base load |
| Solar thermal field (large flat-plate) | 250–450 €/m² installed (field+piping) | ~0.5%/yr | ~0 | Yield 400–550 kWh/m²/yr (HR continental) | 25–30 yr | Summer/DHW; seasonal w/ pit TES |
| Biomass hot-water boiler (5–20 MW) | 0.5–0.9 M€/MW | 2–3%/yr | 3–5 €/MWh | 85–92% (108%+ w/ flue-gas condensation) | 25 yr | Base/mid load |
| Biomass CHP (ORC/steam) | 3–6 M€/MW_e | 3–4%/yr | 4–8 €/MWh | η_th 60–70%, η_e 15–25% | 25 yr | Base load + el. revenue |
| Energy-from-waste heat offtake | highly site-specific; offtake pipeline dominates | — | — | — | 25–30 yr | Base load; contract-dependent |
| Industrial/data-center waste heat recovery | 0.3–1.0 M€/MW (HX, pumps, controls) + pipeline + often booster HP | 2%/yr | low | booster HP SPF 4–6 (small lift) | 20–25 yr | Base load; counterparty risk |
| Electric boiler | 0.10–0.25 M€/MW + grid connection | 1%/yr | ~1 €/MWh | 99% | 20 yr | Peak, flexibility, P2H |
| Gas boiler (existing/peak-reserve only) | 0.08–0.15 M€/MW | 2%/yr | 1–2 €/MWh | 92–104% | 25 yr | Peak/reserve ONLY — EED bans new fossil capacity in efficient DH; check status before proposing |

Fuel/energy price defaults (real, register + sensitivity-test): biomass chips 25–45 €/MWh_fuel; natural gas 30–50 €/MWh incl. network charges; electricity for large consumers 80–140 €/MWh incl. grid fees (HP economics are dominated by this — always test); ETS CO₂ central trajectory 80–100 €/t to 2030 rising toward 120–160 €/t by 2040 (verify current forward curve); ETS2 expected materially lower initially (soft cap 45 €/t mechanism) — verify current status.

## 2. Thermal storage

| Type | CAPEX | Round-trip | Role |
|---|---|---|---|
| Steel tank TES (daily) | 100–250 €/m³ (~1.5–4 €/kWh) | 90–98% | Peak shaving, HP/CHP optimization |
| Pit TES (seasonal, >50,000 m³) | 20–40 €/m³ | 60–80% seasonal | Solar thermal seasonality; large systems |

## 3. Network infrastructure

| Item | CAPEX | Notes |
|---|---|---|
| Distribution pipe pair, urban (DN80–DN200) | 0.6–1.5 M€/km | Surface, congestion-dependent |
| Transmission pipe pair (DN300–DN600) | 1.2–3.0 M€/km urban; 0.7–1.5 M€/km greenfield | Source-to-network connection lines |
| Customer substation | 15–60 k€ per connection (size-dep.) | |
| Network refurbishment / temp. reduction program | site-specific | Enables losses ↓ (target ≤10–12%) and low-T sources |
| Grid connection for large HP/e-boiler | HEP-ODS/OPS quote; can be limiting in timing and cost | ASK if >5 MW_e |

Network losses defaults: existing older HR systems 12–18%; refurbished 8–12%; new low-T 5–8%.

## 4. Demand-side (EE) measures

| Renovation depth | Specific heating savings | Indicative cost (full works) | Heating-attributable share |
|---|---|---|---|
| Shallow (single measures) | 10–25% | 50–150 €/m² | 60–80% |
| Medium (integral, standard) | 30–45% | 200–400 €/m² | 50–70% |
| Deep (nZEB-level) | 50–70% | 400–700 €/m² | 40–60% |

Realistic renovation rates: 1–1.5%/yr of stock BAU; 2–3%/yr with strong programs (aligned with Dugoročna strategija obnove); do not assume >3%/yr without explicit justification.

## 5. Lead times — the feasibility test (development + permitting + construction, from decision)

| Measure | Typical total lead time (HR/EU) | Notes |
|---|---|---|
| Electric boiler / tank TES | 1–2 yr | Grid connection can extend |
| Biomass boiler plant | 2–4 yr | Fuel supply contracting in parallel |
| Large ambient/sewage heat pump | 2–4 yr | Water rights (vodopravni uvjeti) for water sources |
| Solar thermal field | 2–3 yr | Land securing + prostorni plan is the driver |
| Waste heat offtake incl. pipeline | 3–5 yr | Contract negotiation often the critical path |
| Deep geothermal (exploration → production) | 4–7 yr | Exploration permit, drilling risk; phase the analysis (P50/P90 resource) |
| Biomass/EfW CHP | 5–8 yr | EIA (procjena utjecaja na okoliš) likely |
| DH transmission pipeline | ~1.5–2 yr permitting/design + construction at ~2–4 km/yr per front in urban terrain (faster greenfield) | e.g., 10 km urban ≈ 4–6 yr total from decision |
| Network expansion into new district | 2–4 yr per phase | Coordinate with road works |
| Seasonal pit TES | 3–5 yr | Land + geotechnics |

Rule: earliest commissioning = decision year (assume analysis year + 1 unless the document says the project is already in development) + lead time. If a scenario needs the asset earlier, the scenario must say what accelerates it (permits already obtained, design done) — otherwise adjust the timeline and register the assumption.

## 6. Spatial and resource caps — checklist per candidate

- Prostorni plan: is the site designated for energy/infrastructure use? If not, add plan-amendment time (1–3 yr) to the lead time.
- Solar thermal land: gross land ≈ 2.5–3.5 × collector aperture area.
- Geothermal: cap annual output at sustainable reservoir yield; carry exploration risk as scenario branch (success/failure), not as an average.
- Biomass: cap at demonstrable sustainable regional supply (require a supply-radius statement, e.g., ≤ 50–80 km); RED III sustainability criteria apply above thresholds.
- Waste heat: cap at contracted/contractible profile; apply an availability haircut (e.g., 80–90%) and model counterparty-exit as a risk case.
- Water-source HPs: thermal discharge limits and water rights; Water Protection Zones restrict some sites.
