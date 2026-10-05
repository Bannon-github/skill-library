# Tune Z offset for a good first layer

Goal: Get a first layer that sticks and looks smooth across the bed.

Source: [How to get PERFECT First Layers on Your 3D Printer!!](https://www.youtube.com/watch?v=Wywd2-MqBLw) (3D Musketeers)

1. Level the bed first. If one side squishes and the other has gaps, square the X and Z axes (e.g. on dual-Z machines, rest the gantry on two identical objects such as same-brand soup cans), then relevel.
2. Run a first-layer or Z-offset test print and live-adjust Z offset from the printer while it prints.
3. Too far: lines do not touch, surface is rough, poor adhesion. Too close: ridges between lines. Target: smooth, glass-like, touching lines (slightly closer is acceptable on textured plates; avoid over-squish on glass).
4. Keep the slicer global Z offset at 0 and set the offset on the printer; only use the slicer offset if the printer cannot adjust it, carefully.
5. If the bed wheels are maxed and the nozzle still cannot get close enough on a limit-switch printer, loosen and lower the Z limit switch a very small amount, tighten the bed springs several turns first so the nozzle cannot crash, then relevel (paper method or leveling tool).
6. If it looks right but will not stick, clean the build plate with isopropyl alcohol on a paper towel to remove skin oils.
7. Check the first layer across the whole plate. On a warped bed without a probe, get the center right; otherwise replace the bed and consider an auto-leveling probe, hard-mounting the bed (silicone spacers or nylon lock nuts) when adding a probe.
8. To release a part stuck to glass, let the plate reach room temperature, then chill it (borosilicate glass only; ordinary plate glass can shatter).

Batch: `2026-10-05-batch-01` · transcript: YouTube-provided (auto-generated)
