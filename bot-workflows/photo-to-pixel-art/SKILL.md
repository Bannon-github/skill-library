---
name: Photo to pixel art
description: >-
  Master specification for the Photo to Pixel Art Coloring Game covering
  generation, gameplay systems, audio, packs, race mode, and iPad constraints.
---
# Photo to Pixel Art Coloring Game — Master Spec

## 1. Overview
Photo → Pillow pixel-art pipeline → paint-by-numbers HTML5 game (iPad Safari). Features: streak/octave audio, fade urgency, adaptive zoom, capped magic wand, entropy chaos, themed packs/levels, unlockable bonus skills, Timer Race vs AI.

## 2. Pixel art generation
Python + Pillow: load photo, flatten alpha, nearest-neighbor downscale, median-cut quantize, nearest-neighbor upscale, black grid lines, save PNG. Emit puzzle JSON (width, height, palette hex, grid indices, cellSize, optional pack/level/difficulty) and self-contained HTML game.

## 3. Game core
Numbered palette swatches; blank player board; tap/drag fill; number hints; reference toggle; completion when every cell matches reference.

## 4. Audio (Web Audio)
Per-pixel square blip (~85ms), pitch by color / streak scale; higher on correct. Row = 3-note sine arpeggio; column = different pattern. 8-step major scale to octave. Wrong thud; streak-reset descending blip. Unlock AudioContext on first touch (iOS).

## 5. Streak
Consecutive newly correct fills; 8 = octave target / max tone; score × multiplier from thresholds; idle timeout resets streak + sound.

## 6. Fade / lock
Active zone: grace then fade unfilled cells; full fade → lock/penalty; octave restores + unlocks next zone. Tunables: graceMs, fadeDurationMs, zoneRows, penalties.

## 7. Zoom
Adaptive start from viewport (~36px/cell, 8–14 visible). Zoom out per correct; octave burst; ease-in on reset. Recalc on rotate when streak idle.

## 8. Magic wand
BFS from tap on matching target colors (exact or RGB tolerance); cap 5/10/15 + radius; badge shows filled/cap. Each cell scores individually. Brush 1×1–5×5 also available.

## 9. Entropy
Level clock on first paint; empty cells flip to wrong palette colors; rate = lerp(start, max, t^rampPower); flash cue; no streak break. Tunables: rates, power, duration, flashMs.

## 10. Levels & packs
Themed packs (nature, animals/space, food, abstract); levels ramp colors/grid/timers; pack select; sequential unlock; pack clear unlocks next pack + bonus skill. `generate_packs.py` + `catalog.json` + hub `index.html`.

## 11. Bonus skills
Skills locked until pack complete (e.g. nature→rainbow, space→starfield). Bonus menu toggles unlocked only. Rainbow = canvas HSL cycle (not CSS filter).

## 12. Timer Race
Side-by-side boards + bars; AI speed / error / tick delay; win/lose/abort/rematch.

## 13. iPad
viewport user-scalable=no; touch-action none; pointer+touch; safe-area; portrait/landscape; 44px targets; no page pinch-zoom.

## 14. Stack
Python+Pillow offline gen; single HTML/JS/CSS; Web Audio; localStorage progression; no backend.
