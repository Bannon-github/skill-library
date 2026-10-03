# YouTube transcript source

Matt’s rule: use the **Show transcript** panel from the video information section — not “captions” as the deliverable.

```
Video → description / ⋯ → Show transcript / Transcript
```

## Fetch

```bash
python /workspace/skill-library/pipeline/fetch_youtube_transcript.py <video_id> [<video_id>...]
```

Outputs under `raw/<video_id>/`:
- `transcript.txt` — panel-style timestamped lines
- `raw.txt` / `raw` — continuous prose for distillation
- `meta.json` — provenance (`source_ui: youtube-show-transcript`)

Primary path: `youtube-transcript-api` (same family as the Transcript panel).  
Fallback: yt-dlp timed text converted into transcript files (`.srt`/`.vtt` are deleted after conversion).
