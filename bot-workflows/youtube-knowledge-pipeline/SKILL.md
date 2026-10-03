---
name: YouTube knowledge pipeline
description: >-
  Use this when Matt wants to learn a topic from YouTube how-to videos end to end:
  search for videos, pull the Show transcript (with translated or machine-translated
  English when the video isn't in English), build a term/relation graph, check it
  against the existing skill library and knowledge graph, and outline new skills
  only for the gaps. Runs a self-questioning router that logs every decision.
---
# YouTube knowledge pipeline (router)

One command walks the whole chain and decides each branch out loud:

```bash
cd /workspace/skill-library
bash scripts/ensure_env.sh                       # venvs (.venv, .venv-translate, mcp-server/.venv)
.venv/bin/python pipeline/route.py --topic "cinematic pad sound design" --langs en,de,es --max 3
.venv/bin/python pipeline/route.py VIDEO_ID [VIDEO_ID ...]       # known ids
```

## The chain (each step is an MCP skill in youtube-skills)
| # | Skill id | Script |
|---|----------|--------|
| 1 | `youtube-topic-search-transcript-precheck` | `pipeline/search_youtube_topics.py` |
| 2 | `youtube-show-transcript-track-ladder-fetch` | `pipeline/fetch_youtube_transcript.py` |
| 3 | `youtube-knowledge-pipeline-router` (orchestrator) | `pipeline/route.py` |
| 4 | `transcript-offline-machine-translate-glossary` | `pipeline/translate_transcript.py` (in `.venv-translate`) |
| 5 | `transcript-domain-term-graph-extract` | `pipeline/extract_terms_graph.py` |
| 6 | `knowledge-graph-gap-check-skill-outline` | `pipeline/graph_gap_merge.py` |
| → | `distill-transcript` + gates | `quality_check_skill.py`, `novelty_check_skill.py` |

## Questions the router asks (and what it does)
- **Q0** Env importable? no → `scripts/ensure_env.sh`.
- **Q1** Transcript already saved? yes → reuse it.
- **Q2** Track ladder: manual EN → auto EN in the original audio → YouTube-translated (tlang=en) → EN auto of an AI-dub track → original track + offline machine translation.
  - **Q2a** Removed/private/age-gated → STOP, drop it.
  - **Q2b** 429 / IP-blocked after backoff → DEFER (`pipeline/queue/deferred.json`), retry later. Only Matt sets `YT_TRANSCRIPT_PROXY` / `YTDLP_COOKIES`.
  - **Q2c** No transcript track at all → STOP and *flag* ASR as a last resort. Don't run Whisper unless Matt asks.
  - **Q2d** Translation failed or garbled → STOP; the original words are kept.
- **Q3** Usable (≥150 words, not music-only)? no → REJECT.
- **Q4** Is the English a translation? yes → label it; the distiller cross-checks `transcript.orig.<lang>.txt`.
- **Q5/Q6** Domain lexicon matched (≥8 hits)? Build `raw/<id>/graph.json`.
- **Q7** Gaps vs library? yes → outlines in `distilled/<id>/candidates/` go to distill-transcript → quality → novelty. no → COVERED (KG still updated).

Logs: `raw/<id>/route.json`, `pipeline/logs/route.jsonl`. Knowledge graph: `knowledge/graph.json` (refs only, no quote text).

## Rules
- Say **transcript** (Show transcript panel), not captions. Never invent transcript text.
- Outlines are not skills; publish only after distill + quality + novelty pass (plus the finance-risk rules for crypto/side hustle).
- Machine-translated sources must say so in the skill's `source` and constraints.
- Raw transcripts, graphs and outlines stay local (gitignored); the public repo gets code, lexicons, skills and the KG.
- Retry deferred ids later with `.venv/bin/python pipeline/route.py $(jq -r '.deferred[].video_id' pipeline/queue/deferred.json)`.
