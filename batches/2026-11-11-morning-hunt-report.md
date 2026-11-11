# Morning synth YouTube hunt: 2026-11-11

Mode: compact library (fold-in). No standalone skills were published. All 5 new skills passed `quality_check_skill.py` (clean) and `novelty_check_skill.py` (NOVEL, 0.91–0.94). I hand-checked each against the target cluster's variants and folded it in with `pipeline/compact/fold_in.py`. LIBRARY.json went 260 → 265 entries (merge_log batch `2026-11-11-morning-hunt`). `mcp-publish/index.json` was refreshed (33 skills) and the new ids resolve through `mcp-publish/aliases.json`. All transcripts are YouTube-provided (pipeline fetcher: youtube-transcript-api / yt-dlp captions). No Whisper/ASR was used.

Rate limiting was lighter than yesterday. The fetcher's internal retry recovered HyXvY_PXI9Q and bXd6Fys0raw. NAEyg_eXP14 failed twice (`rate_limited_or_ip_blocked`, retried after a 45 s gap). P--40MYlGuI has **transcripts disabled**, so it can't be fetched under the no-ASR rule; I've dropped it from carry-overs.

`route.py` returned CANDIDATES_READY for every transcript I routed, including obvious rejects. The false-novel pattern continues, so I kept hand-checking.

## Folded in (5)
| video | skill id (alias) | cluster | one-line goal |
|---|---|---|---|
| _MgJJpqxcn8 | filtered-vibey-drum-bus-lowpass-1k-boxy-mid-tube-drive-borrowed-verb-sends-automated-long-plate-throws | drum-groove-programming-swing-and-ghosts | Filtered ambient drum bus: low-pass to ~1 kHz with a 500 Hz–1 kHz boxy boost and gentle tube drive, sends to the mix's existing (chorused, EQ'd) reverbs, an 8 s+ low-cut plate opened by automation only at phrase ends, and a gain ride into section ends. |
| aBiz2axINMA | monaural-beat-two-fixed-sines-or-tremolo-at-entrainment-rate-on-playable-pad-speaker-safe | brainwave-binaural-isochronic-layers | DAW brainwave layer that also works on speakers: two fixed sines a target-rate apart summed in mono, or a tremolo (auto-pan in tremolo mode, ~40% shape) at the target Hz on a playable pad, so chords pulse. Carrier is tuned to a key note. |
| 64H_K7rosSo | sleep-descent-arrangement-40-50bpm-descending-lines-staggered-fade-ins-lowpass-recede-key-tuned-binaural-notch | arrangement-ambient-cinematic-score | Descent-only sleep/meditation arc at 40–50 BPM: a loop-first sketch with descending in-key lines, slow per-layer fade-ins, low-pass automation so the mix "moves away", a scaled-in EQ low cut where layers hit the bass, a long master fade, and a key-root binaural/monaural pair with a narrow notch carved for it. |
| BfRyPzy-e-k | dub-stab-family-detuned-saw-lp24-res-hp120-drawn-cutoff-dual-bandpass-lfo-sidechained-dub-verb | filter-types-and-resonance-design | Dub-techno stab family: detuned saws into a resonant LP24 at ~100 Hz with env amount and HP 120 Hz, hand-drawn cutoff automation that differs each repeat, dual resonant band-pass + chorus, a kick-sidechained dub-verb return, breakdown-only long-verb/echo automation, and one four-note minor chord (triad plus the note a tone below the root). |
| HyXvY_PXI9Q | sample-to-synth-keygroup-mono-lowpass-env-pluck-resonance-square-lfo-steps-octave-layer-through-one-filter-reversed-octave-granular | granular-and-spectral-texture-design | Hybrid synthesis on any sampler: map a one-shot chromatically, then low-pass env sweep/pluck, resonance, a 1/8 square-LFO for filter steps, an octave/other-sample layer through one shared filter, then distortion/chorus, a reversed +12 granular layer and reverb. |

Matt's preferences are written into each skill's constraints: steady pitch (no random/wobbly variation; I dropped the video's portamento, vibrato-delay and fast auto-pan), no rapid clicking or rolls (echo throws stay sparse), drums early (~8 counts / ~12 s), Ableton/MIDI-friendly, and portable module mapping.

## Rejected (8)
- **X_yfys8wAJ4**: first ambient track in Logic (carry-over). Beginner one-shot/freebie walkthrough with randomly played melodies and a masterclass promo. Nothing beyond the existing ambient clusters.
- **4MDD4zRaMjw**: tension and energy in electronic music. Mostly conceptual (macro/micro tension, start with the drop). Its tools (removal, silence before the drop) are already in arrangement-loop-to-song, and it leans on snare rolls.
- **bXd6Fys0raw**: subtractive arrangement (duplicate the loop to 6 min, then delete). Near-duplicate of the existing four-levels/subtractive and loop-to-song variants.
- **lR3FbYzwgZw**: atmospheric "air group" layer. A class walkthrough built on preset browsing (Ableton packs), so it isn't portable.
- **oVF57Bnm4UE**: custom kicks and snares. Rambling beginner session; the pitch-env sine kick and 100 Hz snare tuning are covered by drum-synthesis.
- **KTSzOfVYDZY**: punchy sub in the master. A mastering plugin list with service promo; low-band saturation/harmonics is already in the bass cluster.
- **tbMIVusd3zY**: mineral ambient. Locked to FL Studio plugins, and its texture relies on a vocoder pitch-shift "float" and transient-random granular loops (wobbly/random, against Matt's preference).
- **P--40MYlGuI**: hybrid score from manipulated orchestral samples (carry-over). Transcripts disabled. Not distilled (no ASR).

Not fetched (YouTube 429/IP block after retry, no transcript saved): NAEyg_eXP14 (3 types of ambient from 1 concept).

Seen but skipped (beginner, product, off-genre or duplicate titles): 5wIcu7h334w / JHiTUBVLmFI (techno arrangement), veMIOXVSJZU / dMzMmnRT_HE (transition listicles), RaqEN_VYVmM, LoQ57jDqAlo, GXNWpGSkgBo, _hP2Qj-9czA, 2tbBNwxt3PQ, kzkDoBupXKM (Logic binaural; method already covered), s3t02k1-G74, ygWakdkYXSo, rswG_lIggmY, vr0DHvuQX8E, UQpyAuq5vHk, F9PApia-X8w / LTF-1N_MFkw / vOtyvqePS1s (FM8/Massive preset tours), WxK8rUl_qnU, ZdKxOsK4nQ8 / uhC-5pwVHLw (plugin FX manuals), o6rBYtj-X5U, 1rWlrInQzh0, y4w_mNuhxmw, bLq5oPoLP0M, nhN1urALopY, b5jovcXYMG4, NqyP9KdWtgU, v97MvZ1XhXM, l1pxzjfwX1c, 5Cu1f2h-Rwk / 7rj31n2kC-o / pxrKn3NNKJY (product walkthroughs), RMXbPOeWA1Y, WeNPbWpHs5I, stereo/M-S hits spaqBr-cCFw, dZVfu4b48ek, 4p-lf94VRkw, HRtqWS5oqtA, lORu0zmSKzc (stereo cluster already deep).

## Searches (2026-11-11)
`search_youtube_topics.py --skip-known` (240–3600 s): ambient arrangement sections/build/breakdown/transition; cinematic structure tension & release; isochronic tremolo/gate on pad (Ableton); brainwave entrainment production (Ableton); soft round ambient kick + sub; noise layer on pad for air; phaser pad; ambient loops from synth sounds; punchy bass; hybrid synthesis sampling + synth layering; stereo width pad M/S; modulation evolving pad macro automation. Logs are in `batches/work-2026-11-11/`.

## Gaps still open
- **DAW isochronic/brainwave production:** largely addressed. The tremolo-on-pad monaural recipe plus the key-tuned binaural pair with notch carving fill the "in-track" gap. Still missing: a slow rate-ramp automation walkthrough (e.g. 8 → 4 Hz over a section).
- **Ambient/cinematic arrangement:** improved with the descent-only sleep arc. Still wanted: ambient-specific build/breakdown transitions. NAEyg_eXP14 is still queued.
- **Soft ambient kick + sub:** still open. Searches keep returning EDM/trap kicks. Next time, try searching by channel/id (e.g. "felt kick ambient techno", "lo-fi soft kick synthesis").
- **Synth-native exciter/noise air on pads:** still thin. The "noise layer on pad" query returned only preset tours.
- **Hybrid synthesis:** improved with sample-to-synth. Orchestral-sample manipulation is still missing (P--40MYlGuI has no transcript).
- **Loops/drums:** improved with the filtered ambient drum bus.
- **Phaser pads:** the dub stab dual band-pass adds phasey motion. There are no new pure phaser-pad recipes (hits were plugin manuals).

## Carry-overs
- Refetch when not rate-limited: NAEyg_eXP14.
- Dropped: P--40MYlGuI (transcripts disabled), X_yfys8wAJ4 (rejected), _MgJJpqxcn8 (folded).
