# Morning synth YouTube hunt: 2026-11-06

Mode: compact library (fold-in). No standalone skills were published. All 3 new skills passed `quality_check_skill.py` (clean) and `novelty_check_skill.py` (NOVEL, scores 0.89–0.93). I hand-checked each against the target cluster's variants and folded it in with `pipeline/compact/fold_in.py`. LIBRARY.json has 3 new entries (245 → 248 entries, merge_log batch `2026-11-06-morning-hunt`), and `mcp-publish/index.json` was refreshed (33 skills). New ids resolve through `mcp-publish/aliases.json`. All transcripts are YouTube-provided (manual or YouTube auto via Show transcript / yt-dlp). No local Whisper/ASR was used.

## Folded in (3)
| video | skill id (alias) | cluster | one-line goal |
|---|---|---|---|
| 4Dub1HigXtU | generative-midi-chord-arp-random-scale-quantize-pad | generative-ambient-drones-and-soundscapes | Generative ambient pad from MIDI FX chain chord→arp→random→scale-quantize LAST, uneven loop lengths, send-return FX as blendable layers, slow LFOs on send/filter/gain. |
| LF4yNpzSARQ | cinematic-seven-section-arc-ostinato-countermelody-bookend | arrangement-ambient-cinematic-score | Cinematic 7-section arc: open piano → sustained strings → chord-tone ostinato → motif melody → countermelody climax with doubles → bookend return to opening. |
| HPDGp6b829s | field-recording-hpf-exciter-air-layer | brightness-and-air-at-the-source | Ambient air layer from field recording: HPF out traffic lows, subtle harmonic exciter for upper sparkle, light high lift (avoid glassy mess). |

## Rejected (23)
- **JP5yTtT-gbk**: ambient Ableton Wavetable pad — false-novel vs wavetable cluster / lush-dual-saw fold; dual-filter mention not a portable delta.
- **Lo9njrFnkTM**: still NO_TRANSCRIPT after retry; ASR flagged, not used.
- **vRa_Zk90lDc**: generic EQ-in-10-minutes — not exciter/air pad.
- **DyHpBtS9Iso**: vocal EQ — wrong target for brightness/air.
- **VBBsuvFGpHc**: NO_TRANSCRIPT (air search).
- **u7-40sDPxQI**: NO_TRANSCRIPT (soft-kick search).
- **I_4d4U3Ti9k**: EDM “perfect kick” sample-pack/promo; not soft cinematic kick+sub.
- **K9JZ1WijGmI**: live ambient film-score / template promo; thin vs arrangement cluster + today’s LF4 fold.
- **Nck9SX52qpU**: Gnaural binaural GUI tour — not DAW isochronic production.
- **Vb4didZ1lho**: 432 Hz conversion sacred-tuning fluff.
- **hdcX5B-xSek**: “make 432 Hz music” detune fluff.
- **HpSC2SFb9E4**: Wurlitzer/Rhodes in Vital + preset pack promo.
- **QDdaYRzPN9E**: HALion 7 wavetable feature tour.
- **eu0zpa7OiYA**: synthesis-for-beginners survey.
- **auztdZ8ysLU**: Massive moody-pad walkthrough; pad/WT covered.
- **AnOJ-uQgwP8**: Butter Synth wavetable editor product tour.
- **4MeP3XbYMGA**: wavetable programming 101; covered by many WT morph variants.
- **3nhk0CD_NKg**: sponsored mixer beginner guide (air-query miss).
- **AMtPQKrP2_U** / **N86NQ8vYQSk**: wall/room soundproofing DIY (air-query miss).
- **rk7k6bJTgVo**: Vital punchy EDM kick — near-dupe of synth-drum-kit 808 recipe; not soft cinematic kick+sub.
- **u4DPfvDX7Sg**: Serum 2 lush pad (soft-kick search miss).
- **Kf2KklP9mSY**: Diva melodic-house bass + preset-pack promo.

## Router note
`route.py` returned CANDIDATES_READY / NOVEL for most transcripts. Several were false-novel on hand-check (JP5, EQ/vocal hits, 432 Hz, product tours, soundproofing). Keep hand-checking both directions. Soft-kick and isochronic queries keep missing the intended gap.

## Searches (2026-11-06)
Carry-overs first: `4Dub1HigXtU`, `JP5yTtT-gbk`, `Lo9njrFnkTM`. Queries run: "exciter air pad sound design high frequency", "ambient soft kick sub bass cinematic tutorial", "ambient cinematic song structure arrangement builds breakdowns", "isochronic tones music production tutorial DAW", "hybrid synthesis sound design wavetable FM tutorial", "wavetable morph pad modulation FX tutorial", "air layering noise high shelf pad sound design exciter", "soft cinematic kick drum synthesis sub bass ambient".

## Gaps still open
- **Brightness/air (synth-source):** field-recording HPF+exciter fills a *parallel air layer* recipe; still thin on **synth-native** exciter / noise-air / high-shelf air-pad design beyond start-bright-then-filter. Try a known air-layering synth video id next.
- **Ambient/cinematic soft-kick + sub:** still open. Soft-kick searches hit EDM kick packs / Vital punchy kicks / unrelated pads.
- **Brainwave/isochronic production:** still open — hits remain Gnaural GUI / 432 Hz sacred fluff; need a DAW gated-carrier / isochronic-under-music workflow beyond the existing 3 variants.
- **Hybrid synthesis:** searches skewed to Rhodes/Vital presets and HALion tours; no strong portable hybrid fold.
- **Wavetable/FX/modulation:** routine coverage already dense; today’s WT hits were 101 / product tours.

## Carry-overs
- None critical from today’s deferred set (4Dub folded; JP5/Lo9 closed as reject).
- Prefer hunting known video ids for: synth-native air/exciter pad, soft cinematic kick+sub, DAW isochronic production (not 432/solfeggio).
