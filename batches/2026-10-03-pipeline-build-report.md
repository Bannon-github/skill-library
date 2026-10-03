# YouTube knowledge pipeline build — 2026-10-03

Matt asked for six connected skills: topic search, transcript extraction that gets past the barriers we've hit, a self-questioning router (including translated tracks), translation of foreign transcripts into English, term/phrase parsing into a graph, and a gap check against the library that drives new skills. All six are built as code, published as MCP skills, and chained by one router.

## What was built

| # | What it does (plain words) | Code | MCP skill (domain `agent-pipeline`) |
|---|---|---|---|
| 1 | Searches YouTube in several languages, filters by length, recency, views and how-to wording, and checks which results have a transcript before anything is downloaded | `pipeline/search_youtube_topics.py` | `youtube-topic-search-transcript-precheck` |
| 2 | Lists every transcript track and picks the best English: manual English → auto English in the original audio → YouTube's own translation (tlang=en) → English auto track of a YouTube AI-dub → original-language track + offline translation. Backs off on 429s; tells removed videos, disabled transcripts and IP blocks apart; keeps the original words next to any translation | `pipeline/fetch_youtube_transcript.py` (extended) | `youtube-show-transcript-track-ladder-fetch` |
| 3 | Router that asks itself explicit questions (Q0–Q7, plus cool-off, low-confidence-translation and upgrade checks), picks the next skill, and logs every answer | `pipeline/route.py` | `youtube-knowledge-pipeline-router` (orchestrator) |
| 4 | Free offline translator (argos-translate, own venv) with a sound-design glossary that fixes known mistranslations after translating, a garble detector, repetition-loop cleanup, and a confidence label | `pipeline/translate_transcript.py`, `pipeline/lexicons/translation_glossary.json` | `transcript-offline-machine-translate-glossary` |
| 5 | Turns a transcript into a graph: concepts, modules, params, values, tools, steps and repeated phrases, linked by sets / affects / precedes / part-of (+ mentions), each with timestamped evidence | `pipeline/extract_terms_graph.py`, `pipeline/lexicons/{synth,blender,crypto,sidehustle,drone}.json` | `transcript-domain-term-graph-extract` |
| 6 | Checks the graph against our 79 published skills and prior-art, merges it into a running knowledge graph, and drafts skill outlines only where there are real gaps | `pipeline/graph_gap_merge.py`, `knowledge/graph.json` | `knowledge-graph-gap-check-skill-outline` |

Also:
- Grok Bot workflow skill: `/home/box/agent-data/workflows/youtube-knowledge-pipeline/SKILL.md` (mirrored to `bot-workflows/`).
- `distill-transcript/SKILL.md` now says to start with the router and to distill only candidate outline spans. Translated sources must be checked against `transcript.orig.<lang>.txt`.
- `scripts/ensure_env.sh` now rebuilds `.venv-translate` (CPU torch, about 1.5 GB) and installs language packs for de, es, ja, fr, pt and it. Turn this off with `SKILL_LIBRARY_TRANSLATE=0`.
- yt-dlp calls now pass `--js-runtimes node`, so YouTube player challenges get solved without a deno install.
- `mcp-publish/index.json` now has 79 skills. I checked through the youtube-skills server: `list_skills` shows all 6 new ones, and `search_skills("router")` and `get_skill` both work.
- Prior-art check: the closest public equivalents are VoltAgent `youtube-skills`, `youtube-fetcher`, `last30days-skill`, `translate-book`, `azure-ai-translation-*` and `understand-anything`. Each of our skills states its delta in its `goal`. Novelty check: every new skill scored NOVEL (best overlap 0.10–0.15, and only against each other). Quality check: 6/6 clean.

## End-to-end tests (real videos)

| Video | Language situation | Route taken | Translation | Graph | Gaps | Outcome |
|---|---|---|---|---|---|---|
| A7q9L5wd7Mk "The Secret to Making MASSIVE Synth Pads – Vital" (Anima Audio) | English original; **only auto English** plus 7 AI-dub auto tracks (fr, de, hi, id, it, pt, es). The title shows in German in some searches | rank 2 `auto-target-original-audio` (the dub tracks were correctly skipped) | none | 79 nodes / 149 edges (30 steps, 16 params, 17 modules, 5 sets, 5 affects, e.g. envelope→cutoff, macro→mix, filter slope = 24 dB) | 42/44 terms covered; 0 gap relations; 2 phrase-only gaps | COVERED, no new skill. Yesterday's hunt had rejected this video as `transcript_unavailable`; the new fetcher got it |
| MH7YiOWQIhI "Síntesis de Pads ORQUESTALES en VITAL" | Spanish; one auto `es` track; English **only by translation** | rank 3 YouTube tlang got a **429** → rank 5 original + argos | machine:argos es→en, 35 segments, 0% garbled, confidence medium, 12 glossary hits | 26 / 27 | 17/19 covered; gap: `filter_drive` | COVERED; queued for a tlang upgrade |
| BqE9S27CZfY "Synthesizer programmieren E03 – ADSR-Hüllkurve" | German; one auto `de` track | first attempt **IP-blocked** (DEFER, queued); after cool-off: rank 3 tlang 429 → rank 5 | machine:argos de→en, 39 segments, medium | 26 / 29 | 15/18 covered; 3 phrase-only gaps (e.g. "volume automation") | COVERED (beginner ADSR is already in the library); queued for a tlang upgrade |
| kHWOIE4YTZ4 "週刊少年VITAL 2 #05: シネマティックシンセパッド" | Japanese; one auto `ja` track | first attempt IP-blocked (DEFER); then rank 3 tlang 429 → rank 5 | machine:argos ja→en, 30 segments, 6.7% garbled → **low confidence** (Q4b) | 43 / 53 | 28/28 terms covered; 2 gap relations (unison = 16 voices / 8 voices) | COVERED; queued for a tlang upgrade |
| EUlrANFXLs4 (the "missing captions" id) | n/a | Q2a: video unavailable | — | — | — | STOP, dropped from queue. The real cause is that the video was removed, not missing captions |

YouTube's own translation (tlang), checked separately: one direct request for kHWOIE4YTZ4 returned 238 English cues. They were far better than argos ja→en (for example "harmonic stretch … about 64%… use a function called spread"). The two pipeline attempts right before and after that request both got a 429 on tlang only. That's why the router queues `upgrade_to_tlang` instead of treating the machine translation as final.

Offline check of the candidate path: I ran the graph and gap steps (dry run, no KG write) on 13 locally saved transcripts that have no published skill. 2 produced outlines; the rest were covered:
- `_fHK9g9nwMM` (reverb types): `synth-decay-time-reverb-pre-delay-31-01`, built from specific decay and pre-delay values (4.49 s, 2 s, 750 ms…) that no current skill carries. Novelty: NOVEL (0.08).
- `oqNCqaQrQBg` (granular Vital soundscapes): `synth-macro-lfo-rate-wavetable-2-11` (macro → LFO rate, ±48 semitones random pitch). Novelty: NOVEL. But this video was deferred earlier as promo-heavy, so the distill gate should probably still reject it.

Both are outlines only. Nothing was distilled or published from them.

Knowledge graph after the tests: 4 videos, 70 nodes, 33 relations; 1 node and 2 relations not covered by any skill.

## Barriers: solved vs still open
Solved or handled:
- **429 / IP blocks.** Exponential backoff only on rate-limit errors. The router defers the video to `pipeline/queue/deferred.json` and stops contacting YouTube for the rest of that run (cool-off). A failed refetch no longer overwrites a good earlier transcript.
- **AI-dub tracks.** The original language comes from yt-dlp (`language` and the `-orig` track), so a German-original video's English auto track is labeled dub-derived and isn't treated as the creator's speech.
- **Auto vs manual tracks.** These are explicit rungs in the ladder and recorded in `meta.json`.
- **Removed or unavailable videos.** Classified and dropped instead of retried.
- **Venv wipes.** `ensure_env.sh` also rebuilds the translation venv and language packs.
- **Broken translator package.** argos es→en 1.9 produced garbage, so it's pinned to 1.0. Pre-injecting English terms also broke argos, so the glossary only corrects after translating.

Still open:
- **YouTube's translation endpoint (tlang) is throttled much harder than plain tracks from this box's IP.** All three non-English tests fell back to argos. The upgrade queue retries later, but it can stay blocked for a while. A proxy (`YT_TRANSCRIPT_PROXY`) or a cookies file (`YTDLP_COOKIES`) would fix it, but only if Matt chooses to set one up.
- **Japanese machine translation is weak** (low confidence). Terms are good enough for the graph, but numbers and steps from ja need the original or YouTube's translation.
- **Whole-IP blocks** ("Sign in to confirm you're not a bot") hit both the API and yt-dlp for 10–30 minutes after bursts. Small batches with gaps between them are the only fix without a proxy.
- **Videos with no transcript at all:** the router flags ASR (Whisper) as a last resort and stops. It never runs it unless Matt asks.
- The graph extractor is lexicon-based. It's strongest on synth, while the Blender, crypto, side-hustle and drone lexicons are smaller. Phrase nodes show where to grow them.

## Files
- Code: `pipeline/{search_youtube_topics,fetch_youtube_transcript,translate_transcript,route,extract_terms_graph,graph_gap_merge}.py`, `pipeline/lexicons/*.json`, `pipeline/requirements-translate.txt`, `scripts/ensure_env.sh`
- Skills: `mcp-publish/skills/{youtube-topic-search-transcript-precheck,youtube-show-transcript-track-ladder-fetch,youtube-knowledge-pipeline-router,transcript-offline-machine-translate-glossary,transcript-domain-term-graph-extract,knowledge-graph-gap-check-skill-outline}.json`
- Workflow: `/home/box/agent-data/workflows/youtube-knowledge-pipeline/SKILL.md`. Updated: `/home/box/agent-data/workflows/distill-transcript/SKILL.md`
- Per-video logs: `raw/<id>/route.json`, `raw/<id>/meta.json` (committed); `raw/<id>/graph.json`, `gaps.json`, `translation.json`, transcripts (local only, gitignored)
- Knowledge graph: `knowledge/graph.json` (references only, no quote text)
- Queues and logs (local): `pipeline/queue/deferred.json` (holds `upgrade_to_tlang` for the 3 non-English tests), `pipeline/logs/route.jsonl`
- Candidate outlines (local): `distilled/_fHK9g9nwMM/candidates/`, `distilled/oqNCqaQrQBg/candidates/`
