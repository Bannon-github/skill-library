# Parallel FX network: same input to up to three effects, heavy drive alongside clean delay, phase-flip a loop to cancel its dry and keep only wet, per-loop EQ/levels, effects inside the delay loop

Goal: Turn a serial chain into a parallel effects network for synth/pad/lead layers: feed the same dry input to up to three effect loops and sum them (so a high-gain drive can growl in the background while a delay stays clean), use a per-loop phase invert to cancel the dry component of an effect without a wet-only mode (inverted dry + summed dry ≈ wet only), check for effects that already invert phase (chorus) against the dry, balance with per-loop EQ, send/return levels and master, and place an effect inside a delay's feedback/insert loop so repeats get processed — the portable parallel-distortion wet/dry recipe that was missing from the library.

Source: [Pedals in Parallel - Discovering new ways to use effects you thought you knew](https://www.youtube.com/watch?v=t0X_HQ25jmg)

1. Baseline: compare serial distortion→echo with echo→distortion to hear order-dependence.
2. Parallel: split the same dry input to drive and delay branches and sum. Keep drive high and sustaining in its branch while the delay branch handles clean repeats.
3. Remove the dry from an effect that has no wet-only mode: flip the phase of that branch so its dry component cancels against the dry in the sum, leaving (mostly) the delay.
4. Chorus = vibrato + dry: test phase flip on modulation effects; inverted dry won't fully 'unbake' into pure vibrato, and some pedals already invert phase, so pick the setting that sounds fuller.
5. Balance each branch with its EQ, send and return levels and a master volume; take the dry out entirely when only effects are wanted.
6. Insert loop: put another effect (e.g. modulation/space) inside the delay's insert/feedback path so delayed sound is processed again on each recirculation.
7. Swap in different trios of effects (e.g. delay + modulation + tremolo, envelope-controlled tremolo) to discover combinations.

Batch: `2026-10-14-morning-hunt` · transcript: YouTube-provided (Show transcript)
