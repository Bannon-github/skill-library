---
name: Blender to glTF game-ready
description: >-
  Use this when exporting Blender 5.x props or characters to compressed .glb for
  Three.js cartoon PBR/toon.
---
# Blender to glTF game-ready

## When
Authoring in Blender and shipping assets into a browser or engine via glTF Binary (.glb).

## Steps
1. Author with Principled BSDF metal/rough; Non-Color for data maps; avoid unsupported node graphs.
2. Apply scale/rotation and modifiers; real-world meters; +Y up on export.
3. For repeats, share mesh data / enable GPU Instances (EXT_mesh_gpu_instancing) when instances share one mesh.
4. Export glTF Binary (.glb): Apply Modifiers on, UVs/Normals on, Tangents if normal maps, materials Export.
5. Post-process with gltf-transform: validate → optimize → resize textures → meshopt OR Draco (not both) → KTX2 (ETC1S color, UASTC normals).
6. In Three.js wire GLTFLoader + MeshoptDecoder and/or DRACOLoader + KTX2Loader.detectSupport(renderer).
7. Verify materials, hierarchy, and optional unlit/toon remap for cartoon look.

## Success criteria
GLB loads cleanly; size/decode acceptable; no double-compression; materials look intentional.
