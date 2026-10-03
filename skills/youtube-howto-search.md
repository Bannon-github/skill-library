# youtube-howto-search

**Goal:** For a user-supplied topic, find how-to YouTube videos and report title, URL, and whether a YouTube **Show transcript** exists — without extracting yet.

## Steps
1. Take the topic string from the user.
2. Search YouTube for how-to / tutorial videos on that topic.
3. For each result, check **transcript** availability (the Transcript panel under video info — manual or auto track) without saving the full body yet.
4. Return a list: title, link, transcript status (available / missing).
5. Stop and wait for user confirmation before stage save-raw — unless Matt has authorized ongoing distillery runs.

## Note
Say **transcript**, not captions. Fetch later via `pipeline/fetch_youtube_transcript.py`.
