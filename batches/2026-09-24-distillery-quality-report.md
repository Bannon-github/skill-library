# Distillery quality report — 2026-09-24

Generated: 2026-09-24 ~05:25 PT (America/Vancouver).  
Scope: quality + pipeline improvements only (no competing synth batch fetches).  
Root: `/workspace/skill-library`

## Summary
- Sampled **10** published skills across cinematic-synth (keysol/traveler), blender, photo, coding, spatial-capture.
- Rubric: goal · steps · grounding · scaffolding · portability · tags/curriculum (1–5 each; overall = mean rounded).
- Structural scan of all **37** `mcp-publish/skills/*.json`: **0** hard fails (no empty steps, no missing `schema_version`).
- Soft issues common: missing per-step `expect` (blender/older skills), short goals (4), duplicated synth legal boilerplate (13).
- Changes shipped: distill `SKILL.md` rubric + rejects + finance/synth rules; `pipeline/quality_check_skill.py`; `QUALITY.md`.

## Sample scores

| Skill | Domain | Goal | Steps | Ground | Scaffold | Portable | Tags | **Overall** | Top defects |
|-------|--------|------|-------|--------|----------|----------|------|-------------|-------------|
| `keysol-venus-fifths-pulsar-wt-impact` | cinematic-synth | 5 | 4 | 4 | 5 | 5 | 5 | **5** | Only 4 steps; constraints duplicated ×5 |
| `keysol-helpling-keytrack-bass-split-delay` | cinematic-synth | 5 | 4 | 4 | 5 | 5 | 5 | **5** | Thin step count (3); same constraint boilerplate |
| `keysol-venus-velocity-hybrid-bass-impact` | cinematic-synth | 5 | 4 | 4 | 5 | 5 | 5 | **5** | Dual-mode skill could split; boilerplate |
| `traveler-walkthrough-wavetable-morph-filter-motion` | cinematic-synth | 5 | 5 | 4 | 5 | 5 | 5 | **5** | Strong portable mapping; boilerplate |
| `traveler-walkthrough-super-unison-wide-lead` | cinematic-synth | 5 | 5 | 4 | 5 | 5 | 5 | **5** | “Osc2-style” still slightly product-tied (acceptable) |
| `traveler-walkthrough-fx-eq-chorus-delay-reverb` | music-synthesis* | 5 | 5 | 4 | 5 | 5 | 4 | **5** | *Domain inconsistency (`music-synthesis` vs siblings `cinematic-synth`); tags still cinematic |
| `blender-boolean-bracket-with-cylinder-holes` | 3d-blender | 5 | 5 | 5 | 5 | 4 | 5 | **5** | No per-step `expect`; UI-path heavy (OK for Blender) |
| `blender-easy-car-box-model-core-tools` | 3d-blender | 5 | 5 | 5 | 4 | 4 | 5 | **5** | No `expect`; inputs oddly require default cube |
| `blender-donut-tutorial-nav-add-shade-smooth` | 3d-blender | 4 | 4 | 4 | 3 | 4 | 4 | **4** | Empty `inputs[]`; null tools/expects; mixes install+nav |
| `blender-gamedev-learning-path-advice` | 3d-blender | 3 | 3 | 4 | 3 | 3 | 4 | **3** | Advice/plan — weakly executable; borderline skill vs curriculum note |
| `blender-chatgpt-python-script-gold-ball` | 3d-blender | 4 | 4 | 4 | 4 | 3 | 4 | **4** | Locked to ChatGPT web UI; dated “GPT-3.5” constraint |
| `python-pathlib-basic-file-workflow` | coding-filesystem | 2 | 3 | 3 | 4 | 5 | 3 | **3** | Goal too short; steps are API cheat-sheet, light verification/tags |
| `lightroom-select-and-develop-photo` | photo-editing | 2 | 3 | 3 | 4 | 3 | 3 | **3** | Vague goal; no concrete slider/panel detail from transcript |
| `drone-hyperlapse-multi-angle-capture` | spatial-3d-capture | 2 | 2 | 3 | 3 | 2 | 3 | **3** | Thin (3 generic steps); DJI-mode specifics missing |

*Counted ≥8 primary samples; extras included for contrast (thin / advice / FX domain drift).*

### Aggregate takeaways
1. **Cinematic synth batch is the quality high-water mark** — specific goals, portable signal-flow, verification, curriculum ids. Main defect: **copy-pasted constraint quintet**.
2. **Blender how-tos are solid procedures** but almost never set `expect` on steps; some early skills omit useful inputs.
3. **Older thin skills** (`drone-hyperlapse-*`, `lightroom-*`, `python-pathlib-*`) meet schema but fail the new publish bar on goal specificity / step concreteness.
4. **Advice skills** (`blender-gamedev-learning-path-advice`) should either emit a real plan artifact or live as curriculum text, not pretend to be a modeling procedure.
5. **Domain hygiene**: `traveler-walkthrough-fx-eq-chorus-delay-reverb` should be `cinematic-synth` like its siblings (not fixed this pass — not a hard schema break).

## Defect themes → fixes applied

| Defect | Mitigation |
|--------|------------|
| No shared publish bar | Rubric + hard rejects in distill `SKILL.md` |
| Thin / promo risk for future finance/crypto batch | Finance risk constraints section in `SKILL.md` |
| Synth skills locked to product UI / preset rips | Portable abstraction rules in `SKILL.md` |
| No automated gate | `pipeline/quality_check_skill.py` |
| Rubric not discoverable in library | `QUALITY.md` + pointer from distill skill |
| Empty steps / missing schema | Scanner found **none**; no JSON surgery; index untouched |

## Changes made

### 1. `/home/box/agent-data/workflows/distill-transcript/SKILL.md`
- Quality rubric (6 criteria) with pass/fail examples
- Hard rejection: thin, promo, music-marker captions, invented content, broken schema, advice-only without plan
- Soft bars: prefer `expect`, verification, dedupe constraints, domain consistency
- **Finance / investing / side-hustle** risk constraints (not advice, no guarantees, no seed phishing, tool-operation focus, `finance-risk` tag)
- **Synth/DAW portable abstraction** rules (modules not banks; one affiliation constraint; reject preset-flex)
- Blender notes; pointer to `QUALITY.md` + checker; optional pre-publish check step

### 2. `/workspace/skill-library/pipeline/quality_check_skill.py`
Validates AgentConsumableSkill v1:
- Required fields, `schema_version == "1.0"`
- Non-empty steps/actions; min 3 steps (warn)
- Goal length ≥40 (warn; `--strict` → fail)
- Verification present & non-empty (warn/strict)
- Empty-action ban (fail)
- Promo/hype phrase heuristics; cinematic constraint-boilerplate warn
- Default scan: `mcp-publish/skills/`; exit 1 on failures

```bash
python3 /workspace/skill-library/pipeline/quality_check_skill.py
python3 /workspace/skill-library/pipeline/quality_check_skill.py --strict path.json
```

**Latest run:** 37 checked → 0 failed, 37 warned (mostly missing `expect` / boilerplate / short goals).

### 3. `/workspace/skill-library/QUALITY.md`
Short human checklist mirroring the rubric and publish gates.

### 4. Published JSON / index
- **No hard-broken skills** (empty steps / missing `schema_version`) → no skill JSON edits, **index.json not refreshed**.
- Recommended follow-ups (not done here to avoid clobbering sibling batch work):
  - Collapse synth constraint boilerplate to 1–2 lines
  - Align FX skill `domain` → `cinematic-synth`
  - Backfill `expect` on blender skills
  - Rewrite or quarantine thin skills below overall 3 under a `needs-redistill` tag

## Coordination
- Did not delete or modify in-progress `raw/` from the sibling synth executor.
- Did not push git or message the user.
- Did not use `update_state` (workflow file edit only).

## Success criteria check
- [x] Rubric applied to ≥8 skills with scores (10+ listed)
- [x] Distill `SKILL.md` improved with actionable rules
- [x] Automated quality helper (`quality_check_skill.py`) + documented checklist (`QUALITY.md`)
- [x] Report at this path for parent relay
