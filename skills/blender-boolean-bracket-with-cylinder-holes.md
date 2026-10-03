# blender boolean bracket with cylinder holes

Goal: Model a simple mm bracket plate and cut bolt holes with cylinder Boolean Difference.

Source: https://www.youtube.com/watch?v=8_0RptMbhe0

1. Optional: delete Camera and Light (right-click Delete) to declutter.
2. Set cube dimensions for the plate (e.g. 100 mm wide, 12 deep, 3 thick); rename to bracket.
3. Add → Mesh → Cylinder; before confirming, open Add Cylinder panel and raise Vertices (e.g. 256).
4. Size cutter diameter with clearance (e.g. 5.6 mm) and height taller than plate (e.g. 10 mm); rename hole cutter.
5. Duplicate cutters, position along plate (set Location numerically); Shift-select cutters → Join into one cutter object.
6. Select bracket → Modifiers → Add Boolean → Object = hole cutter, Operation Difference → Apply.
7. Delete cutter object(s); verify holes. Tab Edit mode; Face select; E extrude an edge/face to form an L-bracket flange as needed.
8. Optional: enable MeasureIt add-on (Edit→Preferences→Add-ons) to measure hole diameters in mm.

MCP: `skill://blender-boolean-bracket-with-cylinder-holes`
