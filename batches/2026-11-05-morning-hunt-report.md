# Morning synth YouTube hunt: 2026-11-05

Mode: compact library (fold-in). No standalone skills were published. All 5 new skills passed `quality_check_skill.py` (clean) and `novelty_check_skill.py` (NOVEL, scores 0.89–0.93). I hand-checked each against the target cluster's variants and folded it in with `pipeline/compact/fold_in.py`. LIBRARY.json has 5 new entries (240 → 245 entries, merge_log batch `2026-11-05-morning-hunt`), and `mcp-publish/index.json` was refreshed (33 skills). New ids resolve through `mcp-publish/aliases.json`. All transcripts are YouTube-provided (manual or YouTube auto via Show transcript / yt-dlp). No local Whisper/ASR was used.

## Folded in (5)
| video | skill id (alias) | cluster | one-line goal |
|---|---|---|---|
| 5oW5Mb-3sF0 | wide-bass-remove-fundamental-add-mono-sine | bass-design-sub-reese-808-and-layering | Strip the fundamental from a unison wavetable, keep wide overtones, restore power with a separate mono sine (phase-rand 0) so wide Reese stays mono-compatible. |
| zscsukQNOLU | width-by-juxtaposition-ms-sides-reverb | stereo-width-haas-midside-mono-safe | Perceived width from narrow↔wide juxtaposition, real double-tracks (not clones), and M/S sides-only EQ (~−30 dB mid) + dry-center / wet-sides reverb for mono-safe stereo beds. |
| p5ETZc7Zfw4 | lush-dual-saw-filter-env-nonretrigger-lfo-pad | wavetable-and-vector-morph-pads | Dual-octave saws, high shimmer-style unison, overlapping amp ADSR, filter env from ~200 Hz, and a slow non-retriggering multi-bar triangle LFO on cutoff so each chord catches a different filter place (pitch-drift LFO dropped). |
| M7fEMi8VSy4 | nested-lfo-layered-riser-downer-kit | risers-impacts-transition-fx | Envelope LFO (~2 bars) drives pitch and nested LFO2 rate for accelerating grit/stutter; layer downer + high stutter + main riser + atmosphere; HPF automation between subgroups. |
| MsT_yjp5kpI | cloakroom-check-lpf-shelf-low-end-balance | mix-eq-gain-staging-and-balance | Master low-pass “cloak-room check” to audition club-wall lows; diagnose kick-only vs mush vs clear priorities; balance bass low/mid shelves against the kick while the check stays on. |

## Rejected (11)
- **A52l7uG3Sq4**: thin Logic tips (good samples, turn it up, key EQ chart, binaural pan) + Splice promo. Router false-novel.
- **ZKR8ODDIWqE**: promo-heavy kick masterclass; core ideas already in mix/sidechain/bass/kick-bass-four-level-lock. Deltas noted (reverse-transient pre-hit, low-shelf vs HPF for sub bleed, multiband sidechain lows) but not published; skipped commercial-kick-extraction tip.
- **CT8vQewKnFE**: modulation-matrix 101 — near-dupe of modulation cluster basics.
- **f_XQfAONZw8**: ambient clip-to-structure session (series part 1); thin vs arrangement-ambient variants.
- **uEGE-B53UPs**: Alloy metallic synth promo/demo.
- **ySjZQ697Mt0**: synthesis-type survey / gear tour; deltas noted (WT position motion, granular on transient-rich samples) but no tight single recipe.
- **JP5yTtT-gbk**: ambient Wavetable pad — overlaps today's lush-dual-saw fold + wavetable cluster; skipped to stay lean.
- **I47BM2qaL2w**: beginner WT pad/chords fundamentals; covered.
- **bN7dgR9a7BI**: sacred/solfeggio overview; brainwave cluster already has portable binaural/isochronic recipes.
- **4Dub1HigXtU**: generative MIDI pad chain (chord→arp→random→scale-quantize last) — real generative-ambient delta but plugin-tour heavy; deferred as carry-over.
- **Lo9njrFnkTM**: NO_TRANSCRIPT.

## Router note
`route.py` returned CANDIDATES_READY / NOVEL for all routed videos that had transcripts. Several were false-novel on hand-check (A52, CT8, JP5, I47, bN7, ySj). Keep hand-checking in both directions.

## Searches (2026-11-05)
Queries run: "wavetable synth pad tutorial sound design", "hybrid synthesis sound design tutorial", "synth modulation matrix LFO tutorial", "cinematic FX sound design riser impact tutorial", "exciter air pad sound design tutorial", "ambient soft kick sub bass tutorial cinematic", "ambient cinematic song structure arrangement tutorial", "isochronic tones music production tutorial". Carry-over ids were fetched first (all 6 got transcripts; some after rate-limit retries). Search leads fetched: JP5yTtT-gbk, I47BM2qaL2w, CT8vQewKnFE, M7fEMi8VSy4, f_XQfAONZw8, Lo9njrFnkTM (fail), bN7dgR9a7BI, MsT_yjp5kpI, ySjZQ697Mt0, uEGE-B53UPs.

## Gaps still open
- **Brightness/air:** still thin beyond filter-from-bright (+ today's WT pad is filter-LFO evolving, not exciter/shelf/noise-air). Exciter search mostly missed; try a tighter query or a known air-layering video.
- **Ambient/cinematic soft-kick + sub:** not filled; soft-kick search was weak. Cloak-room check helps low-end listening but is not a soft-kick design recipe.
- **Song structure/arrangement for ambient/cinematic:** f_XQfAONZw8 was too thin; deepen arrangement clusters only with a stronger how-to.
- **Brainwave/isochronic production:** searched; hits were sacred/solfeggio fluff — gap remains for a production-focused isochronic/brainwave workflow beyond the existing 3 variants.
- **Hybrid synthesis:** search skewed to trap/Rhodes demos; no strong portable hybrid fold this run.
- **Generative ambient pads (4Dub1HigXtU):** deferred — strong candidate for generative-ambient-drones next run.

## Carry-overs
- **4Dub1HigXtU** — generative MIDI ambient pads (transcript ready; distill next).
- **JP5yTtT-gbk** — optional dual-filter Ableton Wavetable routing delta only if hand-check shows novelty beyond today's WT fold.
- **Lo9njrFnkTM** — ambient arrangement part 10; retry if a transcript appears.
- Exciter/air and ambient soft-kick+sub remain open search targets.
