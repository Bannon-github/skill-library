# Per-element sidechain shapes: bass ducks the whole kick, mids/highs duck only the punch, depth set by loudness, multiband for full-range sounds

Goal: Set sidechain ducking per element instead of one kick-shaped duck on everything: the bass and low end duck deeply for the whole kick length (returning exactly as the tail ends), mid/high instruments duck only briefly around the kick's punch/transient, and loud foreground layers duck deeper than quiet background layers. Full-range sounds such as a reese use multiband sidechain with separate low and mid/high shapes. Don't fix pumping by lowering the mix knob, because partial ducking leaves kick and element overlapping and that shared volume hits the master limiter early. Delta vs the generic sidechain-compressor-duck-synth-pads skill: shape and depth rules per element and the loudness/limiter reason.

Source: [Sidechain Tutorials Ruined A Generation of Producers](https://www.youtube.com/watch?v=UwrnD0CSi_U)

1. Split the kick mentally into punch (transient/click/attack, the only part with mid/high energy) and tail (mostly low end). Check the kick's total length.
2. On the bass/low end, draw a deep duck (high mix/depth, near full) that lasts the whole kick and returns right as the kick tail ends: not before, not way after. A longer kick needs a longer duck.
3. On mid and high instruments (leads, synths, pads, vocals to an extent), use a short duck that covers only the kick's punch and then recovers quickly.
4. Set depth by loudness. Loud, important foreground layers get deeper, more precise ducks (they pump a bit more); quiet background layers can duck less.
5. For a sound with lows plus mids/highs (for example a reese bass), use multiband sidechain: a long, deep full-kick shape on the low band and a short punch-only shape on the mid/high band.
6. Avoid partial ducking (for example a 50% mix) as a cure for pumping: the element stays on top of the kick, their summed volume makes peaks, and across many elements it buries the kick.
7. Test into a master limiter: raise the input to the fixed ceiling and compare against the old setting.

Verify: Gain-reduction meter on the master limiter shows less reduction at kick hits than with the one-shape/50% setup at the same loudness; The bass duck ends within a few ms of the kick tail end; A/B listening: no audible pumping on the leads/pads, kick still clear

Transcript: YouTube-provided (Show transcript); the promo section was dropped.
