# Animate a static pad with a stepped 12-band stereo filterbank: assign groups of bands to sequencer patterns (offset ups vs a big down note), set a Q slope with wider low bands and narrower high bands, tame resonant peaks with mild drive plus smoothing compression, alternate bands L/R for width, and use per-band versus group random triggering

Goal: Turn a sustained pad into rhythmic, moving texture with a sequenced filterbank of 12 bands per side. Use each band's volume as an EQ to keep what works. Assign subsets of bands to a step sequencer pattern (first five bands, then three frequencies with an offset 'up' pattern, then the last bands as one big down note). Increase the Q globally to get pointed peaks but apply a slope so low bands stay wider and high bands narrower. Add a little drive and a negative 'pull' (compression-style) setting to smooth peaks that blow up at high Q. Spread by sending alternate bands to left and right (sending the same band to both stays mono). Use random triggering per band ('S': each band triggers independently) or grouped ('A': grouped bands fire together) for subtle versus extreme motion. Distinct from our filter-spread and phaser skills: discrete stepped bandpass bank.

Source: [Philtor 12 Band Sequencer Filter](https://www.youtube.com/watch?v=Py4XQbjvn4o)

1. Insert the 12-band stereo filterbank on a static pad and use the band volumes as an EQ, turning down only the bands that are too much.
2. Raise the global Q from fully open (no contour) until the bands become pointed, and apply a slope so low bands are wider and high bands narrower.
3. Add a little drive and set the compression/'pull' control negative so peaks are smoothed without much distortion.
4. Assign the first five bands to a step pattern; then unassign them and give three frequencies an offset pattern of up notes; finally give the last bands a single big down note.
5. Alternate bands between left and right (flip-flop) for stereo spread, choosing the assignment that works in the mix.
6. Enable random triggering: per-band mode makes each band trigger independently (subtle, dense); grouped mode makes grouped bands fire together (sparser, more extreme). Fine-tune band volumes to contour the result.

Batch: `2026-10-16-morning-hunt` · transcript: YouTube-provided (Show transcript) · Device-specific labels (S/A random modes, 'pull') mapped to generic per-band vs grouped random trigger and compression.
