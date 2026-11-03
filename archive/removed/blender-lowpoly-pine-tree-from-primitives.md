# blender low poly pine tree from primitives

Goal: Build a simple low-poly pine tree using cylinder and circle meshes with extrude/scale/duplicate.

Source: https://www.youtube.com/watch?v=peSv5IT5Ve4

1. Delete unneeded default mesh if present.
2. Shift+A → Mesh → Cylinder; in Add Cylinder adjust vertices down (e.g. 8) for low poly.
3. Tab Edit mode; scale trunk; select top face, move up, S scale for trunk taper; optional Shade Smooth Auto Smooth.
4. Shift+A → Mesh → Circle (e.g. 12 sides).
5. Edit mode, edge select; E then Z to extrude on Z; S scale; Ctrl+R loop cuts and scale for foliage layers.
6. L select linked pieces as needed; Shift+D duplicate foliage layers; R/S (and R then Z) to vary layers.
7. Stack scaled/rotated circle extrusions above the trunk for a pine silhouette.

MCP: `skill://blender-lowpoly-pine-tree-from-primitives`
