# Block Loop (2026-11-21)

Score 99.63 pass (iter 4 kept; iters 94.91 / 98.31 / 99.66 / 99.63 — all passed; iter 4 kept because it brought block brightness span from 1.08 to 1.01 oct). LUFS -17.0, TP -2.1 dBTP, limiter GR 0 dB, 81.3 s (30 bars + 3 s tail), E minor (Em-C-G-D, 2 bars each), 92 BPM. Kick + bass come in at 10.43 s (bar 4). Before that there's only the PWM pad. No rapid ticks, no random pitch.

Skills (all first tests):
- P 80s PWM string pad, free-running LFO + detune (cinematic-synth-0n23itgG0LU, synth-strings-choir-ensemble)
- D delay as instrument: Haas / delay-chorus / 100 % feedback looper / repitch octaves / grain octave (cinematic-synth-VSGYqvV4bTg, 11-20 hunt, reverb-delay-space-and-shimmer, loops gap)
- B dynamic-interest 16-bar block map (cinematic-synth-JHiTUBVLmFI, 11-20 hunt, arrangement-loop-to-song-build-drop)

P: band-limited pulse with per-sample PW, 0.7 Hz free-running sine on PW (0.5 ± 0.32), osc 2 = saw at 0.6 level +7 cents, 2 voices ±1.5 cents, static LP 4.2 kHz (1-pole) / HP 90, no filter env, attack 1.4 s, release 2.6 s.
D: delay-chorus on the pad (20 ms base, 3 ms depth, 0.45 Hz, L/R LFO offset 90°, feedback 0.35, mix 0.5). Haas clap with L at 0 ms; R searched 8-22 ms while mono-summed, which picked 11 ms (mono peak -2.7 dB). Looper: 1-bar loop at 100 % feedback, overdubbing one note per cycle from bar 4 (E4 G4 B4 D5). Repitch steps are an exact 2:1 resample (+12) at bars 14-20 and 22-26. Feedback goes to 0 at bar 26 and the loop dies after one cycle. It's resampled under the pattern (11 ms Haas + 3.5 s verb). Grain-delay +12 octave layer fades 0→0.25 wet over bars 20-22.
B: the 16-bar blocks are scaled to 4-bar blocks: intro(-) / B1 kick+bass+500 Hz noise hit / B2 shifts to Haas clap / B3 adds soft offbeat open hat, with a turnaround at bars 14-16 (lows scooped + looper octave up) / B4 BREAK (no kick/bass/perc, reverse pad-verb swell into bar 20) / B5 DROP ++ (marker splash, call/response lead, grain octave layer) / 2-bar squeeze-in = minimalism (kick + lead + pad, no bass/perc) / outro (scoop-up at bar 26, kick out at 28).

Checks: side<120 Hz -27.2 dB, M5 side<150 -20.9 dB, tilt -6.3 dB/oct, M7 9.1 (sub 0.97), corr 0.26, width 0.76, HF spikes 2275 (offbeat hat onsets, visible as regular hat lines in the spectrogram, not clicks). Block centroids 583/321/371/398/554/534/648/465 Hz, span 1.01 oct (yesterday's ≤~1 oct suggestion was met).
Iterations: iter1 94.91 (M5 side lows -13.7, tilt -7.2 too dark, M7 10.2) → side HP 160→220, pad LP 2.6k→3.4k, looper LP 3.2k→4k, kick/bass down → iter2 98.31 → pad LP 4.2k, pad HP 110→90, hat .035→.045 → iter3 99.66 (span 1.08 oct) → noise hit .05→.07, bass .12→.11 → iter4 99.63, span 1.01.
Unclear: PWM skill gives osc-2 level/detune in synth display units (17.5 / fine 0.20) and attack "38", so I chose +7 cents, 0.6 level and 1.4 s. The osc-2 waveform isn't stated (saw assumed). Delay skill: "delay time at maximum" = 1 bar (Ableton max sync 16 sixteenths assumed). It gives no chorus depth or flanger numbers and no grain spray/frequency values. Block map assumes 5-min tracks (10 × 16 bars), so it has no rule for scaling to a 90 s test.
