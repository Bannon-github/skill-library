# Morning synth YouTube hunt: 2026-11-03

Mode: compact library (fold-in). No standalone skills were published. All 17 new skills passed `quality_check_skill.py` (clean) and `novelty_check_skill.py` (NOVEL). I hand-checked each against the target cluster's variants and folded it in with `pipeline/compact/fold_in.py`. LIBRARY.json has 17 new entries (229 → 236 entries, merge_log batch `2026-11-03-morning-hunt`), and `mcp-publish/index.json` was refreshed (33 skills). Old and new ids resolve through `mcp-publish/aliases.json`. All transcripts are YouTube-provided. No ASR was used.

## Recovered from the failed 2026-11-02 run
The 11-02 run searched, fetched and distilled 7 skills, then died before publishing. It also left 3 fetched transcripts that were never distilled and 2 fetches that had been rate-limited. All of that was finished today.

## Folded in (17)
| video | skill id (alias) | cluster | one-line goal |
|---|---|---|---|
| Z6IUhXyOvFc | three-bassline-roles-… | bass-design-sub-reese-808-and-layering | Low-cut other parts at 100-150 Hz, then audition three bass-line roles (matching, eighth pluck, sustained root). |
| MULPJOhSrZ0 | ambient-bass-mono-voice-… | bass-design-sub-reese-808-and-layering | Ambient bass: mono voice, one slow 4-bar master LFO on many timbre targets, direct-out sine sub, mono below 100-120 Hz. |
| 63FvtgN6Yrc | audible-sub-bass-on-phones-… | bass-design-sub-reese-808-and-layering | Make a sine sub audible on small speakers: clipping/overtones in 60-200 Hz, low-mid scoop, low-pass. |
| eDErfMlnh7c | parallel-octave-down-bass-from-stereo-mix | bass-design-sub-reese-808-and-layering | Thin ambient take: an octave-down copy LP'd at 100 Hz, the original HP'd at 100 Hz, the copy squashed and tucked under. |
| 3cSsQw4CggE | compress-expand-voice-leading-… | harmony-chords-voicing-and-slow-motion | Cinematic voice-leading: two-voice layers alternating 2nds and 3rds, common tones kept, layers a 4th/5th/8ve apart. |
| 9Re-L7z0068 | drone-role-pedal-point-and-polychords | harmony-chords-voicing-and-slow-motion | Use drones by role: pedal point, a fixed mid-range through-line, and drone stacks over a progression for polychords. |
| CwRN2ZVZweA | mix-by-arrangement-ambient-techno-… | arrangement-ambient-cinematic-score | Ambient techno mixed by arrangement: self-oscillating-filter kick and sub, pads rotating out, HP'd kick before the return. |
| Dscd9Q79fwQ | metric-modulation-action-cue | arrangement-ambient-cinematic-score | Action-cue tension: metric modulation (100 → 150 → 133 BPM), 3/4 → 6/8 → 5/8, ostinatos, orchestration by role. |
| PE3c8J6glho | ambient-loop-to-track-arp-rate-energy | arrangement-loop-to-song-build-drop | Loop to full track using single-chord clips, arp rate whole → 1/8 as the energy dial, a double-time drum clip and pluck bass at the peak. |
| QdveXtMhAnk | flanger-sequence-pad-… | pad-phaser-notch-comb-movement | Flanger with its rate at 0 and delay time stepped by a square LFO for an arpeggio-like comb pad, then a resampled transition. |
| 1s_wcjB31iA | build-stereo-phaser-from-allpass-chain-… | pad-phaser-notch-comb-movement | Build a stereo phaser from 1-7 all-pass biquads: Q 0.7071, exponential LFO sweep, R-channel phase offset. |
| ZsbcQZtklGI | phaser-chorus-pure-wave-octave-pad | pad-phaser-notch-comb-movement | Triangle+sine octave-stacked pad whose only motion comes from phaser and feedback chorus; notch the phaser whistle; dark reverb. |
| bAovHufTsc8 | staggered-attack-octave-layer-pad | pad-supersaw-unison-detune-width | Pad with per-layer amp envelopes so the octave-up layer blooms late in each chord, plus a foley noise layer (pitch-bend LFO dropped). |
| 3rCUdTDodrc | whoosh-into-hit-layer-resample-chain | risers-impacts-transition-fx | Whoosh-into-hit impact: whoosh quieter than the hit, no sub in the whoosh, resample milestones, clip, then multiband and true-peak limiting. |
| Pp88aLB3LpE | organic-tension-from-track-sounds | risers-impacts-transition-fx | Build tension from the track's own sounds: a one-osc pitch ramp, an irregular vocal loop pitched up, a fully fed delay revealed by its return fader. |
| Fj7E0DXML1o | velocity-and-flam-groove-on-step-sequencer | drum-groove-programming-swing-and-ghosts | Four-on-the-floor feel: velocity-shaped hats, 56% swing, stacked loose clap, 24-step bar with 8-bar reset, bus pump. |
| GomiGC__HC0 | dynamics-restoring-saturation | mix-eq-gain-staging-and-balance | Saturate drums without losing punch: an envelope follower on the dry signal drives gain after the saturator. |

## Rejected (3)
- **63nKuxQCdJc** (Aphex exciter tutorial): promo/thin plugin demo. The exciter-vs-EQ concept is already covered.
- **MNSoaIHyIfY** (Film-score tension with synths): walkthrough with no reusable recipe, and the bass drifts microtonally (against the steady-pitch rule). The arc is already covered.
- **NRWqPRrxY44** (Theta binaural beats in Ableton): already covered by the brainwave cluster, and mostly wellness claims. Delta noted in REJECTED.md: set the beat offset in Hz, not cents.

Earlier 11-02 rejects (2kLF7w-EaCg, Y3eB64YwCow, gK_jgUtBOos, 7iHAf88Mfn0, Qjx4xRXErXk, p1-WmITJqBk, LMInvlw-iAE, m788n74Ldd4, hfjLuqOK9Co, vYRIXi4A6CU) still stand.

## Router note
`route.py` returned CANDIDATES_READY for all 8 videos fetched today. On 11-02 it said COVERED for 5 videos that hand-checking showed were novel. Keep hand-checking.

## Other changes
- `mcp-server/server.py` `search_skills` now also searches variant names and goals. Without this, folded content could not be found by search (e.g. "metric modulation" or "loose clap" returned 0 hits). Verified: list = 33, search hits the new terms, and `get_skill` resolves the old alias ids.

## Searches (2026-11-03)
These queries were run: "how to make synth pads brighter and airy", "saturation exciter add air to pads tutorial", "evolving ambient loop synth tutorial", "cinematic build up tension arrangement tutorial" and "ambient drum programming tutorial". Fetching: 1 rate-limit at the start of the run, then 9 of 9 fetches succeeded at 30 s spacing.

## Gaps still open
- **Brightness/air on pads:** still no dedicated source. Queries like "high shelf vs exciter" and "bit crush before reverb" return plugin promos or off-topic videos. The brightness-and-air-at-the-source cluster has 0 video variants. Try channel-targeted searches next (e.g. sound-design channels plus "airy pad", "pad presence 8k").
- **Punchy bass:** better (4 bass variants plus dynamics-restoring saturation), but there is still no ambient/cinematic kick+bass punch workflow.
- **Wavetable, hybrid, FX, modulation, stereo width:** not searched today, to stay within the token budget.

## Carry-overs
- Unfetched candidates worth trying: TosV3erGfsg (Ambient pads and atmospheres), p5ETZc7Zfw4 (lush evolving pads in Wavetable), y1YmvAO_5ko and uTKYIv4xnYE (tension cue for TV/film, parts 1-2), q7OQdzGZwNA, xeuYUFZpOdA (atmospheric liquid DnB drums), L0mST_BaaBA (drums for any genre), 5A8mI4l-erg and HJZG-qD4oso (ambient loop).
- Brainwave: vYRIXi4A6CU (thin transcript) and hfjLuqOK9Co (off-lexicon) were rejected 11-02. Low priority; nothing new.
- MH7YiOWQIhI / kHWOIE4YTZ4: tlang upgrade still optional and not done.
