---
name: study-platform-design
description: Use this skill to generate well-branded interfaces and assets for Soul Dust Revival (a commerce storefront + gated study app for devotional study content, plus its printed book-cover system), either for production or throwaway prototypes/mocks/etc. Contains the sunset palette, Anton/Source Serif 4/Archivo type, spacing, UI kit components, brand marks, and the calibrated wraparound-cover system.
user-invocable: true
---

Read the readme.md file within this skill, and explore the other available files.

If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view. If working on production code, you can copy assets and read the rules here to become an expert in designing with this system.

If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.

Note: the canonical palette is the "sunset" direction (ink `#1a120c`, parchment `#f7ecd8`, ember `#e2762c`, gold `#f6c453`), kept in step with the Soul Dust Revival design system in Claude. Ember and gold fail 4.5:1 on parchment, so use them for fills, buttons, focus and large display type only; use `ember-700` `#b8501f` for large accent text. For book covers, read `assets/applied-covers/README.md` and `calibration.json` before building anything; never re-derive cover measurements.
