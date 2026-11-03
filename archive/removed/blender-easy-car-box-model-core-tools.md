# blender easy car box model with core tools

Goal: Block out a simple car using scale-axis locks, loop cut, extrude, inset, apply transforms, and duplicated wheels.

Source: https://www.youtube.com/watch?v=nESaz92SJ0w

1. Select cube; S then Y stretch length; S then Z flatten height to a car-body proportion.
2. Tab Edit mode; A select all; Ctrl+R loop cut (scroll for 2 cuts); place cuts; wireframe view to move side verts for body shape.
3. Face select roof region; E extrude upward; pull windshield verts back on Y for rake.
4. Object mode Ctrl+A Apply All Transforms; Edit mode again; select window faces; I inset then E extrude inward for glass recesses.
5. Object mode; Shift+A Mesh → Cylinder for a tire; S and S+Z to tire proportions; Edit mode I/E for hub detail.
6. Front orthographic view; R rotate tire with Ctrl for snapped angle; rename objects; duplicate wheels to four corners.

MCP: `skill://blender-easy-car-box-model-core-tools`
