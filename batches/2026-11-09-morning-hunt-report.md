# Morning synth YouTube hunt: 2026-11-09

Mode: compact library (fold-in). No standalone skills were published. All 6 new skills passed `quality_check_skill.py` (clean) and `novelty_check_skill.py` (NOVEL, scores 0.90–0.93). I hand-checked each against the target cluster's variants in both directions and folded it in with `pipeline/compact/fold_in.py`. LIBRARY.json has 6 new entries (248 → 254 entries, merge_log batch `2026-11-09-morning-hunt`), and `mcp-publish/index.json` was refreshed (33 skills). New ids resolve through `mcp-publish/aliases.json`. All transcripts are YouTube-provided (youtube-transcript-api / yt-dlp, auto or manual captions). No local Whisper/ASR was used, and there were no rate limits this run.

Housekeeping: `.venv` was missing, so `search_youtube_topics.py` failed on `.venv/bin/yt-dlp`. I recreated it with `python3 -m venv --system-site-packages .venv` and symlinked `/home/box/.local/bin/yt-dlp`. It is gitignored.

## Folded in (6)
| video | skill id (alias) | cluster | one-line goal |
|---|---|---|---|
| -yzW0DZuo40 | synth-noise-osc-split-filter-env-air-plus-tuned-noise-layers | brightness-and-air-at-the-source | Synth-native noise air: noise osc on its own LP filter (split routing) opened by a fast envelope for a bright attack, plus a low-shelved tape-noise bed boosted near 6 kHz, a +24 st noise layer on bass, tuned envelope-follower noise on kick/snare and a parallel master noise chain. |
| eG0401qU-Pw | short-kick-three-sub-layers-hierarchical-ducking | bass-design-sub-reese-808-and-layering | Short transient kick + 3 band-focused subs in a ducking hierarchy (all to a ghost kick; sub2→sub1; sub3→sub1+sub2), tape glue, 550 Hz cut, mono. |
| XAch1Q0Iodc | sampler-loop-chord-scrub-parallel-harmony-pad | granular-and-spectral-texture-design | 90s sampler pad: loop one bounced note in a repitch sampler, play chords so voices drift at different speeds, ping-pong loop, wide voicings, slow filter LFO, resample for parallel harmony. |
| nIGiY1jYgWM | phaser-pad-four-bar-ramp-inverse-filter-peaks-reverb-mix-counter-automation | pad-phaser-notch-comb-movement | 12-stage phaser on a 4-bar ramp → delay used as inverse-moving HP/LP filter peaks → narrow-band 100%-wet reverb whose mix is automated opposite to the peaks. |
| HnDS1YURJkE | house-organ-bass-sine-sub-unfiltered-plus-square-fifth-two-octaves-up-lp24-keytrack | bass-design-sub-reese-808-and-layering | Classic house organ bass: unfiltered sine −2 oct sub + square +7 st (fifth two octaves up) through key-tracked LP24 at 30 Hz with 50% env, mono, ~8 ms noise transient, bass-mono <120 Hz. |
| VhjJlD0Gck0 | noof-synth-pulse-noise-saw-octave-unison-saw-closed-ladder-env-cutoff-energy-macro | filter-types-and-resonance-design | NOOF cinematic synth pulse: noise + saw + octave-up 5-voice unison saw into a closed ladder LP with a per-note envelope; one cutoff lane controls energy. |

## Rejected (12)
- **SR9XWpVhWqU**: reverb-tail kick layering — thin; overlaps drum-synthesis boom/whoosh variants; not a soft ambient kick.
- **WpDFPEeBvzI**: cinematic drums by swapping in dhol/taiko library patches — library-locked, thin.
- **gaykd6kuBhU**: Ableton isochronic/binaural "sound healing" — thin, 417 Hz solfeggio, template promo.
- **HsCHTobiv6Y**: 10-minute ambient speed challenge — random MIDI seed (random pitch), DAW-locked, loose.
- **C_k08WO1EZc**: scoring a dialogue scene to picture — spotting advice, not track generation; could be a reference later for Boreal cues.
- **03ByZItqJis**: house build-up breakdown — sample-pack promo; covered by the arrangement build-up/pre-drop and risers variants; snare-roll texture.
- **InSUr0vGgxw**: phaser experiments with randomly drawn automation — random, thin.
- **GA78yWUMZvQ**: Reason fifth-interval house bass — near-dupe of today's HnDS1 fold, which is more precise; factory-patch walkthrough.
- **ilQCsDexooo**: Reason Objekt textural pad — product templates and randomise, ± pitch LFO wobble, collision dings.
- **lQRLKSgU9Us**: Logic pulse bass with arp grid — pulse core covered by the NOOF fold; velocity→cutoff already a filter-cluster variant; pack promo.
- **qViBFmoZLKc**: ostinatos "without theory" (root/4th/5th rhythms) — thin, beginner level, Fiverr promo.
- **WctiTN8PLWY**: FM8 hybrid jam — no reproducible recipe.

Seen in search but not fetched (out of scope, promo, or beginner level): eGrXhugDAO4 (ambient masterclass, course promo, loop-to-arrangement already covered), k40nANMRnG4 / 7LNNKpU2Z34 (binaural for healing), 2bvdVDRpfAQ / 95cHiqdoDsc / CW3jk3BgE1E (ambient for beginners), ZdKxOsK4nQ8 / uhC-5pwVHLw (plugin phaser manuals), m0C7nTIuOl8 (Serum EDM kick), ZeTCWjfN0LQ (braams, cluster already has a braam variant), E3HK05_GhLY / lORu0zmSKzc / Ww-2TtxrZTw (generic width tricks). Already rejected in earlier batches: vYRIXi4A6CU, hfjLuqOK9Co.

## Router note
`route.py` returned CANDIDATES_READY for 17 of 18 transcripts, including obvious rejects (product jams, solfeggio, scene spotting), so the false-novel pattern continues. -yzW0DZuo40 came back OFF_LEXICON even though the transcript is plainly about synthesis: noise, filter routing and envelope vocabulary isn't in `lexicons/synth.json` enough. It was distilled through plain distill-transcript and passed quality and novelty. Consider extending the synth lexicon with noise, low-shelf, split-routing and erosion terms.

## Searches (2026-11-09)
Pipeline `search_youtube_topics.py` (--skip-known, 240–3600 s): "add air to pads high shelf noise layer synth sound design", "soft kick and sub bass for ambient music tutorial", "cinematic kick drum sub layering film score tutorial", "isochronic tones in ableton tutorial", "ambient track arrangement how to structure an ambient song", "how to arrange cinematic music build tension breakdown", "phaser pad sound design tutorial", "punchy bass synth sound design tutorial", "hybrid synthesis sampler and synth layer sound design tutorial", "cinematic pulse ostinato synth sound design tutorial", "how to make a deep punchy bass synth tutorial", "stereo width pad mid side tutorial synth". Web searches for known video ids: air/exciter pads (→ ilQCsDexooo), DAW isochronic (→ only already-rejected ids), ambient soft kick+sub (articles only), ambient arrangement (→ eGrXhugDAO4 promo), hybrid synthesis (product walkthroughs only), phaser pad (→ nIGiY1jYgWM).

## Gaps still open
- **Ambient/cinematic soft kick + sub:** partly addressed. The kick+3-sub hierarchy gives the layering/ducking method, but it is club techno; there's still no soft, rounded, long-body ambient kick recipe. Searches return EDM/trailer kicks.
- **DAW isochronic/brainwave production:** still open. Every hit is healing/solfeggio, Audacity or Gnaural; none puts a gated carrier under a real track.
- **Song structure/arrangement for ambient/cinematic:** no new fold today. The hits were speed challenges, scene spotting or build-up promos; the cluster is already dense.
- **Hybrid synthesis:** still open. Hits were product walkthroughs (Industry, Porphyra, FM8 jams).
- **Synth-native air:** substantially addressed by the noise-osc split-filter fold. A dedicated exciter-on-pad (harmonics-generator) recipe is still thin.
- **Loops / drums:** no new drum fold. Cinematic drum hits were library swaps.

## Carry-overs
- None deferred. Next time, try known ambient producer channels (e.g. specific soft-kick or isochronic-under-music walkthroughs) by video id rather than generic queries.
- Optional lexicon fix: add noise/air terms to `pipeline/lexicons/synth.json` so the router doesn't OFF_LEXICON noise-design transcripts.
