# Use sample-and-hold as a processor on another modulator (not as a random source): step a sine LFO at a rate, automate the LFO rate and the S&H rate separately on a filtered-noise riser so the end seems to slow down through aliasing, and turn a regular step pattern into random hat-loop volume dips with the inverse amount on an FX mix, on a duplicated layer

Goal: Delta beyond our random S&H LFO skill: here S&H samples an input modulator at its own rate. With a sine LFO (unipolar, full amount) into the S&H input, a low S&H rate gives coarse steps over the sine and a high rate follows it finely, so you keep the LFO's regularity with random-feeling steps. On white noise through a filter, map S&H → cutoff at a reduced amount; instead of a linear ramp LFO riser over four bars, put the LFO rate and the S&H rate on automation lanes, ramp the LFO rate to maximum and start the S&H rate low (individual steps audible), so near the end the sampled pattern sounds like it is slowing down. For hat loops, feed a random-drawn 4-bar step modulator (1/8 rather than 1/16) into the S&H and map S&H → volume (unipolar, ~80%) for random level dips, map the same S&H inversely to a metallic FX mix, and keep the processed loop as an extra layer over the original.

Source: [This is Sample & Hold | Cubase Modulators Explained](https://www.youtube.com/watch?v=SZKIODnJuwU)

1. Add a sine LFO and a sample-and-hold modulator, both in Hz. Route LFO → S&H input, LFO unipolar at maximum amount. Sweep the S&H rate from about 1 upward.
2. Generate white noise through a filter and route S&H → cutoff; reduce the amount until it is not excessive.
3. Compare with a simple riser: an upward-ramp LFO over 4 bars on both rates. Note it is linear and not editable; remove it.
4. Expose the LFO rate and S&H rate as automation lanes. Ramp the LFO rate up to maximum over the riser; start the S&H rate low and shape it with its own curve and a few random moves.
5. For a hat loop: draw a random 4-bar step pattern on a step modulator at 1/8, route it to the S&H input (unipolar, max), and route S&H → loop volume (unipolar, ~80%).
6. Route the same S&H to the mix of a metallic FX with inverted amount, so the FX closes where the volume is high.
7. Duplicate the channel: keep the original loop and use the modulated version as a second layer; let other loops fill the quiet sections.

Batch: `2026-10-22-morning-hunt` · transcript: YouTube-provided (Show transcript) · DAW modulator walkthrough; channel intro and comments CTA dropped.
