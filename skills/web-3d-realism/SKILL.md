---
name: web-3d-realism
description: Make a three.js / web 3D game look realistic instead of "Minecraft boxes" - free CC0 PBR models and textures from Poly Haven, HDRI sky lighting, soft shadows, ambient occlusion, rounded geometry, a procedural grime/dirt shader for cleaning games, asset compression and publishing limits. Use for "більш реалістично", "графіка як у Steam-іграх", "не квадратні об'єкти", "realistic graphics", "better 3D models".
---

# Realistic web 3D (three.js) - what worked on Junk Lot Tycoon v0.3

## 1. Real models instead of boxes
- Poly Haven (polyhaven.com) = CC0, photoreal PBR models with real-world scale in metres. API:
  `https://api.polyhaven.com/assets?t=models` (list), `https://api.polyhaven.com/files/<id>` -> `gltf.1k.gltf.url` + `include` files.
  Same API has textures (`t=textures`: Diffuse + nor_gl jpg) and HDRIs (`hdri.1k.hdr`). Credit them anyway.
- Pipeline (`fetch.py` pattern): download 1k gltf + bin + textures -> resize textures to 512 px (PIL, quality 82) ->
  `gltf-transform copy` to glb -> `gltf-transform simplify --ratio 0.5 --error 0.002` (0.15 for heavy plants/sets).
  Check sizes: some assets are huge (fir_tree_01 was 290 MB) - skip vegetation, make stylised trees from icospheres.
- Many assets are SETS (several suitcases/cans in one file): list top-level nodes with bounds and keep one by centre x (`keepX`).
  Some are in wrong units (steel_frame_shelves_01 = 10x) - check bounds and scale.
- Normalise every model at load: optional rotate (lay flat), centre x/z, bottom at y = 0, minimum size ~0.28 m so it can be aimed at.

## 2. Lighting & post that make it look "Steam-like"
- `renderer.toneMapping = ACESFilmicToneMapping`, exposure ~0.95, sRGB output, `PCFSoftShadowMap`.
- HDRI as `scene.environment` + `scene.background` (PBR reflections are the biggest jump in realism).
- One DirectionalLight sun with shadows (2048 map, bias -0.0004, normalBias 0.03, ortho box covering the play area),
  low HemisphereLight (0.35), small warm PointLights inside rooms.
- Post: EffectComposer -> RenderPass -> GTAOPass (radius .35) -> OutputPass. Add a Low/High toggle (G key): low = no composer, no shadows, pixelRatio 1.
- Ground/floors/walls: tiled PBR textures (diffuse + normal) with repeat; RoundedBoxGeometry for anything built by code; smooth shading.

## 3. Grime shader for cleaning / restoration games
`material.onBeforeCompile`: pass object-space position to the fragment, fbm noise, mask = smoothstep(1-dirt±0.05, noise);
mix base colour to dark brown, roughness -> 1, metalness -> 0, and darken overall by dirt*0.3. One uniform per item (`uDirt`)
shared by all its cloned materials; condition 0..1 -> uDirt = (1-condition)*0.88. Scrubbing reveals the clean texture in patches.

## 4. Hosting limits (claude.ai artifacts)
- Served file types only: no `.glb`, `.bin`, `.hdr`. Convert to `.gltf` JSON with the buffer embedded as base64 data URI,
  textures as separate `.jpg` (served), file named `.json`. HDR -> base64 in JSON, decode with `RGBELoader.parse` into a DataTexture.
- Max 255 files per publish (publish twice to the same URL), 16 MB per file, 64 MB per publish.
- For Steam (Electron) keep the same files; for web portals keep the first-load payload small: load the props + tier 1 models first,
  then lazily load other tiers in the background.

## 5. Testing
Headless Chromium uses SwiftShader (CPU) -> 1-3 fps with GTAO; test logic with direct calls (`window.__game`), screenshots
need 1-2 s waits; never judge performance from headless.
