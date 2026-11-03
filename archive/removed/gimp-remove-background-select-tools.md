# GIMP background removal with selection tools

Goal: Delete an image background to transparency using fuzzy select, select by color, paths, or foreground select.

Source: [5 Ways To Remove A Background with GIMP](https://www.youtube.com/watch?v=lOzSiOIipSM) (Logos By Nick)

1. Right-click the image layer > Add Alpha Channel (if greyed out, it already has one).
2. Pick the method: fuzzy select for photos with a clear subject/background split; select by color for vector or flat illustrations; paths for the most accurate crisp edge; foreground select for subjects with fine detail like hair.
3. Fuzzy select: enable antialiasing, feather edges and draw mask; click-hold on the background and drag down to raise the threshold or up to lower it; release and press Delete. Repeat for remaining areas.
4. Select by color: enable antialiasing and draw mask (feather edges for photos, off for illustrations); click-hold on the background color, drag to tune the threshold, release, press Delete.
5. Paths: click points around the subject edge, drag to curve segments and adjust handles; to continue, click the last point first; close with Ctrl+click on the first point; press Enter to make a selection; Select > Invert; press Delete.
6. Foreground select: draw a rough outline around the subject and press Enter; brush over the subject interior (resize brush with [ and ]) without hugging the edges; toggle Preview to check; press Enter to make the selection; Select > Invert; press Delete.
7. Check the transparency checkerboard and export as PNG to keep transparency.

Batch: `2026-10-05-batch-01` · transcript: YouTube-provided (auto-generated)
