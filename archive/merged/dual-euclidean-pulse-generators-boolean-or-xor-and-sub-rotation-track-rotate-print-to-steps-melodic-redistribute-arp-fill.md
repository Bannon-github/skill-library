# Two Euclidean pulse generators per track combined with Boolean logic (OR, XOR, AND, SUB), per-generator rotation and whole-track rotation, then printed to an ordinary step sequence for hand edits; also used to redistribute an existing bassline and to leave gaps an arpeggiator fills

Goal: Generate musically coherent, non-obvious drum and melodic patterns by combining two Euclidean pulse generators on one track. Each generator spreads N pulses as evenly as possible over the track length (e.g. 16 or 32 steps); numbers that do not divide the length (5, 9, 11, 12) give the interesting grooves. Combine the two with a Boolean operator: OR (any pulse plays; overlaps become one note), XOR (overlaps are removed, leaving space), AND (only overlaps play; the number of possible notes is limited by the smaller pulse count) or SUB (generator 1 minus where it overlaps generator 2, a way to carve notes out). Rotate each generator to change their relationship, then rotate the whole track to move the downbeat of the combined pattern. Print the result to a normal step sequence to edit single notes, apply the same Euclidean distribution to a pre-programmed melodic line (notes stay, positions change), randomise the Euclidean settings with a snapshot to return to, and let an arpeggiator with step offsets fill the gaps. Delta beyond our probability/seeded loop skills: the two-generator Boolean combine plus print-to-steps workflow, mapped to Polyrhythm Studio lanes.

Source: [How I Actually Use Euclidean Sequencing on Digitone 2](https://www.youtube.com/watch?v=WeOuxcN0pV8)

1. Turn on Euclidean mode for a drum track. Set generator 1 to a simple count (e.g. 4 pulses over 16 steps) and listen; then try counts that do not divide 16 (5, 11).
2. Enable generator 2 with a different count (e.g. 5 against 4) using OR. Rotate generator 2 to move its hits against generator 1.
3. Switch the operator: XOR to remove overlapping hits and open space; AND to keep only overlaps (raise counts, e.g. 9 and 12, and rotate until notes appear); SUB to keep generator 1 except where generator 2 lands.
4. When an emergent pattern makes a new downbeat, use whole-track rotation (e.g. +3 steps) to move both generators together so that hit becomes step 1.
5. Print the pattern to the normal step sequencer, then hand-edit (move a note, leave room for a snare). Build hats on another track at length 32 with SUB to carve notes out of a dense generator 1.
6. On a melodic (bass) track with notes already programmed, enable Euclidean mode so those notes are redistributed by the pulse pattern; add generator 2 with XOR and rotate the track. Randomise the Euclidean settings repeatedly until a version works.
7. For sparse patterns, enable an arpeggiator and remove one arp note with its offset/step mask so it fills gaps without crowding.
8. For performance, change rotations and pulses on all tracks at once, and keep a snapshot so you can jump back to the original pattern.

Batch: `2026-10-21-morning-hunt` · transcript: YouTube-provided (Show transcript) · Hardware walkthrough; device button combos and part-two teaser dropped.
