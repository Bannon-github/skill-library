---
name: Distill transcript
description: >-
  Use this when turning a raw YouTube-provided how-to transcript into an
  agent-consumable skill: strip filler, keep procedures and facts, emit
  AgentConsumableSkill v1 JSON, and publish it to the youtube-skills MCP
  catalog. Reject thin/promo content; keep synth/DAW steps portable.
---
# Distill transcript

## When
After a how-to video’s **YouTube Show transcript** text is saved (never invent transcripts).

That is the **Transcript** panel opened from the video info / description area (⋯ → Show transcript / Transcript), **not** a caption-file download as the deliverable.

Fetch with:
```bash
python /workspace/skill-library/pipeline/fetch_youtube_transcript.py <video_id>
```
Writes `raw/<video_id>/transcript.txt` (panel-style) plus `raw/<video_id>/raw.txt` (prose for distill).

## Goal
Turn that YouTube-provided **transcript** into one or more **AgentConsumableSkill v1** documents agents can execute, then publish them for MCP discovery.

## Steps
1. Read `raw/<video_id>/raw.txt` (or `raw` / `transcript.txt`). Prefer prose `raw.txt` for distillation.
2. Drop filler: hesitation, greetings, outros, sponsorship, subscribe CTAs, empty hype, pure promo.
3. Keep tools/UI names, settings, ordered actions, and hard constraints; dedupe; keep chronological order when clear.
4. **Gate against the Quality rubric** (below). If the transcript cannot yield a passing skill, **reject** — write a short note under `distilled/<video_id>/REJECTED.md` instead of publishing thin JSON.
5. **Format** each executable skill as AgentConsumableSkill v1 (`/workspace/skill-library/schema/agent-skill.v1.json`):
   - `schema_version`: `"1.0"`
   - `id`, `name`, `goal`, `domain`
   - `source` (youtube video id/url/title; transcript = youtube-provided)
   - `prerequisites[]`
   - `inputs[{name, type, description, required}]`
   - `outputs[{name, type, description}]`
   - `constraints[]`
   - `steps[{n, action, tool?, expect?}]`
   - `verification[]`, `tags[]`, `curriculum_ids[]`, `mcp_resource` (`skill://<id>`)
6. **Novelty gate:** run `python /workspace/skill-library/pipeline/novelty_check_skill.py` on the candidate (see Novelty / prior-art). Reject or delta-only if overlap is high.
7. Optionally run `python /workspace/skill-library/pipeline/quality_check_skill.py` on the new JSON before publish.
8. Write `distilled/<video_id>/agent-skill-<id>.json` and copy to `mcp-publish/skills/<id>.json`; refresh `mcp-publish/index.json`.
9. Merge into `LIBRARY.json` / topics / curriculums as usual.

## Transcript source (mandatory)
- **Wanted:** YouTube **Show transcript** (info section → Transcript).
- **Not wanted as the product:** caption/subtitle file dumps (`.vtt` / `.srt`) — those may be used only as a fallback transport for the same timed transcript track, then converted to `transcript.txt`.
- **Do not** run our own ASR / Whisper unless Matt explicitly asks; stay on YouTube’s transcript.
- Provenance in skill `source.transcript` must be `youtube-provided` (Show transcript).

## Quality rubric (score 1–5; publish only if overall ≥ 3 and no hard reject)

| Criterion | Pass looks like | Fail looks like |
|-----------|-----------------|-----------------|
| **Goal** | Specific, executable outcome in ≥1 clear sentence (≥40 chars preferred) | Vague (“learn Blender”), promo tagline, or empty |
| **Steps** | Ordered, concrete, non-filler; ≥3 steps with non-empty `action`; each step is something an agent/human can do | Empty steps, advice-only fluff, “enjoy / subscribe”, duplicated noise |
| **Grounding** | Steps/settings clearly derived from the transcript (or honest “approximate from transcript description”) | Invented slider values, fake UI paths, fabricated recipes |
| **Scaffolding** | Useful `prerequisites`, `inputs`, `outputs`, `constraints`, non-empty `verification` | Missing fields, empty arrays where content is needed, placeholder text |
| **Portability** | Where claimed portable: maps product-specific UI to generic modules/params | Locked only to unreproducible proprietary clicks / preset bank names |
| **Tags / curriculum** | Sensible `tags[]` + `curriculum_ids[]` matching domain | Empty, mismatched domain, spam tags |

### Hard rejection criteria (do not publish)
- **Thin**: fewer than 3 substantive steps, or goal + steps together say almost nothing actionable.
- **Promo / CTA**: transcript is mostly sponsorship, unboxing hype, “buy my course”, channel trailer — no procedure.
- **Music-only / marker-only transcript**: timestamps or `[Music]` with no spoken procedure.
- **Invented content**: any step not grounded in the YouTube Show-transcript text (never fabricate speech or “fill in” missing how-to).
- **Broken schema**: missing `schema_version` `"1.0"`, empty `steps`, empty `action` strings, or missing required v1 fields.
- **Advice-only with no plan output**: pure opinion without even a usable ordered plan/checklist (prefer curriculum note over a fake “skill”).

### Soft quality bars (fix or mark constraints)
- Prefer ≥4 concrete steps when the transcript supports it.
- Every step should preferably include `expect` (observable outcome).
- `verification[]` ≥1 check that an agent can evaluate.
- Deduplicate near-identical `constraints` (one clear legal/portability block is enough).
- Keep `domain` consistent within a curriculum family (e.g. cinematic Traveler/Keysol skills → `cinematic-synth`).

## Novelty / prior-art (mandatory before publish)

Check that we are not recreating skills already covered by major public collections (Anthropic, skills.sh, VoltAgent awesome lists, Cursor rules, Hugging Face, OpenAI, community AgentSkills, MCP skill packs, etc.) or near-duplicates of our own `mcp-publish` catalog.

**Index:** `/workspace/skill-library/prior-art/` (`SOURCES.md`, `index.json`, `overlap-report.md`).

### Steps
1. Draft the candidate AgentConsumableSkill v1 (or at least `id` / `name` / `goal` / `tags`).
2. Run:
   ```bash
   python /workspace/skill-library/pipeline/novelty_check_skill.py path/to/candidate.json
   # or: --goal "..." --name "..." --tags a,b
   ```
3. Read verdict + top matches (prior-art **and** local mcp-publish).

### Decision rules
| Verdict / situation | Action |
|---------------------|--------|
| High overlap (`REJECT_OR_DELTA` or clearly same job as Anthropic/Cursor/community pack) | **Reject**, or distill **only the missing delta** — the `goal` **must** state that delta explicitly |
| Near-duplicate of our own published skill | Prefer **merge / curriculum link** over a new id; or publish only if steps add new constraints |
| Overlap with adjacent but different job (e.g. Blender Python addon rules vs viewport modeling how-to) | **Keep-as-more-specific**; mention distinction in `goal`/`constraints` |
| Low overlap | Proceed; still pass Quality rubric |

### Prefer specificity (our moat)
- **Stack-tied**: Web Audio / Polyrhythm control-tracks, Traveler/Keysol portable modules, Splatware/Volyraph, DJI capture settings.
- **Curriculum-tied**: ordered Blender beginner path pieces with hotkeys + verification — not "learn Blender".
- **Constraint-rich procedures**: observable `expect`/`verification`, portable param relationships.
- Avoid generic tutorials already covered by Anthropic document skills, obra/superpowers, Matt Pocock packs, marketing skill libraries, Binance crypto packs, etc.

### Soft integration
`quality_check_skill.py` warns when `prior-art/index.json` exists and name/goal heavily overlaps prior-art.

## Risk constraints — finance / investing / side-hustle topics
When distilling crypto, trading, investing, tax, or “make money” / side-hustle videos:
- **Not financial advice.** Put that in `constraints[]` and keep the skill procedural (how a tool/UI works), not predictive.
- **No guarantees**: never encode “you will profit”, guaranteed APY, or “risk-free”.
- **No scam amplification**: reject skills that teach phishing, fake airdrops, social-engineering wallets, pump groups, or bypassing KYC/AML.
- **No private-key / seed handling**: never instruct pasting seeds into websites or sharing keys; if the video does, reject or constrain to “use official wallet UI only; never share seed”.
- **Ground claims**: only record steps/settings present in the transcript; do not invent ticker strategies, leverage recipes, or tax positions.
- Prefer skills about **tool operation** (exchange UI navigation, DCA setup screens, spreadsheet tracking) over “how to get rich” narratives.
- Tag with `finance-risk` when publishing; keep curriculum ids explicit (e.g. `curriculum-crypto-tooling` not “wealth”).

## Portable abstraction rules — synth / DAW / plugin tutorials
Product walkthroughs (Traveler, Serum, Vital, Ableton, etc.) must distill **signal-flow recipes**, not rip kits:
1. **Map to portable modules**: oscillators, filters, envelopes, LFO/mod matrix, control/sequencer lanes, FX order (EQ → chorus → delay → reverb, etc.).
2. **Do not** copy proprietary factory preset names, bank dumps, wavetable file names, or sample packs into steps. Say “original/free WT” or “generic saw/pulse”.
3. **Do not** instruct ripping, dumping, or redistributing plugin content.
4. Prefer **parameters and relationships** (“Osc2 +7 semitones”, “velocity → cutoff near-exponential”, “dual control tracks length 15 vs 14”) over mouse-only click paths.
5. When UI labels are product-specific, add a portable alias in the same step (“KeySPACE-like = multi-algo cinematic reverb”).
6. State affiliation clearly once in `constraints[]`: original synthesis; not affiliated with the vendor; recreate in browser/Web Audio or any hybrid synth with comparable modules.
7. If the transcript is only a preset flex with no adjustable recipe → **reject** as thin/promo.

## Blender / creative-tool notes
- Prefer hotkeys + menu paths that remain valid across minor versions; note version when the transcript depends on it.
- UI-only clicks are OK when that *is* the skill (viewport nav), but still require verification.
- Split mega-tutorials into multiple focused skills rather than one giant thin summary.

## MCP publish
Skills live on the **youtube-skills** MCP server (`/workspace/skill-library/mcp-server/server.py`), tools: `list_skills`, `get_skill`, `search_skills`; resources `skill://{id}`.

Quality docs: `/workspace/skill-library/QUALITY.md`. Checker: `/workspace/skill-library/pipeline/quality_check_skill.py`.

## Do not
- Invent steps or transcripts
- Skip the novelty / prior-art check when `prior-art/index.json` exists
- Republish generics already covered by Anthropic/Cursor/community packs without a stated delta
- Learn from raw video pixels
- Skip the v1 schema fields
- Publish thin, promo, or finance-advice-as-guarantee skills
- Lock synth skills to unreproducible proprietary preset banks
