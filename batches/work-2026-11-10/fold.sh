cd /workspace/skill-library
P="27ewHn5SAiI:bass-design-sub-reese-808-and-layering u4tg0u-THS8:arrangement-ambient-cinematic-score N60Jcn9zfBo:drum-synthesis-and-hybrid-percussion RPzAJFC_JkI:wavetable-and-vector-morph-pads 3zIsQfKtUno:drum-groove-programming-swing-and-ghosts 6x1_XZDcI8I:arrangement-loop-to-song-build-drop"
for x in $P; do v=${x%%:*}; c=${x##*:}; python3 pipeline/compact/fold_in.py distilled/$v/agent-skill-*.json $c; done
python3 batches/work-2026-11-10/lib.py $P
