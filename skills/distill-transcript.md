# distill-transcript

**Goal:** Turn a raw YouTube-provided transcript into actionable procedure lines an agent can execute.

**When to use:** After a how-to video's caption file is saved as `raw` under `raw/<video_id>/`.

## Steps
1. Read `raw/<video_id>/raw.txt` (or `raw`).
2. Remove filler: hesitation words, greetings, sponsorships, subscribe CTAs, empty hype.
3. Keep only actionable steps, tool/UI names, numeric settings, and necessary constraints.
4. Deduplicate; preserve chronological order when clear.
5. Write `distilled/<video_id>/distilled.json` and `distilled.md`.
6. Derive or update executable `skills/*.md` entries and append to the library/curriculum.
