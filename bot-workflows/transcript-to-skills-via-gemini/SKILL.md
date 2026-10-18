---
name: transcript-to-skills-via-gemini
description: >-
  Use this when turning a saved video transcript document into a markdown file
  of reusable AI skills and workflows using Gemini in the box browser.
---
# Turn a transcript into a skills file with Gemini

This is done by a computerUse subagent in the box browser, which is already signed in to Gemini.

1. Put the transcript in a document (a Google Doc, or a .md file you can upload). See the youtube-transcript-via-browser skill.
2. Open https://gemini.google.com/app and start a **New chat**.
3. Attach the transcript with the + button, choosing either the Google Doc from Drive or the uploaded file.
4. Send this prompt: "please analyze the contents of the attached document and generate a markdown document containing any useful skills or workflows that can be used by an ai."
5. Gemini opens the result in a document panel. Use **Export** and download it as Markdown (.md). It saves to ~/Downloads.
6. Rename the file after the source video, then review it. Keep only steps actually in the transcript, because Gemini can add things. Then file it in the skill library or pass it to the normal distill and quality checks.
7. Report the saved path and a one-line summary of the skills found.
