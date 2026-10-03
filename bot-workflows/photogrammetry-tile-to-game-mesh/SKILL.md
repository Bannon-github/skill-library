---
name: Photogrammetry tile to game mesh
description: >-
  Use this when turning drone/photo photogrammetry tiles into stylized game
  meshes that fit a chunk/LOD pipeline.
---
# Photogrammetry tile to game mesh

## When
Avata / drone / phone scans must become shippable game props, not raw multi-million-tri dumps.

## Steps
1. High-overlap capture → dense mesh export from photogrammetry tool.
2. Blender cleanup, meters, decimate/remesh, retopo heroes.
3. UV + bake albedo/normal/AO; posterize or paint-over for cartoon.
4. Build LOD0–LOD2 (+ optional impostor); consistent naming for runtime swap.
5. Export via Blender to glTF game-ready; compress scans harder than hand-painted art.
6. Place as chunk-local prop or simplified collider patch — never stream raw scans.
7. Validate: one hero tile at LOD0 in view vs VRAM budget.

## Success criteria
Reads as intentional stylized dressing; LOD swaps clean; cost like hand props.
