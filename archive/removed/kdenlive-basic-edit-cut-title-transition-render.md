# Kdenlive: basic edit, title, transition and render

Goal: Edit a video in Kdenlive from imported clips to a rendered MP4 with cuts, a title, an effect, and a transition.

Source: [LEARN KDENLIVE IN 15 MINUTES ~ Basic Video Editing Tutorial for Beginners](https://www.youtube.com/watch?v=V18BX15KbKs) (Chris' Tutorials)

1. Drag video (MP4/MKV), audio, or image files from your file manager into the Project Bin.
2. If the recording has several audio tracks and only one plays: select the clip, open Clip Properties > Properties, and pick the audio stream. To use two streams, right-click the clip > Duplicate, set the duplicate to the other stream.
3. Zoom the timeline and drag the first clip to the very start on video track 1/audio track 1. To drop only the second stream's audio, lock the video tracks first, drop the duplicate, then unlock.
4. Select the clips that belong together (click, then Shift+click) and right-click > Group Clips (Ctrl+G) so they move as one.
5. Cut: press X (razor tool) and click at the playhead to split a clip; press S to return to the selection tool.
6. Remove dull sections: select a piece and press Delete (leaves a gap, then right-click the gap > Remove Space), or right-click > Extract Clip to ripple-delete in one step.
7. Trim by dragging a clip's start or end edge (you can only extend into unused source footage). Move clips by dragging; to move up a track, right-click a track name > Insert Track first. Use the spacer tool to shift a clip and everything to its right together; snapping closes gaps.
8. Title: double-click the title clip in the bin, replace the text, center it horizontally and vertically, set font, outline (0-1 px to remove), and optional drop shadow (blur and x/y offset, e.g. 5/5); optionally save it as a title template, then click OK and drag it to video track 2 above the footage.
9. Effects: from the Effects panel drag an effect (e.g. Color > Sepia, or Mirror) onto a clip; select the clip and adjust or delete it in the Effect/Composition Stack. Effects apply per clip piece.
10. Transition: right-click a clip > Insert a Composition > Wipe; right-click > Edit Duration (e.g. 1 s). Copy it, paste and snap the copy to the other side of the cut, tick Revert on one so it fades out, and optionally choose another wipe method (e.g. checkerboard) on both.
11. Render: click Render, choose MP4, set the output file location, click Render to File and wait for the job queue to finish.
12. Verify: open the rendered file and check audio, title, cuts, and transitions play correctly.

Batch: `2026-10-12-batch-01` · transcript: YouTube-provided (auto-generated)
