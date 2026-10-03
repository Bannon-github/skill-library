# Prior-art index (YouTube Distillery)

Durable catalog of **existing public / open agent skill collections** so distill runs do **not** recreate generics already covered by Anthropic, Cursor, skills.sh, community packs, MCP skill servers, etc.

## Purpose

1. Awareness before publishing a new distilled skill.
2. Force **novelty**: reject or distill-only-the-delta when overlap is high.
3. Push distill toward **more specific** skills (stack-tied, curriculum-tied, constraint-rich) in our moat domains: cinematic synth / portable signal-flow, Blender procedures, Gaussian splat pipelines, crypto **tooling** (not advice), side-hustle **procedures**.

## Layout

| Path | Role |
|------|------|
| `SOURCES.md` | Human catalog of collections (URL, license, size, re-fetch, relevance) |
| `index.json` | Machine-readable skill ids/names/goals/tags/urls for novelty checks |
| `overlap-report.md` | Compare our `mcp-publish/skills` against this index |
| `vendors/<slug>/` | Optional shallow clones when license + size allow |
| `raw/` | Saved README/API listings used to rebuild the index |

Our own **youtube-skills** MCP catalog is a **de-dupe peer**, not external prior-art to skip wholesale. Still check it so we do not publish near-clones of ourselves.

## How distill uses this

Before writing/publishing AgentConsumableSkill v1 JSON:

```bash
python /workspace/skill-library/pipeline/novelty_check_skill.py path/to/candidate.json
# or
python /workspace/skill-library/pipeline/novelty_check_skill.py --goal "..." --name "..." --tags a,b
```

| Verdict | Action |
|---------|--------|
| `NOVEL` | Proceed (still pass quality rubric) |
| `REVIEW` | Skim top matches; tighten specificity if needed |
| `WARN_NEAR_DUPLICATE` | Prefer stack/curriculum-tied delta; state delta in `goal` |
| `REJECT_OR_DELTA` | **Reject** publish, **or** distill only the missing delta (must state delta in `goal`) |

Also invoked as a soft warning from `quality_check_skill.py` when `index.json` exists.

Guidance lives in `/home/box/agent-data/workflows/distill-transcript/SKILL.md` → **Novelty / prior-art**.

## Rebuild

```bash
# refresh vendors (optional), then:
python /workspace/skill-library/pipeline/build_prior_art_index.py
```

See `SOURCES.md` for per-collection re-fetch notes. Prefer indexing from README/API listings for huge awesome-lists; only shallow-clone when MIT/Apache and reasonable size.

## Domains we care about

- `synth-cinematic` — pads, FM, WT morph, control tracks, portable DAW/Web Audio recipes
- `blender-3d` — viewport, modeling, geo, print setup, splat-adjacent capture
- `crypto-tooling` — exchange/wallet **UI procedures** only (not financial advice)
- `side-hustle` — tool/workflow procedures; avoid cloning marketing skill packs
- `general-agent` — only when YouTube adds a real delta vs Anthropic/Cursor/community

## Do not

- Claim affiliation with vendor skill packs
- Copy proprietary preset banks or closed course kits into skills
- Treat skills.sh installs / marketing packs as something to clone into youtube-skills
