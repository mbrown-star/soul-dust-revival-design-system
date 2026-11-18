# Cover Blends × Mottles

All 43 cover grounds, each blend shown beside the plain mottle it's built on, with its name. Choose a new title's ground here, then check the register in `assets/applied-covers/README.md` to make sure no other title uses it.

**Numbering:** `01`–`15` are the original sunset-family grounds (only the darker eight appear on this page). `16`–`27` are darker ground-level variations. `28`–`43` are the production hex values from shipped covers (`39`–`43` added 2026-11-17). Every name is unique: Soot, Peat, Garnet, Smolder and Tannin (28, 33, 30, 32, 36) were renamed on 2026-10-01 so they no longer clash with Ash, Loam, Oxblood, Ember and Rust.

| # | Ground | Hex | # | Ground | Hex |
|---|---|---|---|---|---|
| 16 | Soil | `#241a12` | 28 | Soot | `#2a2a26` |
| 17 | Ash | `#2b2b28` | 29 | Navy | `#1e2733` |
| 18 | Stone | `#33383a` | 30 | Garnet | `#2e1013` |
| 19 | Iron | `#23282b` | 31 | Deep Teal | `#12302c` |
| 20 | Clay | `#3a2420` | 32 | Smolder | `#3d1c0c` |
| 21 | Bark | `#2e2117` | 33 | Peat | `#2e2a18` |
| 22 | Char | `#1c1611` | 34 | Basalt | `#2a2530` |
| 23 | Loam | `#2f2a1c` | 35 | Veil | `#3a1b32` |
| 24 | Bramble | `#2a2f1f` | 36 | Tannin | `#4a2318` |
| 25 | Marrow | `#211b16` | 37 | Regal | `#211b47` |
| 26 | Cinder | `#2c211e` | 38 | Storm | `#34383e` |
| 27 | Slate | `#26302f` | 39 | Gunmetal | `#323232` |
| | | | 40 | Coal | `#1b1b1b` |
| | | | 41 | Sapphire | `#15264a` |
| | | | 42 | Ochre | `#3e2c0e` |
| | | | 43 | Verdigris | `#1b3b40` |

The original fifteen (`01`–`15`) and their hex values are in `CoverMottleLibrary`.

**Recipe for `16`–`43`** (use the same recipe for any new ground):
- *Mottle:* a flat color, then a low-frequency cloud blotch (SVG fractal noise, `overlay`, 55% opacity), then fine grain + vignette (`soft-light`, 90% opacity).
- *Blend:* `hero-variants/01-original.png` in grayscale, tinted with the ground via a `color` blend, desaturated 50%, `overlay`-composited onto the mottle. The texture layers are not reapplied over the photo.
- The recipe matches the original `01-dusk-on-dusk` within ≈7/255 mean pixel difference: close but slightly brighter than the originals.
- Checked 2026-11-17 by regenerating Soot (28) and Cinder (26) at 480px: mottles within ≈5/255 of the files here, blends within ≈4/255. Reapplying the textures over the photo (as this page used to say) comes out ≈18/255 off and much brighter, so the files were never built that way. The 39–43 files were made with the recipe exactly as written here.
- These swatches are for choosing a color. A cover is built with `assets/applied-covers` and must look like the shipped covers (see its README).

**On a full wraparound,** the mottle runs continuously across the canvas and the blend fades in only within the spine's width (see `assets/applied-covers/README.md`).

Images on this page are 220px inline JPEGs. Use `assets/cover-blends` and `assets/cover-mottles` for the real files.
