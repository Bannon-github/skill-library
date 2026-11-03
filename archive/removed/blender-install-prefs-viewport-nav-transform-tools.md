# Blender first launch: install, preferences, viewport navigation, Move/Rotate/Scale

Goal: Install Blender, set useful preferences (Resolution Scale, GPU/CUDA Cycles device, Undo Steps, Save Preferences), navigate the viewport with MMB orbit / Shift+MMB pan / scroll zoom and numpad or Alt+MMB orthographic snaps, then transform the default cube with the Move/Rotate/Scale tools and G/R/S hotkeys with X/Y/Z axis locks.

Sources (merged 2026-10-03):
- https://www.youtube.com/watch?v=Ci3Has4L5W4 (from `blender-install-preferences-and-viewport-basics`)
- https://www.youtube.com/watch?v=98qKfdJRzr0 (from `blender-beginner-three-tools-and-viewport-nav`)
- https://www.youtube.com/watch?v=peSv5IT5Ve4 (from `blender-viewport-navigation-mmb`)

1. Download Blender from blender.org and install for your OS; open and click outside splash to dismiss.
2. Edit → Preferences → Interface: adjust Resolution Scale (e.g. 1.25) if UI is tiny/huge.
3. Preferences → System: enable CUDA/GPU Cycles device if available; raise Undo Steps (e.g. 100); Save Preferences.
4. Without a middle mouse button / on trackpad: enable Emulate 3 Button Mouse or use trackpad alternatives.
5. Scroll the middle mouse wheel to zoom in and out.
6. Click and drag the middle mouse button to orbit around the object.
7. Hold Shift and middle-mouse-drag to pan the scene. Optional: viewport gizmo orbit/zoom/pan.
8. If you have a numpad: 1 front orthographic, 3 right, 7 top, 9 bottom.
9. Without a numpad: hold Alt, middle-mouse-drag toward the desired axis to snap orthographic views. Or click gizmo axes for axis views.
10. Activate Move tool; drag RGB handles to move the cube.
11. Activate Rotate tool; drag handles to rotate.
12. Activate Scale tool; drag the white uniform handle to scale on all axes.
13. Use hotkeys G, R, S for Move/Rotate/Scale; axis-constrain with X/Y/Z; Tab for Edit mode.

Replaces: `blender-install-preferences-and-viewport-basics`, `blender-beginner-three-tools-and-viewport-nav`, `blender-viewport-navigation-mmb`

MCP: `skill://blender-install-prefs-viewport-nav-transform-tools`
