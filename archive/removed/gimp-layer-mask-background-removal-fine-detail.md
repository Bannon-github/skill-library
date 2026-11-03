# GIMP layer-mask background removal for hair and fine detail

Goal: Remove a background behind hair or fine detail when subject and background contrast strongly.

Source: [5 Ways To Remove A Background with GIMP](https://www.youtube.com/watch?v=lOzSiOIipSM) (Logos By Nick)

1. Confirm the image has strong subject/background contrast; this method fails otherwise.
2. Duplicate the layer.
3. On the duplicate: Colors > Saturation, scale all the way down, OK.
4. Colors > Curves: drag the top and bottom nodes until the subject is mostly black and the background mostly white.
5. Colors > Invert, then Edit > Copy Visible.
6. Hide the duplicate (eye icon).
7. Right-click the original layer > Add Layer Mask with default settings > OK.
8. Edit > Paste, then click the anchor icon to anchor the paste into the layer mask (black stays visible, white becomes transparent per the video's result).
9. Paint on the mask with a white brush to fix areas that were wrongly removed, then export as PNG.

Batch: `2026-10-05-batch-01` · transcript: YouTube-provided (auto-generated)
