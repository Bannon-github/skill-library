# Inkscape Trace Bitmap: convert a JPEG/PNG to vector

Goal: Convert a raster image (JPEG/PNG) into scalable vector paths in Inkscape, choosing single-scan or multi-color tracing.

Source: [Inkscape Trace Bitmap Tutorial: How to Convert Jpeg | PNG | Raster to Vector Image](https://www.youtube.com/watch?v=a8SAAJBo3yU) (IronEcho Design)

1. Pick a source image with a plain, neutral background (royalty-free sources like Pexels work); downscale it to under about 10 MB if your computer is slow.
2. Import or open the image in Inkscape and select it.
3. Open Path > Trace Bitmap. Start on Single scan > Brightness cutoff with defaults: threshold about 0.45, speckles 2, smooth corners 1.0, optimize 0.20.
4. Click Update to preview, then OK. Drag the new vector off the original to compare.
5. If dark areas clog (e.g. too much black around a face), reselect the image and lower the threshold (try 0.43, 0.35, 0.25), updating and comparing each result; optionally composite parts of several traces.
6. For hard-edged objects (cars, buildings, still life) try Single scan > Edge detection around 0.50; it gets very busy on organic subjects.
7. For a fast color result try Autotrace (e.g. error threshold 2.0, filter iterations 5), Update, OK.
8. For a detailed color vector use Multiple scans > Colors: start with 8 scans, enable Smooth and Stack, enable Remove background, keep the speckle/corner/optimize defaults, Update, OK. More scans add layers and detail but take longer; save your file before going to 20+ scans because Inkscape may crash.
9. Double-click into the traced group to isolate individual color layers (black, gray, orange, etc.) and keep, recolor, or delete them.
10. Verify: zoom far in and confirm edges stay crisp (no pixelation), then save as SVG.

Batch: `2026-10-12-batch-01` · transcript: YouTube-provided (auto-generated)
