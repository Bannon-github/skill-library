# blender low poly character scene prep

Goal: Prepare a Blender 4+ scene for stylized low-poly character work: Eevee, Standard view transform, incremental saves, image references, Rigify metarig scale.

Source: https://www.youtube.com/watch?v=Use9T2IX1XE

1. Render Properties: Engine Eevee; ensure Ambient Occlusion, Bloom, Screen Space Reflections, Motion Blur off.
2. Color Management → View Transform → Standard.
3. Delete default cube if desired; File → Save As into a project folder; use Ctrl+S often and Ctrl+Alt+S for incremental saves.
4. Shift+A → Image → Reference; import front and side images.
5. Edit → Preferences → Add-ons → enable Rigify; Shift+A → Armature → Human Meta-Rig for human scale.
6. Select both references; front ortho view; Alt+G/Alt+S/Alt+R reset as needed; R then X 90 to stand images up.
7. G/S and axis locks (G+Z, G+Y, R+Z 90) to align feet to ground and match metarig height; set reference Opacity ~0.5.

MCP: `skill://blender-lowpoly-character-scene-prep`
