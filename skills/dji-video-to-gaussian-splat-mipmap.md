# DJI drone video capture (GPS subtitles) to Gaussian splat in Mip-Map

Goal: Record a geo-referenced DJI drone video for splatting (Video Subtitles GPS on, white balance Auto then locked, 4K/30fps Normal color, ISO 100 and ~1/60 shutter, smooth overlapping multi-angle orbit), then import it into Mip-Map, extract frames using the subtitle GPS, run Gaussian splat reconstruction, and inspect/export the splat.

Sources (merged 2026-10-03):
- https://www.youtube.com/watch?v=mQ4EHUpXj9Q (from `dji-video-capture-for-gaussian-splat`)
- https://www.youtube.com/watch?v=mQ4EHUpXj9Q (from `process-drone-video-to-gaussian-splat-mipmap`)

1. Power on DJI drone and climb to subject height.
2. Switch to video mode; enable Video Subtitles (GPS per frame).
3. Set WB to Auto then lock it; set 4K 30fps Normal color.
4. Set ISO 100 and shutter ~1/60 (or lighting-appropriate).
5. Fly a smooth multi-angle orbit with overlap; land and copy the video.
6. Import the video into Mip-Map.
7. Extract frames using subtitle GPS when present.
8. Run Gaussian splat reconstruction.
9. Inspect and export the 3D splat.

Replaces: `dji-video-capture-for-gaussian-splat`, `process-drone-video-to-gaussian-splat-mipmap`

MCP: `skill://dji-video-to-gaussian-splat-mipmap`
