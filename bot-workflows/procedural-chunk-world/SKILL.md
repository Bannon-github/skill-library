---
name: Procedural chunk world
description: >-
  Use this when standing up or extending a browser cartoon open-world ground
  plane with seeded chunks, streaming, and distance LOD.
---
# Procedural chunk world

## When
Browser / Three.js (or similar) cartoon open world that needs infinite-feeling terrain without loading everything.

## Steps
1. Define chunk size (e.g. 32–128 units), world seed, and height scale for a stylized silhouette.
2. Generate height per chunk with layered FBM + light domain warp; derive slope and a cheap moisture proxy for biomes.
3. Classify biomes with simple thresholds (beach / grass / forest / rock / snow); output splat or vertex-color masks.
4. Build mesh (or GPU-displaced grid) per chunk; add edge skirts and LOD hysteresis to avoid cracks and thrashing.
5. Spatial index; each frame: select LOD by camera distance, prefetch along velocity, unload-on-leave with LRU.
6. Stylized ground material; instance foliage from biome density maps.
7. Smoke-test a walk/fly loop; confirm no unbounded memory growth and stable frame time.

## Success criteria
Player can traverse large stylized terrain with roughly constant resident chunks, visible LOD without cracks, and unload reclaiming memory after leaving an area.
