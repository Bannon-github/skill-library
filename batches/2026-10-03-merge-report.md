# 2026-10-03 — Library merge pass

**Before:** 84 published skills · **After:** 73 published skills (10 merged skills replace 21 originals; 0 content dropped)

Backup of the full pre-merge library: `backups/pre-merge-20261003-084519/`

## How publishing works (checked before changes)
- The `youtube-skills` MCP server (`mcp-server/server.py`) reads `mcp-publish/skills/*.json` live; `mcp-publish/index.json` is the manifest. There is no separate publish script. "mcp-publish" means: write `distilled/.../agent-skill-<id>.json`, copy it to `mcp-publish/skills/<id>.json`, and refresh `index.json`.
- The server venv (`mcp-server/.venv`) was **missing**, which is likely why the `user-youtube-skills` connector shows `error`. I recreated it (mcp 2.3.0).

## Merge rules applied
Each merged skill keeps the union of all steps, constraints, inputs, outputs, and checks from its inputs, with exact duplicates removed. No new facts or settings were added: only routing/"choose a method" steps and cross-references to related skills. The merged skill keeps every source video in `sources[]`, plus `merged_from[]` and `aliases[]`. Retired docs were moved to `mcp-publish/retired/` (their old distilled files stay in `distilled/<video_id>/`). Old ids still resolve through `mcp-publish/aliases.json`: `get_skill`, `skill://`, and `search_skills` all map them to the new id.

## Merges (old → new)
1. `reverb-types-hall-chamber-room-plate-spring` + `reverb-send-wet100-eq-room-plate-spring` → **`reverb-pads-type-choice-and-send-setup`**: picking a reverb type and setting up the send returns are one job, and both covered the same room/plate/spring set.
2. `ping-pong-delay-filtered-motion-recipe` + `dual-delay-parallel-two-tap-crossfeedback` → **`stereo-delay-pingpong-dual-parallel-two-tap`**: the dual-delay skill described itself as a "delta vs ping-pong", so ping-pong is now one mode of a single stereo-delay skill.
3. `odd-even-unison-center-vs-width` + `supersaw-clean-unison-detune-width` → **`unison-odd-even-detune-width-clean-supersaw`**: both are about voice count, detune/blend, and width/mono-compatibility; the odd/even rule now feeds directly into the supersaw voice count.
4. `lfo-envelope-motion-routing-basics` + `mod-matrix-source-destination-routing-basics` → **`modulation-lfo-envelope-mod-matrix-routing`**: the mod-matrix skill said it was a delta on the LFO/envelope basics, so the two now form one modulation-routing path.
5. `highband-pan-lfo-pad-width-keep-lows` + `mono-compatible-chord-split-stereo-pad` → **`pad-width-no-phase-smear-highband-pan-or-chord-split`**: same goal (widen a pad without chorus/imager phase smear), so it's now one skill with two methods (A/B).
6. `sidehustle-productize-service-fixed-scope-price` + `sidehustle-productize-sustainable-ops-constraints` → **`sidehustle-productized-service-offer-and-ops`**: the second skill's input was the first one's output (draft offer → hardened offer).
7. `blender-install-preferences-and-viewport-basics` + `blender-beginner-three-tools-and-viewport-nav` + `blender-viewport-navigation-mmb` → **`blender-install-prefs-viewport-nav-transform-tools`**: three overlapping first-launch, navigation, and Move/Rotate/Scale skills.
8. `blender-donut-tutorial-nav-add-shade-smooth` + `blender-complete-beginner-add-delete-focus` → **`blender-first-scene-add-delete-focus-shade-smooth`**: both are "delete cube, add primitives" first-scene basics (keeps the donut/mug path note).
9. `drone-hyperlapse-multi-angle-capture` + `upload-capture-to-free-splatware` → **`drone-hyperlapse-to-splatware-splat`**: same video, sequential, and each was only 3 thin steps; together they make one end-to-end skill.
10. `dji-video-capture-for-gaussian-splat` + `process-drone-video-to-gaussian-splat-mipmap` → **`dji-video-to-gaussian-splat-mipmap`**: same video and tightly coupled (the processing step depends on the GPS subtitles enabled during capture).

## Checks
- `quality_check_skill.py --strict` on the 10 merged skills: 10 clean.
- Full catalog: 73 checked, 0 failed, 28 warned. The warnings are older, untouched skills missing `expect` fields.
- JSON Schema (`agent-skill.v1.json`): 73/73 valid.
- `novelty_check_skill.py`: the only near-duplicate hits were each merged skill's own source skills (now retired). No external prior-art conflicts.
- Verified through a real MCP stdio client against `server.py`: `list_skills` → 73, no retired ids listed; `get_skill("ping-pong-delay-filtered-motion-recipe")` → merged delay skill; `skill://reverb-types-…` → merged reverb skill; `search_skills("odd-even-unison")` → merged unison skill.

## Also updated
- Curricula: `curriculum-cinematic-hybrid-synth` (supersaw → unison merge), `curriculum-crypto-sidehustle` (productize pair), `curriculum-blender-beginner` (level 1 now has the two merged skills), `curriculum-drone-to-splat` (restructured into 2 levels: free-web-tool pipelines, then DJI GPS capture → Mip-Map), and `curriculums/index.json`.
- `LIBRARY.json` (`skill_aliases`, `merge_log`, per-entry `merged_into`), `topics/taxonomy.json`, and `skills/*.md` (new .md files written; retired ones moved to `skills/_retired/`).
- `mcp-server/server.py`: alias resolution for `get_skill` and `skill://`, and old ids are now searchable.

## Clusters deliberately left unmerged
- **Shimmer reverb**: a pitch-shift/feedback send chain, which is a different build from choosing a reverb type or setting up sends.
- **Sidechain duck vs trance-gate**: one uses a compressor to duck pads under the kick; the other uses a gate keyed by a silent trigger to chop a pad. Different processors and goals.
- **Mid/side EQ and mix-pads-role**: EQ and mix-role procedures, not width tricks; kept apart from the merged pad-width skill.
- **Filter flavors / parallel filters / Traveler stereo ladder / velocity→filter**: each covers a different job (choosing a filter design, rhythmic parallel chains, stereo cutoff offset, velocity expression).
- **Traveler walkthrough (6) and Keysol Venus (6) series**: these follow the distill rule to split mega-tutorials into focused per-module or per-patch skills. Each is a distinct patch or module.
- **Pad recipes** (warm-heavenly supersaw pad, evolving fifth pad, granular dual-saw, lush stereo saw, warm analog drift, organic looped sample, digital WT bandpass, ambient pluck, formant/comb): each is a different patch from a different video.
- **Wavetable family** (crossfade morph, spectral warp, scratch-built ambient WT, Traveler WT motion) and **chorus / tape saturation / AM / FM / osc-as-granular-delay**: different techniques.
- **Crypto hardware wallet unbox/verify vs seed backup (standard/Shamir/metal)**: back-to-back steps, but they serve different jobs (supply-chain check and init vs backup scheme and storage). A user with an existing wallet only needs the backup skill.
- **Gumroad listing vs Stripe invoice vs Upwork proposal**: different tools and tasks.
- **Blender setup-nav-and-geometry-practice, edit-mode hotkeys, metric-mm vs boolean bracket, mug, cookie, etc.**: distinct content (learning map/practice, mesh-edit ops, reusable unit setup).
- **Polyrhythm Studio**: not touched.

## Open items
- The `user-youtube-skills` connector still reports `error` in tool discovery. The server itself runs fine locally with the rebuilt venv; the connector probably needs a reconnect or restart on the platform side.
- The merged reverb, delay, modulation, and pad-width skills (and their sources) were never in the cinematic curriculum's levels. I didn't add them; they only carry `curriculum_ids`.
