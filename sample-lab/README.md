# Sample Lab

Offline renderer plus skill-chain workflows plus a quality target for cinematic/ambient samples (original synthesis only).

- `TARGET.md`: the quality target (hard gates, 15 metrics, composite ≥ 85 with no sub-score < 0.5; reliable = passes on every note/seed in the grid).
- `leaderboard.md`: winning systems and progress by round. `FINDINGS.md`: what was learned about the skills.
- `systems/<name>/`: chain.json, README.md (which skills fire in which order and why), scores.json, patch_resolved.json, WAVs plus spectrograms.
- `workflows/<name>.md`: reusable workflow-skill drafts.
- `iterations.jsonl`: every candidate evaluated. `runs/`: population, logs, stats.
- `engine/`: dsp.py (numba DSP), render.py, skills.py (skill → parameter appliers with cites), metrics.py, lab.py, iterate.py, finalize.py.

Render a system by name:

    .venv/bin/python render_system.py --list
    .venv/bin/python render_system.py pad-wide-supersaw-chord-pad --notes 50,53,57,64 --seed 7 --score --spectrogram
    .venv/bin/python render_system.py drone-wavetable-artifact-drone --grid

Run more search rounds: `cd engine && ../.venv/bin/python iterate.py --rounds N` (see `--help`).
