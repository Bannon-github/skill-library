---
name: youtube-transcript-via-browser
description: >-
  Step 1 of the video-to-skills workflow. Use this when you need a YouTube
  video's transcript and automated download (yt-dlp/API) failed or was
  rate-limited: search YouTube in the browser, open the video, show the
  transcript, and save it to a Google Doc in Drive or a document on the box.
  Step 2 is transcript-to-skills-via-gemini.
---
# Get a YouTube transcript through the browser (step 1 of 2)

This is a fallback for when scripted transcript fetching fails. It's done by a computerUse subagent in the box browser.

1. Open https://www.youtube.com and type the exact search term into the search box, then press Enter. If you already have a video URL or ID, go straight to it.
2. Pick the video from the results by matching its title and channel to the target. Skip Shorts. Record the video URL, title, channel and duration.
3. On the watch page, expand the description ("...more"), then click **Show transcript**. The transcript panel opens on the right. If there's no Show transcript button, the video has no transcript: report that and stop. Never write a transcript yourself.
4. If there's a language menu in the panel, pick English (auto-generated is fine).
5. Select all of the transcript text in the panel and copy it.
6. Save it in one of two ways:
   - **Google Drive:** paste it into a new Google Doc titled with the video title.
   - **Box document:** paste it into a document on the box and save it as a `.md` file named after the video.
   Either way, put the video URL, title and channel at the top.
7. Report where it was saved and whether the transcript looked complete.

Next: run transcript-to-skills-via-gemini, attaching the Drive doc or uploading the box file.

## Tips
- Timestamps are optional; strip them when processing the text.
- If a sign-in or consent popup appears, dismiss it. Sign-in isn't needed to see transcripts.
