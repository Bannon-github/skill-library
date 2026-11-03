# blender mug with solidify subsurf and loop cuts

Goal: Block a coffee mug from a cylinder using Edit mode, Solidify, Subdivision Surface, and Ctrl+R loop cuts (from Blender Guru beginner series).

Source: https://www.youtube.com/watch?v=z-Xl9tGqH14

1. Add/position cylinder as mug; Tab Edit mode; shape walls (scale loops) toward a mug silhouette.
2. Add Solidify modifier for wall thickness; adjust thickness non-destructively.
3. Add Subdivision Surface; raise Viewport levels carefully; note how unchecked edges become overly round.
4. Ctrl+R add loop cuts near rim/base to hold shape under Subsurf; slide and confirm.
5. Use reference image (Add Image Reference); clear bad rotation, set 90° with Ctrl-snap; scale to match mug.
6. Before handle extrudes: Apply Solidify so inner/outer walls are real mesh; then extrude handle geometry from an appropriate face.

MCP: `skill://blender-mug-solidify-subsurf-loopcut`
