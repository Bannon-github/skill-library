# Zone Gate (2026-11-25)

Score 99.77, pass (iter 2 kept; iter 1 99.78 but tilt -6.51 and width 0.2495 just outside target bands). -17.0 LUFS, true peak -4.5 dBTP, limiter GR 0 dB. 88.3 s (32 bars + 3 s tail), A minor (Am(add9)-Fmaj7-C-G6, 2 bars each), 90 BPM. Kick + bass at 10.67 s (bar 4); body pad + quiet air only before. Steady fixed-pitch lead (no glides/bends/random notes), no hats/ticks.

Skills (all first tests, all from this morning's hunt):
- ZO: ambient zone owners + establish/expand/contrast/return (cinematic-synth-YdnMi_TIXso, arrangement-ambient-cinematic-score)
- KK: acoustic-style 4-layer kick (cinematic-synth-oRhBZ6L9rU8, drum-synthesis-and-hybrid-percussion)
- GA: autopan phase-360 amplitude gate on long texture (cinematic-synth-RDubhupxDsw, brainwave/isochronic; fixed rate)

Form: establish a 0-4 body pad (two copies of the same pad, 0.67 beat out of sync, panned +/-0.6, HP150/LP2.3k) + air | establish b 4-8 kick 1&3 + mono unison bass on A1 (roots A1/F1/C2/G1, sine sub) | expand 8-16 focal lead (sine/tri, 8 ms atk, LP 6.5k, drier) | contrast a 16-20 hand-off: lead + kick out, one saw pluck 8th arp (LFO 0.06 Hz on LP 900-3.8k, dotted-1/8 delay fb .35), gated texture ramps in | contrast b 20-24 kick back | return 24-30 opening material + lead, gated texture kept at 0.55 (the new element) | end 30-32 pad + bass + gate.
Notes per section: expand 28, contrast a 32, contrast b 32, return 21.

ZO: one owner per zone (bass <150, pad 150-800 body, lead/pluck focal, air >8k); depth via level/attack/brightness/reverb only; air = noise LP 13k + fixed comb 420 Hz + HP 5k into 5 s reverb at -20 dB re pad RMS; one new foreground element per section.
KK: sine body 48 Hz phase 90 with +20 st pitch env (tau 28 ms), decay 0.26 s; transient sine 3.2 kHz phase 95, 2.5 ms; 'acoustic sample' layer = fixed-seed membrane modes 172/268/395 Hz + band noise, 6 ms fade-in, HP 180, gain .18; pink-noise tail .04/60 ms; +3 dB low, +2 dB 2-6k, fast comp ~half amount. Same hit reused (sample-identical, no random phase).
GA: texture = chord tones +12 saws LP 4.2k; autopan 1/16 at 90 BPM = 6.0 Hz, L/R phase 360 => identical gain both sides (envelope correlation 1 by construction), shape .6 = flatter tops with raised-cosine edges, 4.5 s reverb after the gate; amount 0 -> ramp bar 16 -> 1.0 (17-24) -> 0.55 (return).

Checks: side<120 Hz -37.7 dB; section centroids 646/257/441/461/443/475/265 Hz = span 1.33 oct (establish b and end darkest: bass+kick with no focal voice); section LUFS -22.5/-19.6/-15.8/-17.0/-17.5/-15.3/-18.2; HF spikes 903; M13 0.995 sub-score from the template's 0.3 s zeroed tail.
Iterations: iter1 99.78 (tilt -6.51, width .2495) -> pad LP 1.6k->2.3k, pads +/-0.45->0.6, lead LP 5.2k->6.5k, bass .30->.27; iter2 99.77 (all metrics in band).
Deviations/unclear: KK needs an acoustic kick one-shot - synthesized (membrane modes + noise) since no sample; 'tune down a couple of semitones' and body/transient decay times not given. ZO's 'two loops slightly out of sync' gives no offset amount (0.67 beat used) and the establish section (body+bass only) is necessarily the darkest, which fights the lab's centroid-span check. GA's 1/16 at 90 BPM is a 6 Hz pulse; shape/waveform values are Ableton-specific, mapped to a raised-cosine with flattening; no reverb size given (4.5 s used).
