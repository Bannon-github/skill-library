---
name: course-script-writer
description: >-
  Use when asked to make a spoken audio course, lesson, or explainer (about 10
  minutes) on any topic: research it, pick a teaching persona, and write an
  ear-first script for course-audio-narrator.
---
# Course script writer

Output: `/workspace/share/courses/<slug>.md` in the course-studio script format (see `/workspace/course-studio/README.md`). Full reference copy: `/workspace/course-studio/skills/course-script-writer/SKILL.md`.

## 1. Pin the brief
- Topic, listener level, why they care. Don't ask unless truly ambiguous.
- 10 minutes = **1,550–1,650 spoken words** (stock voices read about 160 wpm; 1,582 words gave 9:57 at speed 0.94).
- Slug: lowercase-hyphen.

## 2. Research and cite
1. WebSearch 2–4 queries ("<topic> explained", "common mistakes", "best practices <year>").
2. Open 3–5 reputable sources with WebFetch: a reference, 1–2 practitioner sources, and optionally a teacher's YouTube transcript via `/workspace/skill-library/pipeline/fetch_youtube_transcript.py <id>`.
3. Check the skill library: `rg -il "<topic>" /workspace/skill-library/skills`.
4. Note 8–12 facts, each with a URL you actually opened. Paraphrase; never quote more than a short phrase.
5. List sources in an HTML comment at the top (not spoken).

## 3. Pick a persona
Demo-then-explain (casual, curious), formula + checkpoint (memorable rule, "okay?" checks), deadpan essay (provocative question, dry humor), or hype coach (energetic, anti-jargon). Note it in the comment; the narrator voice will match it.

## 4. Structure
```
# Title
<!-- persona, sources, target words -->
[music: intro]
## Welcome            ~180 w  hook + promise + 3–4 goals in a sentence
[pause 1.5]
## Part one: ...      ~280 w  explain, example, quick check
[pause 1.5]
## Part two: ...      ~320 w
[pause 1.5]
## Part three: ...    ~320 w
[pause 1.5]
## Part four: ...     ~260 w  mistakes or when not to
[pause 1.5]
## Recap and your next step  ~200 w  4–5 sentence recap + ONE action
[music: outro]
Sign-off line.
```
- One paragraph per TTS request; keep each under about 900 characters.
- Quick check: "Quick check. <question>? Think about it. The answer is ... because ..."

## 5. Write for the ear
- Short sentences (8–18 words), contractions, signposts.
- No bullets read aloud; turn lists into sentences.
- Spell out numbers, symbols and units as spoken ("four to one", "E Q", "fifty percent"). No URLs, parentheses or slashes.
- Same term every time for technical words; one idea per paragraph; a concrete example per module.
- No health, financial or legal claims beyond the sources.

## 6. Self-check
```bash
cd /workspace/course-studio
/home/box/audio-tools/bin/python render_course.py /workspace/share/courses/<slug>.md /tmp/dry.mp3 --voice iP95p4xoKVk53GoZ742B --dry-run
```
Fix length with a worked example, never filler. Then hand off to course-audio-narrator.
