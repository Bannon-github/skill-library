# OBS Studio: set up a scene and record

Goal: Build an OBS Studio scene with audio and visual sources, configure output, and record or stream it.

Source: [OBS Studio - Tutorial for Beginners in 7 MINUTES! [ COMPLETE ]](https://www.youtube.com/watch?v=Muk9LfEWHeU) (Skills Factory)

1. Install OBS Studio and run the auto-configuration wizard (reopen it later from Tools > Auto-Configuration Wizard), choosing recording or streaming.
2. In Scenes click + to add a new scene; default system audio and microphone are detected automatically.
3. Add extra audio with Sources > + : Audio Input Capture for an external mic, Audio Output Capture for computer or other device audio. Adjust each level in the audio mixer meters.
4. Add visuals as needed: Color Source (background), Image, Image Slide Show, Media Source (video file), Text (font, size, color, opacity), Browser (a URL, display only), Window Capture (one app; it must not be minimized), Display Capture (whole screen), Game Capture (full-screen games, low overhead), Video Capture Device (webcam).
5. Arrange on the canvas: drag sources to move, drag the corner handles to resize, hold Alt while dragging a handle to crop. Anything in the striped area outside the canvas is cut off.
6. In the Sources list use the eye icon to hide or show, the lock to freeze position and size, and drag sources up or down to change stacking order. Use the gear/filters for properties and effects.
7. Open File > Settings: Stream (connect Twitch, YouTube, or Facebook if streaming); Output (recording path, format, quality, video and audio bitrate); Video (base canvas and output resolution, FPS); Hotkeys (start/stop recording and streaming).
8. Optionally enable Studio Mode to edit the Preview without touching the live Program, and push changes live with Transition (configure Quick Transitions).
9. Click Start Recording (or Start Streaming), use Pause if needed, then Stop.
10. Verify: open File > Show Recordings and play the file to confirm the video, audio sources, and levels are all present.

Batch: `2026-10-12-batch-01` · transcript: YouTube-provided (youtube-provided (yt-dlp timed text))
