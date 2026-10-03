---
name: LOD streaming VRAM budget
description: >-
  Use this when enforcing draw-call and VRAM budgets on ~8GB GPUs while
  streaming a large cartoon world.
---
# LOD streaming VRAM budget

## When
Streaming open worlds on RTX-class ~8GB cards (or similar) where memory must stay flat.

## Steps
1. Set hard budgets (example: terrain tex ≤256 MB, props ≤800 MB, peak app ≤5 GB).
2. Enforce prop LODs; impostors/billboards beyond mid distance for trees/rocks.
3. Atlas or share materials; prefer InstancedMesh; merge static same-material batches where safe.
4. Stream by priority: heightmesh → splat/albedo → foliage → hero scans.
5. Unload-on-leave + dispose geometries/materials/maps; cap concurrent chunk loads; LOD hysteresis.
6. Profile GPU memory; add WebGPU frustum cull only with a WebGL2 fallback.
7. Re-test by circling the same region repeatedly (LOD thrash check).

## Success criteria
Extended session stays in VRAM envelope; leaving frees memory; frame time stable on loops.
