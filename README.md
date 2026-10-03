# YouTube Practical Skills Library

**Guiding purpose:** An agent that can do anything a human can do, by learning from YouTube how-to videos through their available transcripts (not pixels), via skills, workflows, and sequenced curriculums.

## Layout
- `LIBRARY.json` — catalog
- `topics/taxonomy.json` — topic categories
- `curriculums/` — sequenced learning paths
- `raw/<video_id>/raw` — YouTube-provided transcripts only
- `distilled/<video_id>/` — output of distill-transcript skill
- `skills/` — executable skill recipes
- `pipeline/STAGES.json` — search → raw → distill → (summary dest TBD) → publish
- `batches/` — dated intakes

## Pipeline
1. User topic → how-to search → titles/links/transcript status → **confirm**
2. Save raw transcripts
3. Run **distill-transcript**
4. Summary final path: awaiting user ("In…")
5. Skills into topics + curriculums

## About this repo

Unaffiliated with any synth, plugin, or software vendor (including Key Solutions, Traveler, Blender, DJI, or any YouTube creator). Skills here are original distillations written as step-by-step procedures; product names are used only to describe what a skill applies to.
Raw YouTube transcripts, the intermediate `distilled/<video_id>/distilled.{md,json}` files (which embed transcript sentences), and vendored third-party prior-art repos are **kept out of this public repo** and stay local only (see `.gitignore`).

## Restore (new box or after /tmp or venvs are wiped)

```bash
git clone https://github.com/Bannon-github/skill-library.git /workspace/skill-library
cd /workspace/skill-library
./scripts/ensure_env.sh          # recreates mcp-server/.venv, .venv (pipeline), sample-lab/.venv, and /tmp/ytvenv symlink
./scripts/refetch_prior_art.sh   # optional: re-clone vendored prior-art at pinned commits
.venv/bin/python pipeline/build_prior_art_index.py   # optional: rebuild prior-art/index.json
```

Repoint the youtube-skills MCP server: its config spawns `/tmp/ytvenv/bin/python /workspace/skill-library/mcp-server/server.py`.
`ensure_env.sh` makes `/tmp/ytvenv` a symlink to `mcp-server/.venv`, so after running it the MCP works again with no config change.
(Alternatively point the MCP command straight at `/workspace/skill-library/mcp-server/.venv/bin/python` so it no longer depends on /tmp.)
Raw transcripts are not in git; re-fetch any you need with `.venv/bin/python pipeline/fetch_youtube_transcript.py <video_id>`.

## Sync

`./scripts/git_sync.sh` mirrors `/home/box/agent-data/workflows` into `bot-workflows/`, commits everything with a dated message, and pushes. See the header of the script for how push auth works.
