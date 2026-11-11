cd /workspace/skill-library
P="_MgJJpqxcn8:drum-groove-programming-swing-and-ghosts aBiz2axINMA:brainwave-binaural-isochronic-layers 64H_K7rosSo:arrangement-ambient-cinematic-score BfRyPzy-e-k:filter-types-and-resonance-design HyXvY_PXI9Q:granular-and-spectral-texture-design"
for x in $P; do v=${x%%:*}; c=${x##*:}; python3 pipeline/compact/fold_in.py distilled/$v/agent-skill-*.json $c; done
python3 batches/work-2026-11-11/lib.py $P
