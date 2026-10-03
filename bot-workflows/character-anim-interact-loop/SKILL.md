---
name: Character anim interact loop
description: >-
  Use this when adding a playable or NPC character with locomotion clips and
  light interaction hooks in a browser world.
---
# Character anim interact loop

## When
Playable or NPC humanoid needs idle/walk/run plus a simple interact for quests/pickups.

## Steps
1. Source stylized humanoid; auto-rig via Mixamo or Rigify; get in-place idle/walk/run clips.
2. Merge clips into one GLB; prefer ≤4 bone influences.
3. Load with GLTFLoader; AnimationMixer + tiny anim graph (idle↔walk↔run, one-shot interact).
4. Drive root motion in code; snap feet to terrain height sample each frame.
5. Interact: raycast/proximity → gesture → emit onTalk/onPickup for game logic.
6. Many NPCs later: shared-pose instancing; don’t full-skin hundreds on CPU.
7. Match world style (toon/ramp or unlit trim).

## Success criteria
Walks on streamed terrain without sliding; clean transitions; ≥1 interact event reaches game logic.
