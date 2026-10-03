---
name: Ambient Web Audio quality pass
description: >-
  Use this when reviewing or upgrading Web Audio synth/mix quality for
  generative ambient or polyrhythm browser apps.
---
# Ambient Web Audio quality pass

Use for generative / ambient browser instruments (Web Audio + Canvas), not DAW sessions.

## Goals
Lush, slow, meditative sound. No toy beeps, no hard clicks, no metronome-drill energy unless requested.

## Checklist
1. **Envelope** — soft attack (≥15–40 ms) and long release on melodic voices; bass can be shorter but never instant on/off.
2. **Voicing** — prefer sine/triangle/pad/bell with gentle lowpass; avoid raw square/saw at full brightness unless filtered.
3. **Stacking** — limit simultaneous voices; apply gentle compression + makeup; pan voices across stereo.
4. **Space** — real or algorithmic reverb wet enough to glue (often 0.3–0.55); short feedback delay optional; darken delay with lowpass.
5. **Density / simplicity** — expose sparse↔busy control; ambient presets default sparse (long gaps between hits).
6. **Pitch** — scale-constrain melodic voices; map size/period to register (fast/small = high, slow/large = low).
7. **Scheduling** — lookahead scheduler on `AudioContext.currentTime`, not `setInterval` for note times; resume suspended context on user gesture.
8. **Listen test** — 30s with eyes closed: if it sounds like a UI kit, rewrite synths before adding features.

## Deliverable
Concrete graph/parameter changes (node list + values), not vibe-only feedback.
