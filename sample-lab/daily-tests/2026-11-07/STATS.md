# 2026-11-07 daily 3-skill test: "Dusk Lift"

74 s, D minor, 96 BPM, 28 bars. Drums in at 10.0 s (bar 4). Retry of the failed 2026-11-05 test (numba was missing that day).

Skills
- lush-dual-saw-filter-env-nonretrigger-lfo-pad (wavetable): 8-voice 30-cent dual saw + saw -12, slow filter env 200 Hz +2800, 3-bar non-retrigger LFO. Wide, warm bed; carries the whole track.
- wide-bass-remove-fundamental-add-mono-sine (bass): unison saw mid layer HP'd above the fundamental (split 110 Hz) + mono sine sub. Side below 120 Hz is -26.8 dB vs mid, so lows stay mono while the bass reads wide.
- nested-lfo-layered-riser-downer-kit (risers): LFO1 drives LFO2 rate; downer, main riser, atmos, noise layers into the peak. Stutter layer muted (Matt dislikes rapid clicking textures).

Score: 99.86 pass on iteration 1 (M6 0.99, M13 0.986). -17.0 LUFS, true peak -5.1 dBTP, limiter 0 dB GR.
Click check: no block-boundary clicks; HF envelope periodicity at 11-13 Hz only from the drum grid.

Renderer fixes: the 11-05 script ran block-wise SVF / sosfilt (512-sample blocks, state reset each block = ~94 Hz click risk, same bug as Air Bookend). Replaced with per-sample-cutoff dsp.svf over the full buffer; flt() now accepts array cutoffs.

Tweak: true peak -5.1 dBTP with 0 dB GR means the mix is crest-heavy (pad transients/kick); add ~2 dB of glue compression on the drum bus so LUFS can hold without that much headroom waste.
