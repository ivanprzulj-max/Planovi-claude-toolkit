# Inputs, Mandatory-Ask Protocol, and the Assumption Register

## 1. Input inventory — what to extract from the document and annexes

Read the entire study and all annexes before asking anything. Build this inventory (a simple table in your working notes):

### A. Demand side
| Item | Criticality |
|---|---|
| Base-year delivered heat (MWh/yr) per zone/sector, and whether it is climate-normalized | CRITICAL |
| Peak load (MW_th) or hourly/monthly load profile, or full-load hours | CRITICAL |
| Number of connections, connected area (m²), specific consumption (kWh/m²) | High |
| Planned network expansion / densification (new demand, MWh/yr per period) | High |
| Renovation program: rate (%/yr or m²/yr), depth (shallow/medium/deep), specific savings | CRITICAL if EE savings are a KPI |
| Cooling demand in scope? | High |
| Domestic hot water share (determines summer base load → solar thermal / waste heat value) | High |

### B. Existing supply and network
| Item | Criticality |
|---|---|
| Existing units: fuel, capacity, efficiency, age, expected retirement year | CRITICAL |
| Network: length, temperature regime (supply/return °C), losses (% or MWh), pressure zones | CRITICAL |
| Temperature-reduction potential (lower regimes enable HP/solar/waste heat) | High |
| Central connection points for new sources; hydraulic constraints | High |

### C. Candidate measures and potentials
| Item | Criticality |
|---|---|
| List of candidate sources with capacity and annual potential (geothermal, HP + heat source, biomass, solar thermal, waste heat, EfW, TES, e-boilers, CHP) | CRITICAL |
| Resource caps: sustainable biomass supply (t/yr → MWh/yr), geothermal well yield (l/s, °C), waste-heat availability profile and counterparty | CRITICAL |
| Spatial planning status per site (prostorni plan namjena, permits obtained/pending) | CRITICAL |
| Distance from each new source to the network connection point (→ pipeline km and cost) | CRITICAL |
| Grid connection capacity for large HPs / e-boilers (HEP-ODS/OPS constraints) | High |

### D. Financial and market parameters
| Item | Criticality |
|---|---|
| Discount rate / WACC (real or nominal, and for whom — utility, municipality, societal) | CRITICAL |
| CAPEX/OPEX per measure (if given in the document, these override catalog defaults) | CRITICAL |
| Fuel and electricity price assumptions and trajectories | CRITICAL |
| CO₂ price trajectory (EU ETS; ETS2 from 2027 for buildings/small combustion) | High |
| Grants/subsidies assumed (NPOO, Modernisation Fund, EU funds, HBOR) and their treatment | High |
| Heat tariff context (HERA methodology) if tariff impact must be shown | Medium |

### E. Targets and constraints
| Item | Criticality |
|---|---|
| KPI minima per milestone year (RES share, savings %, CO₂, efficient-DH status) — as stated in the document or derived from EED/NECP | CRITICAL |
| Milestone years (default 2030, 2035, 2040, 2045, 2050 if unstated) | High |
| Security-of-supply requirements (reserve capacity, n-1) | High |
| Any political/contractual constraints (e.g., coal/gas phase-out dates, PPA commitments) | Medium |

## 2. Mandatory-ask protocol

Ask the user (in their language, concisely, grouped in one message) when ANY item marked CRITICAL is missing, ambiguous, or contradicted elsewhere in the document. Good asking practice:

- Group questions by theme; number them; for each, offer the default you would otherwise assume, so the user can simply confirm. Example: *"3. Dokument ne navodi WACC. Predlažem realni WACC 5% (komunalno poduzeće, dugoročno financiranje). Potvrđujete ili želite drugu vrijednost?"*
- Distinguish "blocking" questions (analysis cannot proceed meaningfully) from "default-able" questions (you will proceed with a registered assumption unless corrected).
- If the user explicitly says "proceed with assumptions", proceed — but flag in the deliverable's executive summary that results are conditional on the register.
- Internal inconsistencies in the document (e.g., demand table ≠ sum of zone tables) are treated like missing inputs: ask, or reconcile transparently and document which figure was adopted and why.

## 3. Assumption Register — mandatory format

Every input not taken verbatim from the document gets a row. This register is an annex of the deliverable and is referenced in-text as (A-xx).

| ID | Parameter | Adopted value | Basis / source | Type | Sensitivity-tested? |
|---|---|---|---|---|---|
| A-01 | Real WACC | 5.0% | Consultant default for municipal DH utility; user confirmed | Financial | Yes (3–8%) |
| A-02 | New DN400 transmission pipeline, geothermal site → CTS node, 10 km | Commissioned 2031 | 2 yr permitting/design + 3 yr construction @ ~3 km/yr urban; catalog lead-time table | Feasibility | Yes (±2 yr) |
| A-03 | Biomass fuel price | 38 EUR/MWh_fuel real 2026, +0.5%/yr | Catalog range midpoint; no local supply study available | Market | Yes |

Types: Financial, Technical, Market, Feasibility, Regulatory, Demand.

Rules:
- An assumption that materially drives the result (changes ranking of measures or KPI pass/fail) MUST be sensitivity-tested and called out in the executive summary.
- Never blend document data and assumed data in one figure without a footnote separating them.
- If the user later supplies a real value, update the register (do not delete the history — mark superseded).
