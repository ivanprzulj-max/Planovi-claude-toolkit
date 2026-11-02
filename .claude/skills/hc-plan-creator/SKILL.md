---
name: hc-plan-creator
description: Create, revise, and audit municipal Heating & Cooling (H&C) plans (Planovi grijanja i hlađenja) under Article 25 and Annex X of the recast Energy Efficiency Directive (EU/2023/1791), following the ESCALATE project templates and REGEA methodology. Use this skill WHENEVER the user works on an H&C plan for any city — drafting new sections from city inputs, updating an existing plan with new data, checking or correcting figures against the Master Sheet, verifying EED compliance, or preparing the plan for delivery. Trigger also on Croatian phrasing like "plan grijanja i hlađenja", "PGH", "ESCALATE plan", "ažuriraj plan za [grad]", "provjeri plan prema Master Sheetu", or when a city H&C plan document and/or the Master Sheet is uploaded or referenced. For the scenario/LCOH optimization chapters themselves, this skill delegates to the hc-scenario-analysis skill — but document assembly, revision, and auditing always go through this skill.
---

# H&C Plan Creator (ESCALATE / EED Art. 25)

REGEA is an official partner of the EU project ESCALATE, which provides standardised templates, methodology, and guidelines for municipal Heating & Cooling plans under Article 25 and Annex X of the recast Energy Efficiency Directive (EU/2023/1791). This skill governs how those plans are drafted, revised, and audited. The plans are formal deliverables read by municipal decision-makers and reported to the European Commission — errors, unsourced numbers, or structural improvisation damage REGEA's credibility, so the rules below exist to protect the document's integrity, not to slow you down.

## The three workflows

Identify which workflow the user needs (they often combine):

1. **DRAFT** — write new sections or a new plan from city inputs.
2. **REVISE** — update an existing plan when new city data or corrections arrive.
3. **AUDIT** — verify consistency between the plan and the Master Sheet, and check EED compliance.

All three share the core rules below; workflow-specific steps follow.

## Core rules (apply always)

### 1. The template is canonical

Structure every plan according to the ESCALATE H&C plan template as implemented for the **City of Karlovac** (available in the Project files). This includes the sections REGEA added on **electricity grid analysis**, which the cities explicitly requested — these are part of the canonical ToC even though they go beyond the base ESCALATE template. Keep this exact ToC structure for every city's plan.

- Never invent alternative structures, merge sections, or reorder chapters.
- If the template and EED requirements appear to diverge for some section, do not resolve it silently: flag the divergence explicitly (which section, which EED provision, what the mismatch is) and let the user decide.
- If the Karlovac template is not present in the Project or conversation, stop and ask for it before drafting structure-dependent content.

### 2. The Master Sheet is the single source of numerical truth

The Master Sheet (Excel, maintained on the shared SharePoint ESCALATE location; typically uploaded to the Project or conversation) contains REGEA's calculations, including the documented methodology for missing, incomplete, or outdated data. Treat it as the **metadata source** for every number and figure in the plan.

- Every quantitative statement in the plan must trace to the Master Sheet or to a cited external source.
- **Correction order is strict**: if a number is wrong, correct it **in the Master Sheet first**, then propagate the correction into the plan. Never patch the plan text while leaving the Master Sheet stale — that creates two diverging sources of truth.
- When drafting or revising, always read the plan and the Master Sheet **in parallel** and note any conflicts between them in your output.
- If the Master Sheet is not available in context, say so explicitly and mark all affected figures as unverified — do not proceed as if verification had happened.

### 3. Source citation discipline

Plans are built from city-provided strategies and data, national/local strategies (energy, climate, spatial), and spatial databases (GIS layers, spatial plans, cadastres, energy statistics). When integrating any input:

- Cite the source document/dataset **and its date** at the point of use.
- Where sources conflict, present the conflict openly (both values, both sources, both dates) rather than picking one silently. Recommend which to use and why, but the choice is flagged for the user.

### 4. Data quality tagging

Distinguish clearly, in the text itself, between:

- **Mjereni podaci** (measured data) — with source and measurement period,
- **Modelirane procjene** (modelled estimates) — with method reference (usually the Master Sheet methodology),
- **Pretpostavke** (assumptions) — explicitly labelled, with rationale.

Missing data is an **open item for the city** (otvorena stavka), listed as such — never filled with an invented plausible value. Where REGEA's missing-data methodology in the Master Sheet provides an estimate, use that estimate and label it as a modelled value per that methodology.

### 5. Per-city separation

Each city's plan, data, and assumptions are strictly separate. Never reuse one city's figures, growth rates, or calibration parameters for another city without explicit instruction. If you notice a significant methodological or relative-data difference between city plans (e.g., very different specific heat demands, RES potentials, or scenario assumptions for comparable contexts), highlight it and **ask for confirmation before** going deeper into calculations or finalising the document.

### 6. EED compliance checking

Cross-check content against the EED requirements for local H&C planning: demand mapping, supply potentials (including waste heat and renewables), scenarios, policy measures, stakeholder involvement, and the further elements in `references/eed-compliance-checklist.md`. Read that file whenever performing an AUDIT or completing a full plan. Note gaps explicitly — a visible gap list is a deliverable feature, not a flaw. Use EED-defined terminology consistently (e.g., "učinkovito centralizirano grijanje i hlađenje" / "efficient district heating and cooling" strictly per the EED Art. 26 definition).

### 7. Language and tone

Plans are written in **Croatian**, formal and technical, suitable for municipal decision-makers and EC reporting. Working discussion with the user may be in whatever language they use, but all plan content, changelog entries, and audit findings destined for the document are in Croatian. Use official Croatian translations of EU terminology; where a term's Croatian rendering is ambiguous, give the English EED term in parentheses on first use.

## Workflow: DRAFT

1. Confirm which city and which sections. Locate the Karlovac-based template ToC and the city's Master Sheet in the Project/conversation.
2. Inventory available inputs (city strategies, national/local plans, GIS/spatial data, energy statistics) with dates. List what is missing as open items.
3. Draft section by section following the template. Pull every number from the Master Sheet; cite external sources with dates.
4. For scenario-analysis and LCOE/LCOH-optimization chapters, **invoke the `hc-scenario-analysis` skill** for the analytical work, then integrate its outputs into the plan structure with proper sourcing back to the Master Sheet.
5. Close with: open items list, source conflicts noted, and any template↔EED divergences flagged.

## Workflow: REVISE

These documents are living — repeated revision as new city inputs arrive is the normal mode, so revisions must be traceable.

1. Identify what changed in the inputs (new data, corrected data, new city feedback) and verify the change against the Master Sheet. If the new data contradicts the Master Sheet, the Master Sheet is corrected first (rule 2), then the plan.
2. Preserve the document structure exactly.
3. **Never silently delete prior content.** Mark superseded material as such (e.g., strikethrough or a clearly labelled "Zamijenjeno / superseded" note with date), so the document's history remains inspectable.
4. Record every change in the plan's **changelog section** (Evidencija izmjena) with: date, section affected, what changed, why, and the triggering source (which input/Master Sheet version). If the plan has no changelog section yet, add one.
5. Report back to the user: a summary of changes made, any Master Sheet corrections that were needed, and any conflicts or open items discovered along the way.

## Workflow: AUDIT

1. Read the plan and the Master Sheet in parallel.
2. Verify every figure in the plan against the Master Sheet: value, unit, reference year, and rounding. List every mismatch with location (section, table/figure number), plan value, Master Sheet value.
3. Check internal consistency: totals vs. components, shares summing to 100%, milestone-year trajectories monotonic where expected, no orphan numbers (values appearing without source or derivation).
4. Run the EED compliance check per `references/eed-compliance-checklist.md` and the template-conformance check against the Karlovac ToC.
5. Deliver a structured audit report: (a) plan↔Master Sheet mismatches, (b) internal inconsistencies, (c) EED gaps, (d) template deviations, (e) data-quality issues (unlabelled assumptions, missing sources/dates), (f) recommended correction order — Master Sheet corrections first, then plan corrections.
6. If the user's forensic auditing skill (`revizija-dokumenata`) is available and the user asks for a full forensic audit, it can be composed with this workflow; this skill contributes the ESCALATE/EED/Master-Sheet-specific checks.

## What to do when context is incomplete

This skill depends on Project-provided files: the Karlovac template/plan, the city's current plan, and the Master Sheet. When any of these are missing from context, name exactly which one is missing and what you cannot verify without it. Partial work is fine (e.g., prose improvement, structure checks) as long as every unverified number is visibly marked as unverified. Guessing at what the Master Sheet "probably says" is never acceptable.
