# Methodology: LCOH, Dispatch, Optimization, Sensitivity

## 1. Price basis and discounting

- Work in **real terms** (constant EUR of a stated base year) with a **real discount rate**, OR fully nominal with a nominal rate — never mix. Default: real.
- Discount rate defaults (register as assumptions if not given):
  - Municipal/regulated DH utility financial analysis: **real WACC 4–6%**.
  - Private developer: real WACC 6–9%.
  - Societal/economic analysis (EU CBA context): social discount rate ~3% real (verify current EC Economic Appraisal Vademecum guidance before citing).
- State whether prices include VAT (normally: excluding VAT for utility analysis).

## 2. Levelized Cost of Heat (LCOH) — technology level

For a single measure/plant over lifetime T:

LCOH = [ Σ_{t=0..T} (I_t + M_t + F_t + E_t + C_t − R_t) / (1+r)^t ] / [ Σ_{t=1..T} Q_t / (1+r)^t ]

where per year t: I = investment (incl. dedicated infrastructure: connection pipeline, substation, grid connection, land, development costs, contingency), M = fixed + variable O&M, F = fuel cost, E = electricity cost (HPs, e-boilers, pumps), C = CO₂ cost (allowance exposure), R = revenues/by-products credited (e.g., electricity from CHP, cooling sales), Q = **useful heat delivered into the network** (MWh).

Conventions:
- Denominator uses heat **into the network at the handover point** for technology LCOH (consistent with EED Art. 26 measurement point). Losses are then charged at system level.
- Include **reinvestment** for components with lifetime < analysis horizon and **residual value** (straight-line) for lifetime > horizon.
- Heat pumps: annual electricity = Q_th / SPF (seasonal, not nameplate COP). SPF depends on source and sink temperatures — document the temperature regime assumption.
- CHP: either (a) credit electricity revenue in the numerator (recommended, transparent), or (b) allocate costs by energy/exergy — state the method; never both.
- Grants: compute **LCOH_ungranted** (for economic ranking of measures) and **LCOH_granted** (grant deducted from I_0; for tariff realism). Rank measures by ungranted LCOH unless the user's decision context is explicitly tariff-driven.

## 3. System LCOH — what actually gets minimized

System LCOH for a scenario in analysis window [t0, T]:

LCOH_sys = [ Σ_t PV(all supply costs + network CAPEX/OPEX + storage + losses' cost is implicit) ] / [ Σ_t PV(Q_delivered_to_customers) ]

- Denominator = heat **delivered to customers** (after network losses). This automatically penalizes lossy configurations and rewards network refurbishment and temperature reduction.
- Demand-side (EE/renovation) measures enter in two consistent ways — choose ONE and state it:
  1. **Demand-vector approach (default):** renovation reduces Q in the denominator and avoids supply costs in the numerator; renovation costs themselves are NOT in LCOH_sys but reported separately as cost of conserved energy (CCE, EUR/MWh saved) and compared against marginal supply LCOH. A renovation measure is "in the optimum" when CCE < marginal LCOH of displaced supply.
  2. **Total-system-cost approach:** include renovation costs in the numerator and use pre-renovation demand as denominator — use when the user wants a single total-cost metric.
- CCE = (annualized renovation CAPEX × attribution share to heating) / annual MWh saved. Attribute only the heating-related share of integral renovation cost when the renovation is multi-purpose (typical heating-attributable share 40–70%; register the assumption).

## 4. Adequacy constraints (must hold before cost matters)

Per milestone year y and scenario s:
- **Energy:** Σ feasible annual output of commissioned units ≥ produced heat requirement = delivered demand / (1 − loss share).
- **Capacity:** Σ firm capacity ≥ peak load × (1 + reserve margin). Non-firm sources (solar thermal) count at their coincident-peak contribution (≈0 for winter-peaked systems unless seasonal TES). If the document requires n-1: peak must be covered with the largest unit out.
- **Ramp/seasonality sanity check:** monthly balance if profiles are available; at minimum check summer (DHW-only) operation — who runs in summer at what marginal cost (this is where solar thermal / waste heat / HP typically win).

## 5. Dispatch model (operational level)

- Build/borrow the load-duration curve (LDC). If only annual energy + peak are known, approximate LDC with a two-parameter form calibrated to full-load hours; register the approximation.
- Merit order by **short-run marginal cost** (fuel/SPF-adjusted electricity + variable O&M + CO₂), subject to availability, must-run (waste heat contracts, CHP heat-led obligations), and capacity limits.
- Annual output of unit i = area under LDC allocated to i in merit order. Storage shifts energy from low- to high-merit hours; model at least seasonal TES as: charge from cheapest summer source, discharge displacing the marginal winter unit, with round-trip efficiency 60–80% (pit, seasonal) / 90–98% (short-term tank).

## 6. Investment optimization algorithm (capacity expansion)

Greedy least-cost with constraints — transparent and defensible for plan-level studies:

1. For each milestone year, compute the **gap**: energy and capacity shortfall after retirements and demand change, plus **KPI gap** (e.g., additional RES MWh needed to reach the minimum share).
2. Enumerate feasible candidates for that year (earliest commissioning ≤ y; resource cap not exhausted; build-out rate respected).
3. Rank candidates by marginal system LCOH contribution = ΔPV(cost)/ΔPV(delivered heat), computed **against the dispatch they would actually get** (a baseload geothermal unit and a peak e-boiler must not be compared at equal full-load hours).
4. Add the cheapest candidate; re-dispatch; repeat until energy, capacity AND all KPI minima are met.
5. If a KPI minimum cannot be met with feasible candidates → the scenario is infeasible for that milestone; report the earliest feasible compliance year and the binding constraint (this is a key deliverable insight, not a failure of the analysis).
6. **Marginal cost of compliance** = LCOH_sys(with KPI constraints) − LCOH_sys(adequacy only). Report it — decision-makers need to see what the KPI costs.

For large candidate sets or strong interactions (storage + variable sources), verify the greedy result with an LP/MILP (Python `pulp` or `scipy.optimize.linprog`; or note that energyPRO/EnergyPLAN modelling is recommended for the detailed design phase). Plan-level greedy + LP cross-check is the right rigor level; do not overclaim hourly-model precision.

## 7. Multi-period consistency

- Decisions are cumulative: capacity commissioned for 2030 remains available in 2035+ (until retirement). Optimize the **pathway**, not isolated snapshots — a slightly more expensive 2030 choice can be optimal if it avoids stranded assets by 2040 (e.g., do not add a new gas boiler in 2029 that EED Art. 26 logic strands by 2035; note the EED ban on new fossil generation capacities in efficient DH systems).
- Perform a **stranding check**: any asset whose remaining life extends past a milestone where it can no longer count toward the KPI mix must either (a) be justified as peak/reserve, or (b) have its early-retirement cost included.

## 8. Sensitivity analysis

- **Tornado:** one-at-a-time ±X% on WACC (±2 pp), electricity price (±30%), fuel prices (±30%), CO₂ price (low/central/high trajectory), CAPEX (±20%, ±30% for geothermal/novel), demand (±10%), SPF (±0.3), on both LCOH_sys and the KPI pass/fail matrix.
- **Switching values:** report the parameter value at which the ranking of the top two measures flips, and at which a KPI fails.
- **Scenario robustness:** identify no-regret measures (in the optimum across all sensitivity runs) vs. contingent measures. Structure the recommendation around this distinction.

## 9. Croatian-context financial specifics

- ETS1 applies to combustion installations > 20 MW_th rated thermal input; ETS2 (from 2027) covers fuels for buildings/small combustion — it raises the cost of the **individual heating counterfactual** and of sub-threshold fossil heat-only boilers; include it in the counterfactual comparison and in gas-boiler variable cost.
- Heat tariffs regulated per HERA methodology — if the user needs tariff impact, translate annualized costs to EUR/kWh delivered and compare with current tariff; do not promise tariff outcomes (regulatory decision).
- Typical funding stack: NPOO/EU cohesion funds, Modernisation Fund, HBOR; grant intensity assumptions must be registered and never treated as certain in the base case unless contracted.
