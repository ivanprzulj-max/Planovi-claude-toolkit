# Document corpora: conventions for REGEA / Novera projects

graphify's defaults assume a codebase. A folder of Croatian studies, spreadsheets and EU application drafts behaves differently, and the differences matter enough to be worth writing down.

## Contents

- [What to exclude](#what-to-exclude)
- [What counts as a node](#what-counts-as-a-node)
- [Relationships worth capturing](#relationships-worth-capturing)
- [Croatian-language pitfalls](#croatian-language-pitfalls)
- [Refresh cadence](#refresh-cadence)
- [Project tag conventions](#project-tag-conventions)

## What to exclude

Write a `.graphifyignore` before the first build. Document folders accumulate material that inflates the graph without adding signal:

```
# Versions and drafts
*_v[0-9]*.docx
*_stara*.docx
*_backup*
~$*
arhiva/
stare_verzije/

# Received, not authored
primljeno/
inbox/

# Binary and generated
*.zip
*.exe
graphify-out/converted/
```

Two judgment calls worth making deliberately:

**Draft versions.** Ten drafts of one study create ten near-identical node clusters that drown out everything else. Keep the current version; exclude the rest. If version history matters, that is what git or the file system is for.

**Received documents.** Ministry guidelines, EU call texts, partner submissions — these are genuinely useful context and genuinely different from authored material. Either exclude them or keep them in a clearly separate subfolder, so the graph does not blur "what we wrote" with "what we were sent". Blurring those two is how a claim from a call text ends up cited as your own analysis.

## What counts as a node

For code, nodes are functions and classes. For this material, the useful nodes are:

- **Documents** — each study, plan, application, contract
- **Projects and programmes** — ESCALATE, LIFE-2026-CET-PDA, BETTERRENO, Interreg
- **Organisations** — REGEA, HEP Toplinarstvo, Kraš, HBOR, partner municipalities
- **Places** — the city or municipality a plan covers
- **Regulatory instruments** — EED Art. 25, Annex X, NECP, ZOEU, HBOR credit lines
- **Quantitative anchors** — named scenarios, milestone years, KPI thresholds

That last category is the one people skip and then wish they hadn't. A node for "Scenarij 2030 — udio OIE 45%" is what lets you later ask which documents assume it, and find the three that quietly assume something else.

## Relationships worth capturing

- **cites / references** — one document points at another
- **derives-from** — a figure in one document was computed from data in another
- **supersedes** — a newer version replaces an older analysis
- **applies-to** — a regulatory instrument governs a document or project
- **prepared-for** — the client, ministry, or funding body

`derives-from` is the highest-value edge in this whole corpus and the easiest to lose. When a figure in a study came out of a spreadsheet, that link exists nowhere except in someone's memory. Capture it when the source is identifiable; mark it inferred when it is a reasonable guess.

## Croatian-language pitfalls

**Diacritics survive conversion.** Verified: č, ć, ž, š, đ come through `.docx` → markdown intact. No transliteration needed.

**Word heading levels do not survive.** The converter flattens Heading 1/2/3 to plain paragraphs. Document hierarchy that was carried only by heading styles is lost. If a study's structure matters, check `graphify-out/converted/` before trusting the graph's hierarchy.

**Case and inflection break exact matching.** Croatian declension means the same entity appears as "Grad Karlovac", "Grada Karlovca", "u Karlovcu". Query with the nominative form first; if it returns little, try a distinctive substring rather than assuming absence. This is the single most common cause of a false "no results" on this corpus.

**Mixed-language corpora are normal.** A project folder routinely holds Croatian studies alongside English EU applications describing the same work. The same concept then exists under two labels — "plan grijanja i hlađenja" and "heating and cooling plan". Query both when a search comes back thin.

## Refresh cadence

- **After adding or substantially revising a document** — rebuild that portion
- **Before submitting anything** to a bank, ministry, or EU agency — a stale graph during a final consistency check is worse than none, because it looks authoritative
- **Not after every small edit** — the noise is not worth it

`graphify check-update .` reports whether a semantic re-extraction is pending, which is a better signal than guessing from timestamps.

## Project tag conventions

Use `<organisation>-<project>`, lowercase, hyphenated, stable over time:

```
regea-escalate
regea-hc-planovi
regea-kras-zapresic
novera-krk
hep-life-pda
```

Stability matters more than elegance. Re-registering under a changed tag leaves the old entry orphaned in the global graph, and `graphify global list` becomes a list of things that may or may not still exist.
