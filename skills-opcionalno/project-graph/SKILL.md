---
name: project-graph
description: "Maintain and consult a persistent knowledge graph of a project folder (REGEA, Novera, EU-projekti, studije, H&C planovi). Use this at the START of work in any project folder that has, or should have, a graphify-out/ directory — consult the graph before grepping or reading files, so answers are grounded in the whole corpus instead of whichever file happened to get opened. Trigger whenever the user asks anything about what is in a project, how documents relate, where a figure or assumption came from, what would be affected by a change, or asks to build/refresh/register a project graph. Trigger also on Croatian phrasing like 'što imamo o', 'gdje smo ovo pisali', 'iz kojeg dokumenta je ovaj broj', 'poveži dokumente', 'napravi graf projekta', 'osvježi graf'. Applies to document corpora (.docx/.xlsx/.pdf/.md) as much as to code."
---

# project-graph

Wraps the `graphify` tool into a per-project lifecycle: build once, consult constantly, refresh when stale.

This skill does **not** reimplement graphify's extraction pipeline. For a fresh build it hands off to the `graphify` skill. What it owns is everything around that: deciding whether to consult or rebuild, keeping graphs current, registering them for cross-project lookup, and applying conventions that suit document corpora rather than codebases.

## The core habit

Reading files one at a time is how context gets lost. A study cites a figure, the figure came from a spreadsheet three folders over, and nobody remembers which. The graph exists to answer that in one hop.

So: **when a project folder has a graph, query it before touching the filesystem.** Not instead of reading files — before, so you know which files to read.

## Step 1 — Orient

At the start of substantive work in a project folder, check state:

```bash
ls graphify-out/graph.json 2>/dev/null && graphify check-update . 2>&1 | tail -5
```

Three outcomes:

| State | What it means | Go to |
|---|---|---|
| `graph.json` exists, no update pending | Graph is current | Step 2 (consult) |
| `graph.json` exists, update pending | Corpus drifted since last build | Step 3 (refresh), then Step 2 |
| No `graph.json` | Never built here | Step 4 (bootstrap) |

Do this once per session, not once per message. Once you know the state, keep working from it.

## Step 2 — Consult before reading

Pick the query shape that matches the question. Do not default to `query` for everything — the other commands are cheaper and more precise.

| Question shape | Command |
|---|---|
| "What do we have about X?" / open-ended | `graphify query "X" --budget 2000` |
| "Where did this number come from?" | `graphify query "X" --dfs` — traces one path rather than fanning out |
| "How do A and B connect?" | `graphify path "A" "B"` |
| "What is X, in plain terms?" | `graphify explain "X"` |
| "If I change X, what breaks?" | `graphify affected "X" --depth 2` |
| "What are the central documents here?" | `graphify god-nodes --top 10` |

Then read the specific files the graph points at. The graph tells you *where to look*; the files are still the source of truth for exact figures and wording. Never quote a number from graph output as if it were from the document — open the document.

### Feeding results back

When a query genuinely resolved something, record it so the graph learns which nodes are load-bearing:

```bash
graphify save-result --question "..." --answer "..." --nodes "Node A" "Node B" --outcome useful
```

Use `--outcome dead_end` when the graph sent you somewhere useless, and `--outcome corrected --correction "..."` when it was actively wrong. This costs one command and makes `graphify reflect` worth running later. Skip it for trivial lookups — logging everything just adds noise.

## Step 3 — Refresh a stale graph

For code and markdown changes, the incremental path needs no LLM and takes seconds:

```bash
graphify update .
```

For document corpora (`.docx`, `.xlsx`, `.pdf`), `update` will not re-derive semantic relationships on its own — those came from a reasoning pass, not an AST parse. When docs have changed materially, re-run the graphify skill's extraction on the changed files rather than relying on `update`.

If the rebuild produces fewer nodes than before, graphify refuses to overwrite by default. That guard is correct — investigate before overriding it. Only pass `--force` when you know why the corpus shrank (documents were genuinely deleted or consolidated). A silent node drop usually means extraction failed partway, not that the project got smaller.

After any rebuild, re-register the graph (Step 5).

## Step 4 — Bootstrap a new project graph

First confirm the tool is present. **The PyPI package is `graphifyy`, not `graphify`** — `pip install graphify` fails with "no matching distribution", which is a confusing error to hit:

```bash
graphify --version || pip install graphifyy --break-system-packages
```

Then hand off to the graphify skill to run the full pipeline on the folder. Before doing so, apply the conventions in `references/document-corpora.md` — for REGEA/Novera material the defaults tuned for source code will pull in noise and miss the relationships that actually matter.

Two things to know before starting a doc-heavy build:

- **Headless `graphify extract` requires an LLM API key** for any `.docx`/`.pdf`/`.xlsx`/`.md` file. It errors out without one. The skill-driven path does not — there, the reasoning pass *is* the extraction, so no key is needed. For document corpora, use the skill-driven path.
- **Office files are converted to markdown sidecars first**, into `graphify-out/converted/`. Croatian diacritics survive this intact, but Word heading levels flatten to plain paragraphs, so structure that was carried by heading hierarchy alone gets lost. If document structure matters, check the sidecar before trusting the graph's sense of hierarchy.

## Step 5 — Register for cross-project lookup

Each project keeps its own graph. Registering it into the global graph makes it reachable later without merging corpora:

```bash
graphify global add graphify-out/graph.json --as <project-tag>
graphify global list
```

Use a stable, obvious tag — the project folder name is usually right (`regea-escalate`, `novera-krk`, `hep-life-pda`). Re-register after every rebuild; the entry is replaced, not duplicated.

To query across everything registered, point at the global graph:

```bash
graphify query "..." --graph "$(graphify global path)"
```

## Step 6 — Wire up automatic consultation

Skill descriptions trigger probabilistically. Project instructions are always in context. So the reliable way to make this automatic is to put it in the project's instructions, not to rely on this skill firing.

When setting up a project, generate a block for the user to paste into the Cowork project's instructions:

```
This project has a graphify knowledge graph at graphify-out/graph.json.
Before answering questions about the contents of this project, or before
searching or reading files to find something, run a graphify query first
and use the result to decide which files to open. Do not answer from a
single file when the graph shows related material elsewhere.
Refresh the graph with `graphify update .` if it looks stale.
```

Adjust the wording to the project, but keep the two load-bearing parts: *query before file-reading*, and *the graph decides what to read*. Tell the user plainly that this paste-in step is what makes it automatic — the skill alone will not guarantee it.

For git-backed projects, `graphify hook install` adds post-commit and post-checkout hooks that keep the graph fresh without manual refresh. Offer it; don't install it unprompted, since it writes into `.git/hooks`.

## Honesty rules

The graph is a map, not the territory, and it is built partly by inference.

- Distinguish what the graph *extracted* from what it *inferred*. Inferred edges are plausible, not verified. When an answer rests on one, say so.
- If the graph has no path between two things, that means the graph found no connection — not that no connection exists. Say the former.
- Never present a figure, date, or quotation from graph output as sourced. Open the file and confirm it. This matters most for exactly the documents where it's tempting to skip: financial models, EU applications, anything going to a bank or ministry.
- If the graph is stale and there wasn't time to rebuild, say which and answer anyway — a flagged stale answer beats a delayed one.

## Reference files

- `references/document-corpora.md` — conventions for REGEA/Novera document projects: what to ignore, what to treat as a node, refresh cadence, and the Croatian-language pitfalls.
