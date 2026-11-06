# Brightness and air at the source for pads and textures

Goal: Make pads bright and airy from the start (instead of boosting treble at the end): choose harmonically rich oscillators, open and key-track the filter, add octave/fifth layers, excite upper harmonics, add a quiet air-noise layer, brighten before reverb and only then a gentle shelf.

**Theory:** Perceived brightness tracks spectral centroid, which rises with energy in upper harmonics. EQ can only boost what exists; saturation/exciters create new harmonics; octave layers add bright partials that are musically related.

**Hear it:** `sample-lab/theory/brightness_air.py`

## Workflow
1. Measure first: spectral centroid of the pad vs a reference (ambient pads ~1.5-3 kHz; dark tests sat ~0.8 kHz).
2. Oscillator: saw/supersaw or bright wavetable frames rather than sine/triangle; keep enough harmonics (no low-passed sources).
3. Filter: cutoff 3-6 kHz, key-tracking 50-100%, filter env to open on attack; avoid treble-cut on the pad.
4. Layer: octave-up sine/triangle or glock/bell partials at -12 to -18 dB; pluck/struck layers bring natural brightness.
5. Exciter: high-pass a copy at ~3 kHz, saturate (tanh/tube), blend -12 dB; or pitch-shift +12 in reverb (shimmer).
6. Air: high-passed noise >8 kHz at -24 to -30 dB following the pad envelope.
7. Brighten before reverb/delay (pre-send), not on the master; finish with a gentle 10-12 kHz shelf (+1-3 dB) only if needed.
8. Check harshness at 2-5 kHz and on small speakers; re-measure centroid.
9. Hear the theory: run `/home/box/audio-tools/bin/python sample-lab/theory/brightness_air.py` from the repo root and compare the sections; reuse its functions as a starting point for renders.

### Start-bright-then-filter pad: pick a harmonically rich (buzzy/bright) oscillator, odd unison 5-9, slow wavetable-position sweep, then low-pass to smooth it (keeping top-end headroom to automate back in), big low-cut reverb, low-cut EQ and a stereo imager to pull the pad around the listener; plus an attack-removed swell pad from any played source
Source: [Sound Design - Ambient Pads and Atmospheres](https://www.youtube.com/watch?v=TosV3erGfsg) · was `start-bright-then-filter-pad`
- Set amp attack and release to about 400-500 ms each as a starting point, then tailor to the part.
- Choose a bright, buzzy, harmonically rich oscillator (a saw, or a PWM/analog-style wavetable). Try many; keep the one with the most high-end energy and character.
- Unison: an odd voice count (5, 7 or 9) gives a solid centre voice with voices spread either side; below 5 is not lush, above 9 costs CPU. For a rougher 'organic' pad, use an even count (e.g. 4): no centre voice gives a slightly unstable, edgy quality. Detune stays static.
- Optional motion: route a slow LFO or long envelope to wavetable position so it sweeps gently through the table.
- Low-pass the tone inside the synth (12 or 18 dB/oct; 18 gives a more pronounced cutoff) until smooth, then raise volume to compensate. Use the filter rather than an EQ so the cutoff can be automated to reintroduce highs for builds.
- Space: a very large reverb at high mix with plenty of low-cut (filter before or after reverb, either order works), then an EQ cutting excess low end and optionally a second reverb.
- Add a stereo imager after the reverbs and A/B: without it the pad sits far in front; with it the pad wraps around the listener.
- Swell variant: play chords or a melody on any source (guitar, piano, vocal), start slightly before the bar, and put a gain envelope first in the chain that rises from 0 at the bar so the attack is removed. Then low-cut EQ, imager, and reverb, which is now fed only by the swell.

### Ambient air layer from a field recording: HPF out traffic lows, subtle harmonic exciter for upper sparkle, light high-end lift; keep it subtle to avoid glassy mess
Source: [Ambient Step by Step Tutorial - Techniques and Processing: Creating Ambient Environment Soundscapes](https://www.youtube.com/watch?v=HPDGp6b829s) · was `field-recording-hpf-exciter-air-layer`
- Place a field recording on its own track above the ambient bed. Solo and find the useful high detail (e.g. a bird call) and the muddy low end (traffic / human noise pollution).
- High-pass the recording to remove the low-end pollution. Expect the bed to sound a bit colder/thinner — that is intended before air is restored.
- Add a subtle harmonic exciter / upper-band enhancer ('fresh air' style) to excite upper frequencies so the clip sounds less dull and distant calls poke through. Keep the amount very low.
- Optionally add a small high-end shelf/boost for the same emphasis. A/B against the bed; if it turns glassy or harsh, back off exciter then shelf.
- Optional motion (same chain idea on a second ambience layer): duplicate with time-stretch/smear automation alternating wet/dry, and/or slow tremolo with changing rate that also pans L↔R for headphone width. Keep levels under the musical bed.
- In the full mix, verify the air layer adds space above ~ several kHz without muddying the pad/drone. Use storytelling markers (a single call → larger event) if arranging a nature-to-elsewhere transition.
