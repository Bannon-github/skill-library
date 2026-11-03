---
name: course-audio-narrator
description: >-
  Use after course-script-writer (or with any course-studio script) to pick a
  stock ElevenLabs voice, render a natural single MP3 with chapters and a soft
  music bed, QA it to 9–11 minutes, and deliver it.
---
# Course audio narrator

Tools in `/workspace/course-studio/`, run with `P=/home/box/audio-tools/bin/python`. Full reference copy: `/workspace/course-studio/skills/course-audio-narrator/SKILL.md`.
- `render_course.py`: per-paragraph TTS with previous/next text for flow, one voice and settings, section pauses, optional ducked synth pad bed, two-pass loudnorm, ID3 chapters plus `.chapters.txt` and `.chapters.json`. Checks quota first; caches clips in `.cache/`.
- `pick_voice.py`: lists and scores stock voices.
- `qa_course.py`: duration, loudness, true peak, long silences, chapters.
- Key is the box secret `ELEVENLABS_API_KEY`. Never print it. Stock voices only, never clone a real person.

## 1. Preflight
`$P render_course.py <script.md> /tmp/dry.mp3 --voice <id> --dry-run` prints words, characters and quota left (aborts if short). 10 minutes is about 8,500 characters; budget twice that for re-renders.

## 2. Pick the voice
`$P pick_voice.py --gender male --age middle_aged --accent american --energy medium --use conversational`
- Warm casual teacher (default): Chris `iP95p4xoKVk53GoZ742B`
- Veteran professor: Bill `pqHfZKP75CvOlQylNhV4`
- Polished deadpan: Eric `cjVigY5qzO86Huf0OWal`
- Hype young coach: Liam `TX3LPaxmHKxFdv7VOQHJ`
- British: George or Daniel. Female: `--gender female`.
Note the voice and one line on why.

## 3. Render
```bash
$P render_course.py /workspace/share/courses/<slug>.md /workspace/share/courses/<slug>.mp3 --voice <id> --speed 0.94 --para-gap 0.75 --section-gap 1.4
```
Defaults: `eleven_multilingual_v2`, stability 0.45 (0.35 livelier, 0.6 calmer), similarity 0.75, style 0.3. `--no-music` skips the bed. Keep speed 0.9–1.1; fix length with words.

## 4. QA
`$P qa_course.py /workspace/share/courses/<slug>.mp3 --min 9 --max 11`
- Duration 9–11 min; about 160 words per minute to add or cut.
- Loudness about −16 LUFS (−18 is OK for speech), true peak ≤ −1.5 dBTP.
- Silences over 3 s only at section breaks; otherwise tweak and re-render that paragraph.
- Spot-check first and last words of 3 paragraphs: `ffmpeg -ss <t> -t 20 -i <slug>.mp3 /tmp/check.wav`.
- Mispronounced terms: respell phonetically. Monotone: lower stability or shorten sentences.

## 5. Deliver
Attach `<slug>.mp3` (10 min ≈ 9.5 MB); keep `<slug>.md` and `<slug>.chapters.txt` beside it. Report duration, voice and why, characters used, and chapters.
