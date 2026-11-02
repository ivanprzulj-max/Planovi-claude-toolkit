---
name: hc-scenario-analysis
description: Techno-financial scenario analysis and least-cost (LCOE/LCOH) optimization of renewables (RES/OIE) and energy efficiency measures for Heating & Cooling Plans (Planovi grijanja i hlađenja) and district heating (CTS) decarbonization roadmaps. Use WHENEVER the user asks to analyze technical potential of RES/waste heat/EE measures, build supply-demand scenarios for milestone years (2030/2035/2040/2045/2050), find the optimal least-cost combination of measures meeting KPI minima (RES share, savings %, EED Art. 26 efficient-DH status), compute or compare LCOE/LCOH of heat supply options, or check feasibility of an investment timeline in a heating/cooling study. Trigger also on Croatian phrasing like "scenarijska analiza", "tehnički potencijal OIE", "optimalna kombinacija mjera", "LCOE toplinske energije", "dekarbonizacija CTS-a", "udio OIE", and whenever a study with energy demand/supply figures is provided and an optimization or compliance analysis is wanted.
---

# Heating & Cooling Plan Scenario Analysis & Least-Cost Optimization

Purpose: from a source study (document + annexes), produce a rigorous, auditable techno-financial analysis that identifies the **optimal combination of supply measures (RES, waste heat, storage, networks) and demand measures (EE/renovation)** which, in each milestone year (typically 2030, 2035, 2040, 2045, 2050):

1. **covers the projected heat (and cooling) demand** with adequate capacity and energy (primary constraint),
2. **meets or exceeds all minimum KPIs** cumulatively (RES share, waste-heat share, savings %, EED Art. 26 "efficient DH" status, CO₂ intensity, national/NECP targets),
3. **is technically and administratively feasible** in the stated timeframe (lead times, spatial planning, resource caps, build-out rates),
4. **at the lowest achievable system cost of heat (LCOH / "LCOE thermal")**.

The analysis is only as credible as its inputs — this skill is therefore built around a strict **input audit → ask → assumption register** discipline before any number is produced.

## Reference files — read before the relevant phase

| File | Read when |
|---|---|
| `references/inputs-and-assumptions.md` | ALWAYS FIRST. Input checklist, mandatory-ask protocol, assumption register format. |
| `references/methodology.md` | Before any calculation. LCOH formulas, dispatch/merit order, optimization algorithm, sensitivity method. |
| `references/technology-catalog.md` | When characterizing candidate measures or when the document lacks technoeconomic parameters/lead times. |
| `references/kpi-compliance.md` | When defining KPI constraints (EED Art. 26 trajectory, RED accounting rules, HR national framework). |
| `references/report-template.md` | Before writing the deliverable. |
| `scripts/lcoh_model.py` | For any numeric run — use it instead of hand arithmetic. |

## Workflow

### Phase 0 — Input audit (GATE — do not skip)

Read the source document and every annex completely. Extract into a structured inventory: demand data, network data, existing plant, candidate measures, resource potentials, constraints, financial parameters, KPI targets. Follow `references/inputs-and-assumptions.md`.

**Mandatory-ask rule:** if any *critical* input (defined in the checklist) is missing, ambiguous, or internally inconsistent, ASK THE USER before finalizing the analysis. Never silently invent a critical input. If the user cannot supply it, adopt a defensible default from `references/technology-catalog.md`, record it in the **Assumption Register** (ID, value, rationale, source, sensitivity flag), and state it explicitly in the deliverable — e.g. *"Assumption A-07: 10 km of new DN400 transmission pipeline from the geothermal site to the CTS connection point is realistically commissioned by 2031 (2 yrs permitting/design + 3 yrs construction at ~3 km/yr in urban terrain)."* Non-critical gaps may be filled with catalog defaults without asking, but still go into the register.

### Phase 1 — Demand projection

- Establish the baseline: useful vs. final vs. delivered heat; climate-normalize (HDD) the base year.
- Project demand per milestone year as: baseline − EE savings (renovation rate × specific savings by depth) + new connections/densification + cooling where in scope.
- Derive peak load and load-duration curve (typical CTS full-load hours 1,800–2,400 h/yr in continental Croatia; verify against document).
- Network losses: model delivered vs. produced heat explicitly (typically 8–18% for existing HR systems).

### Phase 2 — Supply option characterization

For every candidate measure record: capacity, annual output potential, efficiency/COP/SPF, availability, specific CAPEX (incl. connection infrastructure — pipelines, substations, grid reinforcement), fixed and variable OPEX, fuel/electricity price exposure, CO₂ cost exposure (ETS1/ETS2), lifetime, **development lead time (permitting + design + construction)**, earliest realistic commissioning year, spatial footprint and planning status (prostorni plan compliance), and resource cap (sustainable biomass supply, geothermal reservoir yield, waste-heat availability and counterparty risk, land for solar thermal). Use `references/technology-catalog.md` for any parameter the document does not provide — and register it as an assumption.

### Phase 3 — Scenario construction

Build at least three scenarios unless the document dictates otherwise: **Reference/BAU**, **Moderate**, **Ambitious/Compliance-driven**. Apply feasibility screening first: a measure's earliest commissioning year = decision year + lead time; cap annual build-out rates (km network/yr, MW/yr, renovated m²/yr). A scenario that meets KPIs only via infeasible timing is invalid — flag it, do not present it as viable.

### Phase 4 — Least-cost optimization

Two-level problem per `references/methodology.md`:
- **Dispatch** (operational): merit order by short-run marginal cost against the load-duration curve, respecting availability and must-run constraints.
- **Investment** (capacity expansion): greedy least-cost screening — iteratively add the feasible measure with the lowest marginal system LCOH contribution until (a) energy/capacity adequacy and (b) all KPI minima are satisfied in each milestone year. Optionally verify with an LP/MILP formulation (scipy/pulp) for larger systems.
- Report **technology-level LCOH** and **system LCOH** per milestone year, and the **marginal cost of KPI compliance** (system LCOH with vs. without the binding KPI constraint).
- Compute LCOH both **with and without grants** — grant-adjusted for tariff realism, ungranted for economic ranking.

### Phase 5 — KPI verification

Cumulative energy balance per milestone year; RES share with correct accounting (heat-pump renewable fraction per RED Annex VII: E_RES = Q_usable × (1 − 1/SPF), SPF eligibility threshold); waste-heat share; EED Art. 26(1) efficient-DH status per period (see `references/kpi-compliance.md` — thresholds tighten in 2028, 2035, 2040, 2045, 2050) and/or the alternative GHG-intensity path; savings % vs. baseline. Present a pass/fail compliance matrix (scenario × milestone × KPI).

### Phase 6 — Sensitivity and risk

Tornado analysis on: WACC/discount rate, electricity and fuel prices, CO₂ price (ETS2 from 2027 matters for the individual-heating counterfactual and sub-threshold plants), CAPEX (±30% for immature options), demand trajectory, SPF/COP. Identify switching values (parameter value at which the optimal mix changes). Qualitative risk register for non-quantifiable risks (geothermal exploration risk, waste-heat counterparty longevity, permitting delays).

### Phase 7 — Deliverable

Follow `references/report-template.md`. Write in the language of the source document (usually Croatian) unless told otherwise; keep formulas and technology names bilingual where helpful. Every figure must trace to a document citation or an Assumption Register ID — no orphan numbers. Include the compliance matrix, LCOH waterfall/comparison, investment timeline (Gantt-style by measure), and the full assumption register as an annex.

## Non-negotiable quality rules

- **Adequacy before cost:** never present a mix that fails the energy balance or peak capacity (incl. n-1 reasoning for the largest unit where the document requires security of supply).
- **Feasibility before ambition:** timing claims must survive the lead-time test. State the commissioning logic for every new asset.
- **No silent assumptions:** every non-document input has a register entry and appears in the report.
- **Consistent money:** one price basis (real, stated base year, EUR), one discount rate convention (real WACC with real prices), declared throughout.
- **Units discipline:** MWh vs. GWh, useful vs. delivered vs. produced heat, MW_th vs. MW_e — label everything; reconcile totals to the document.
- **Reproducibility:** run numbers through `scripts/lcoh_model.py` (or an equivalent transparent spreadsheet) and preserve the input file so the client can audit.
