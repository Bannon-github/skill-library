---
name: Blender live work session
description: >-
  Use this when collaborating in a live Blender session: apply scripts,
  screenshot the Blender window (not camera), and verify object dimensions
  against targets before calling the work done.
---
# Blender live work session

## When
Collaborating in a live Blender session: apply bpy scripts, **screenshot the Blender window**, **verify dimensions against targets**, backup, export glTF.

## Capture rule (critical)
Inspect a **screenshot of the Blender application window** (what is on screen in USER/perspective view) — never a Camera view and never `bpy.ops.render.opengl` camera renders.
- Workbench writes `outbox/viewport.png` and `outbox/window.png` via `bpy.ops.screen.screenshot(full=True)` after forcing USER perspective if the view was CAMERA.
- Optionally also capture the OS window with a desktop screenshot of the Blender HWND when verifying from outside Blender.
- Keep a single Blender window.

## Protocol
Workbench root (Windows): `Desktop/Cartoon World/blender-workbench/`
- Write commands to `inbox/pending.py` (UTF-8 **without BOM**).
- Expected sizes: `inbox/targets.json` (feet).
- Capture only: empty `inbox/capture.request`.
- Read: `outbox/viewport.png` / `window.png`, `outbox/status.json`, **`outbox/dimensions.json`**.

## Steps
1. Confirm one Blender with Cartoon World Workbench.
2. Write `inbox/targets.json` for the brief.
3. Write `inbox/pending.py` (one intent). Prefer background `--python` if live inbox fails.
4. Trigger window screenshot; visually confirm the room is readable (not camera-in-wall).
5. **Must pass dimension audit:** every check in `dimensions.json` `ok: true`. Fix if not.
6. Backup/export via panel when shipping to the game.

## Success criteria
Applied script + clear **window** screenshot + **dimensions.json ok=true**.
