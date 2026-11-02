"""
lcoh_model.py — plan-level LCOH, merit-order dispatch and greedy least-cost
capacity expansion for Heating & Cooling Plan scenario analysis.

Pure stdlib. Real-terms convention: pass real discount rate with real prices.
All heat quantities in MWh, capacities in MW_th, costs in EUR unless noted.

Usage sketch:
    from lcoh_model import Technology, annuity, lcoh_simple, dispatch_ldc, greedy_expand
See __main__ at the bottom for a worked example; adapt inputs per project and
keep the input dict in the deliverable annex for auditability.
"""
from dataclasses import dataclass, field
from typing import Optional


def annuity(rate: float, lifetime_years: int) -> float:
    """Capital recovery factor. rate is real discount rate (e.g. 0.05)."""
    if rate == 0:
        return 1.0 / lifetime_years
    return rate * (1 + rate) ** lifetime_years / ((1 + rate) ** lifetime_years - 1)


@dataclass
class Technology:
    name: str
    capacity_mw: float                  # thermal capacity at handover point
    capex_eur: float                    # total investment incl. dedicated infrastructure
    fixed_om_eur_yr: float              # fixed O&M per year
    var_om_eur_mwh: float               # variable O&M per MWh heat
    fuel_eur_mwh_fuel: float = 0.0      # fuel price per MWh fuel input
    efficiency: float = 1.0             # heat out / fuel in (boilers); ignored if spf set
    spf: Optional[float] = None         # heat pumps: heat out / electricity in
    el_price_eur_mwh: float = 0.0       # electricity price (HP, e-boiler)
    co2_t_per_mwh_fuel: float = 0.0     # emission factor per MWh fuel (gas ~0.202)
    co2_price_eur_t: float = 0.0
    lifetime: int = 25
    availability: float = 0.95          # share of hours available
    max_annual_mwh: Optional[float] = None  # resource cap (geothermal/biomass/WH)
    must_run: bool = False              # contracted waste heat etc.
    is_res_share: float = 0.0           # share of output counting as RES (HP: 1-1/SPF)
    is_wasteheat_share: float = 0.0
    earliest_year: int = 2026           # feasibility: earliest commissioning
    grant_eur: float = 0.0              # deducted for granted-LCOH variant only

    def srmc(self) -> float:
        """Short-run marginal cost EUR/MWh heat (merit-order key)."""
        if self.spf:
            energy = self.el_price_eur_mwh / self.spf
            co2 = 0.0
        else:
            energy = self.fuel_eur_mwh_fuel / max(self.efficiency, 1e-9)
            co2 = self.co2_t_per_mwh_fuel * self.co2_price_eur_t / max(self.efficiency, 1e-9)
        return energy + co2 + self.var_om_eur_mwh

    def annualized_fixed(self, rate: float, granted: bool = False) -> float:
        capex = self.capex_eur - (self.grant_eur if granted else 0.0)
        return capex * annuity(rate, self.lifetime) + self.fixed_om_eur_yr

    def lcoh(self, rate: float, annual_mwh: float, granted: bool = False) -> float:
        """LCOH at a given dispatch level (EUR/MWh into network)."""
        if annual_mwh <= 0:
            return float("inf")
        return self.annualized_fixed(rate, granted) / annual_mwh + self.srmc()


def make_ldc(annual_mwh: float, peak_mw: float, n: int = 8760) -> list:
    """Two-parameter load duration curve approximation calibrated to
    annual energy and peak. Register as assumption if no real profile exists."""
    if peak_mw * 8760 < annual_mwh:
        raise ValueError("Peak too low for annual energy.")
    # load(h) = peak * (1 - (h/n)^p); larger p => curve stays near peak longer
    # => more energy. Bisect p so annual energy matches.
    lo, hi = 0.01, 200.0
    for _ in range(100):
        p = (lo + hi) / 2
        e = sum(peak_mw * max(0.0, 1 - (h / n) ** p) for h in range(n)) * (8760 / n)
        if e < annual_mwh:
            lo = p
        else:
            hi = p
    p = (lo + hi) / 2
    return [peak_mw * max(0.0, 1 - (h / n) ** p) for h in range(n)]


def dispatch_ldc(techs: list, ldc: list) -> dict:
    """Merit-order dispatch against an LDC. Must-run units first, then by SRMC.
    Returns {tech.name: annual_mwh}. Respects availability and resource caps."""
    hours_scale = 8760 / len(ldc)
    order = sorted(techs, key=lambda t: (not t.must_run, t.srmc()))
    residual = list(ldc)
    out = {}
    for t in order:
        cap = t.capacity_mw * t.availability
        served = 0.0
        for i, load in enumerate(residual):
            take = min(cap, load)
            served_i = take * hours_scale
            if t.max_annual_mwh is not None and served + served_i > t.max_annual_mwh:
                served_i = max(0.0, t.max_annual_mwh - served)
                take = served_i / hours_scale
            residual[i] = load - take
            served += served_i
        out[t.name] = served
    out["_unserved_mwh"] = sum(residual) * hours_scale
    return out


def system_metrics(techs: list, dispatch: dict, rate: float,
                   loss_share: float, network_annual_cost: float = 0.0,
                   granted: bool = False) -> dict:
    """System LCOH per MWh DELIVERED (after losses), RES and WH shares at handover."""
    produced = sum(v for k, v in dispatch.items() if not k.startswith("_"))
    delivered = produced * (1 - loss_share)
    cost = network_annual_cost
    res = wh = 0.0
    for t in techs:
        q = dispatch.get(t.name, 0.0)
        cost += t.annualized_fixed(rate, granted) + t.srmc() * q
        res += q * t.is_res_share
        wh += q * t.is_wasteheat_share
    return {
        "produced_mwh": produced,
        "delivered_mwh": delivered,
        "system_lcoh_eur_mwh": cost / delivered if delivered > 0 else float("inf"),
        "res_share": res / produced if produced > 0 else 0.0,
        "wasteheat_share": wh / produced if produced > 0 else 0.0,
        "unserved_mwh": dispatch.get("_unserved_mwh", 0.0),
    }


def greedy_expand(existing: list, candidates: list, ldc: list, year: int,
                  rate: float, loss_share: float,
                  min_res_share: float = 0.0, min_res_wh_share: float = 0.0,
                  network_annual_cost: float = 0.0) -> dict:
    """Add feasible candidates (earliest_year <= year), cheapest marginal system
    LCOH first, until unserved energy ~0 and KPI minima met. Returns fleet + metrics.
    Candidates are added whole; split a large option into tranches upstream if
    partial sizing should be allowed."""
    fleet = list(existing)
    pool = [c for c in candidates if c.earliest_year <= year]
    added = []
    for _ in range(len(pool) + 1):
        d = dispatch_ldc(fleet, ldc)
        m = system_metrics(fleet, d, rate, loss_share, network_annual_cost)
        ok = (m["unserved_mwh"] < 1e-3 * sum(ldc) * 8760 / len(ldc)
              and m["res_share"] >= min_res_share - 1e-9
              and (m["res_share"] + m["wasteheat_share"]) >= min_res_wh_share - 1e-9)
        if ok or not pool:
            m["added"] = [t.name for t in added]
            m["dispatch"] = {k: round(v) for k, v in d.items()}
            m["feasible"] = ok
            return m
        best, best_lcoh = None, float("inf")
        for c in pool:
            trial = fleet + [c]
            dt = dispatch_ldc(trial, ldc)
            mt = system_metrics(trial, dt, rate, loss_share, network_annual_cost)
            # prefer candidates that reduce unserved/KPI gap; rank by system LCOH
            if mt["system_lcoh_eur_mwh"] < best_lcoh:
                best, best_lcoh = c, mt["system_lcoh_eur_mwh"]
        fleet.append(best); added.append(best); pool.remove(best)
    return {"feasible": False}


if __name__ == "__main__":
    r = 0.05
    ldc = make_ldc(annual_mwh=180_000, peak_mw=90, n=876)
    gas = Technology("Existing gas HOB", 90, 0, 400_000, 1.5,
                     fuel_eur_mwh_fuel=40, efficiency=0.92,
                     co2_t_per_mwh_fuel=0.202, co2_price_eur_t=90)
    hp = Technology("Sewage HP 20 MW", 20, 22_000_000, 300_000, 1.5,
                    spf=3.3, el_price_eur_mwh=110, lifetime=25,
                    is_res_share=1 - 1 / 3.3, earliest_year=2029)
    bio = Technology("Biomass HOB 15 MW", 15, 10_500_000, 250_000, 4,
                     fuel_eur_mwh_fuel=38, efficiency=0.9, lifetime=25,
                     is_res_share=1.0, max_annual_mwh=90_000, earliest_year=2029)
    res = greedy_expand([gas], [hp, bio], ldc, year=2030, rate=r,
                        loss_share=0.13, min_res_share=0.50)
    print(res)
