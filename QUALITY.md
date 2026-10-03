# Skill quality rubric (AgentConsumableSkill v1)

Companion to `/home/box/agent-data/workflows/distill-transcript/SKILL.md`.
Automated checks: `python /workspace/skill-library/pipeline/quality_check_skill.py`.

## Score each skill 1–5

| # | Criterion | 5 | 1 |
|---|-----------|---|---|
| 1 | Goal specific & executable | Clear outcome an agent can finish | Vague / promo |
| 2 | Steps ordered, concrete, non-filler | ≥3 doable actions, chronological | Empty / fluff |
| 3 | Grounded in transcript | Settings/actions from YouTube captions | Invented content |
| 4 | Scaffolding useful | prereqs, inputs, outputs, constraints, verification | Missing / empty |
| 5 | Portable where claimed | Generic modules/params, not unreproducible clicks only | Locked to proprietary UI/presets |
| 6 | Tags + curriculum_ids sensible | Match domain & learning path | Empty / mismatched |

**Publish bar:** overall ≥ 3 and no hard reject.

## Hard rejects
- Thin (<3 substantive steps)
- Promo / CTA / music-marker-only captions
- Invented transcript or steps
- Broken schema (`schema_version` ≠ `1.0`, empty steps/actions)
- Finance “guaranteed profit” / seed-phishing / scam flows

## Finance topics
Procedural tool-use only; add “not financial advice”; never guarantee returns; never handle seed phrases via web forms.

## Synth / DAW portability
Map to oscillators, filters, envelopes, mod matrix, FX order. No preset-bank rips. One clear affiliation/original-synthesis constraint is enough (avoid duplicated boilerplate).

## Checklist before MCP publish
- [ ] `schema_version` = `"1.0"`
- [ ] Non-empty `goal` (≥40 chars preferred)
- [ ] ≥3 steps with non-empty `action` (prefer `expect` too)
- [ ] Non-empty `verification[]`
- [ ] `prerequisites`, `inputs`, `outputs`, `constraints` present and useful
- [ ] `tags` + `curriculum_ids` set; `domain` consistent with siblings
- [ ] `source.transcript` = `youtube-provided`
- [ ] Ran `quality_check_skill.py` on the file
