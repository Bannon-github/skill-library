# blender chocolate chip cookie model and render

Goal: Model a cookie with chips on a tray, assign materials, light with an Area light, frame camera, and render.

Source: https://www.youtube.com/watch?v=Ci3Has4L5W4

1. Object mode: add Cylinder as cookie base (Shift while drawing for 1:1 circle); scale Z flatter; right-click Shade Smooth; rename to cookie.
2. Shift+A → Mesh → UV Sphere for a chip; S scale; G then Z place into cookie; Shade Smooth; Shift+D duplicate many chips.
3. Add thin Cube tray (Shift for square); Tab Edit mode; face select top; I inset; Extrude region downward for tray lip; Tab Object mode; position under cookie.
4. Select cookie → Material Properties → New → set Base Color (eyedropper optional); switch Viewport to Material Preview.
5. Select one chip → set dark Base Color; Shift-select all chips ending on the colored one; Ctrl+L → Link Materials.
6. Material on tray (e.g. blue). Delete default light; Shift+A → Light → Area; raise Power (~800–850), lower temperature (~4000K); move/rotate to light cookie.
7. Numpad 0 camera view; N → View → Lock Camera to View; compose shot; uncheck Lock Camera to View.
8. Render Properties: choose Eevee or Cycles (GPU if available); Render → Render Image (F12); Image → Save As.

MCP: `skill://blender-chocolate-chip-cookie-model-and-render`
