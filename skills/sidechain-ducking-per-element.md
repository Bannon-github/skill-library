# Sidechain and ducking per element (kick/bass, pads, trance gate, pump)

Goal: Apply sidechain correctly per element: bass/lows duck fully for the whole kick, leads/pads duck only on the punch, depth follows loudness, multiband sidechain for full-range sounds, plus trance-gate chops and pumping pads.

**Theory:** Ducking gain g(t) = 1 - depth·env(t) after each kick; release decides 'pump'. A 50% wet mix only hides a wrong shape and pushes the limiter.

**Hear it:** `sample-lab/theory/sidechain_ducking.py`

## Workflow
1. Key every sidechain from a clean kick trigger (ghost kick if needed).
2. Bass/sub: duck 100% for the kick's length (release ~150-250 ms at 120-128 BPM).
3. Pads/leads: duck 3-6 dB on the punch only, fast release ~50-80 ms; louder elements duck deeper.
4. Full-range sounds: multiband sidechain on lows only.
5. Creative pump/trance gate: volume shaper or gate in 1/16 patterns for chopped pads.
6. Avoid wet/dry 50% fixes; adjust shape instead; check limiter gain reduction.
7. Hear the theory: run `/home/box/audio-tools/bin/python sample-lab/theory/sidechain_ducking.py` from the repo root and compare the sections; reuse its functions as a starting point for renders.

## Source techniques (merged, numbers kept)

### Sidechain-compressor duck synth/pad group to kick
Source: [Sidechain Synthesizers (and any other instruments, also called the sidechain effect or ducking)](https://www.youtube.com/watch?v=e6Ek5Kmieq0) · was `sidechain-compressor-duck-synth-pads`
- Identify dense synth/pad stacks competing with a loud kick on beats 1–2–3–4. Goal: duck those instruments each kick hit to open mix space.
- Group the synth waves onto one bus. Insert a compressor on that group *before* reverb (optional HP on the bus to clear mud). Plain compression without sidechain just thickens—enable sidechain instead.
- Turn on compressor sidechain / external key; set audio-from to the kick track so compression engages when the kick hits.
- Set a strong starting ratio (~6:1). Use a very fast attack so the duck grabs with the kick; start with a slower release so the pad swells back between hits (adjust to taste; exaggerated settings teach the effect).
- Tune threshold (and makeup if needed) so ducking makes kick space without squashing musicality; A/B bypass to confirm clearer kick and breathing pads.

### Per-element sidechain shapes: bass ducks the whole kick, mids/highs duck only the punch, depth set by loudness, multiband for full-range sounds
Source: [Sidechain Tutorials Ruined A Generation of Producers](https://www.youtube.com/watch?v=UwrnD0CSi_U) · was `sidechain-shape-per-element-bass-full-kick-mids-highs-punch-only-depth-by-loudness-multiband-for-full-range-avoid-50pct-mix-limiter-overlap`
- Split the kick mentally into punch (transient/click/attack, the only part with mid/high energy) and tail (mostly low end). Check the kick's total length.
- On the bass/low end, draw a deep duck (high mix/depth, near full) that lasts the whole kick and returns right as the kick tail ends: not before, not way after. A longer kick needs a longer duck.
- On mid and high instruments (leads, synths, pads, vocals to an extent), use a short duck that covers only the kick's punch and then recovers quickly.
- Set depth by loudness. Loud, important foreground layers get deeper, more precise ducks (they pump a bit more); quiet background layers can duck less.
- For a sound with lows plus mids/highs (for example a reese bass), use multiband sidechain: a long, deep full-kick shape on the low band and a short punch-only shape on the mid/high band.
- Avoid partial ducking (for example a 50% mix) as a cure for pumping: the element stays on top of the kick, their summed volume makes peaks, and across many elements it buries the kick.
- Test into a master limiter: raise the input to the fixed ceiling and compare against the old setting.

### Trance-gate: sidechain-gate chop a sustained pad
Source: [The trance gate technique (like Ross from Friends, Bicep, Max Cooper and Moderat)](https://www.youtube.com/watch?v=DxyQNgNKUf8) · was `trance-gate-sidechain-chop-texture`
- Build a source that sustains loudly while held (long notes or short hits + lots of reverb/compression so the wash stays continuous). Optionally thicken with power-chord voicing (root + octave + perfect fifth / +7 st).
- Create a separate trigger track with short clicks/samples on a 16th grid; classic patterns: repeating clusters of 3 sixteenths, or every 16th. Mute/do not mix the trigger into the output.
- Put a gate on the source. Enable sidechain/external key from the trigger track. Raise/lower threshold until the source opens only when triggers fire.
- Adjust gate release for more/less snap (shorter = choppier). Try alternate trigger densities.
- Optional: same technique on a vocal snippet + huge reverb before the gate; add another reverb after the gate to reintroduce space around chops.
