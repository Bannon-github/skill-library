---
name: Blender live work session
description: >-
  Use this when collaborating in a live Blender session on the user's PC: apply
  bpy scripts, screenshot the viewport, backup, and export glTF for the game.
---
# Blender live work session

## When
The user is in Blender (or about to open it) and you should apply changes while they talk, then inspect a viewport screenshot.

## Protocol
Workbench root (Windows): `Desktop/Cartoon World/blender-workbench/`
- Write commands to `inbox/pending.py` (full bpy script).
- To inspect only: write empty `inbox/capture.request`.
- Read results from `outbox/viewport.png` and `outbox/status.json`.
- Never overwrite the user's mesh unless the script they asked for does.

## Steps
1. Confirm Blender is open with Cartoon World Workbench addon (Launch Blender Workbench.bat). If not, launch it.
2. Write a small, undoable `inbox/pending.py`. Prefer one intent per file (add cube, set material, etc.).
3. Wait a few seconds for the addon timer (~1s) or ask the user to click Apply Pending.
4. Copy `outbox/viewport.png` to the box and inspect it. Also read `outbox/status.json`.
5. If wrong, tell them to Undo in the N-panel (or write a corrective script). Do not keep stacking failed scripts.
6. After a good change: backup is automatic; export GLB via the panel when they want it in the game (`export/` or `app/models/`).
7. Talk in chat about what you see in the screenshot; ask them to orbit if the camera angle hides the change.

## Success criteria
Command applied, screenshot shows the intended change, status.json ok, user can Undo.
