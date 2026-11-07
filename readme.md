# Soul Dust Revival Design System

The design system for **Soul Dust Revival**, a Psalm 119:25 devotional ministry (*"My soul cleaves to the dust; revive me according to Your word"* — NASB). It covers the **web platform** (public storefront, gated study app, blog, leader resources and the admin console — the primary, actively-developed product, built on `mbrown-star/study-platform-scaffold`) **and** the printed book-cover system for the Book Study, Topical Study and 365-Day Devotional titles. Covers get a lot of this system's file volume (dozens of ground images, a full calibration pipeline) because they're produced one at a time by hand; the web app's tokens and live components are the part that actually ships continuously and should be read first for anything touching the site.

## How we work

- **The Soul Dust Revival design system in Claude is the master copy.** This repo is its versioned backup. Don't edit it independently: change the system in Claude, then at the end of that session copy the changes here and add a line to `github.md`.
- **Keep the web app in step — both directions.** `mbrown-star/study-platform-scaffold` (built out as the real `soul-dust-revival` project) takes its colors from CSS variables in `app/globals.css` (mapped in `tailwind.config.js`) and its fonts from `app/layout.tsx`. When a color or font changes here, update those files in the same session — and the reverse: when the live site's own build adds or changes a token, a component, or a real page/flow, that needs to land here too, not just in the site's own `CLAUDE.md`. **This system had drifted on the second direction** — see "Web app — current state" below for what that audit found and what it didn't reach.
- **Log every change** as a dated entry at the top of the Changelog section (`CHANGELOG.md`): what changed and why, in a few lines. This README holds only the current rules. History goes in the changelog.
- **Finished covers don't live here.** Each print-ready cover PDF goes in the shared drive under *Soul Dust Revival → [Claude Code Covers](https://drive.google.com/drive/folders/17VHHakHBc2b0LlbSSa_JYw1e3bshOl4M) → <title>*, with that title's build notes. This system keeps only what's needed to *make* a cover (see Covers below).
- **Starting a cover:** Before starting any cover, make sure you have both: the study's manuscript PDF (ask for it if it wasn't provided) and `SDR-cover-pipeline.zip`, the cover scripts, fonts and hero photo (ask for it if it isn't already in the conversation). Don't start without both.
- **Building a cover:** read the rules in `assets/applied-covers/README.md` → pick an unused ground from `CoverBlendMottlePairings` → write `titles/<key>.json` → `gen_covers.py` (reads every number from `calibration.json`) → `render.py` → `verify_covers.py` must exit 0 → check the full, back, front and spine crops → export the PDF to the Covers folder → add the title to the register and the changelog.
- **Undecided things stay out of the rules.** Open questions go in the "Open items" section below until they're decided.

## Content fundamentals

- **Direct and functional, never marketing-voiced.** Buttons say exactly what happens: "Proceed to payment," "Send login link," "Save product," "Delete product," "Import document." Never "Get started" or "Let's go."
- **"You/your" for the reader, plain first person only in confirmations.** "Check your email for a login link." / "Thank you for your order."
- **Sentence case** in the app. ALL CAPS only for the small tracked block-type labels ("TEXT", "CALLOUT") and Anton titles.
- **No exclamation points, no emoji, no hype.** Errors are specific and calm: "This product has order history and can't be deleted. Mark it inactive instead."
- **Devotional labels are short and plain:** "Key Verse," "Reflection," "Prayer Prompt."

## Visual foundations

- **Color: the sunset palette.** Ink `#1a120c` on parchment `#fefdfa` (lightened 2026-11-05 from the original cream `#f7ecd8` — see `PaletteOptions`). Dusk `#3a281c` for deep sections and footers, moss `#6b5344` for secondary text. **Ember `#e2762c`** is the one chromatic accent and **gold `#f6c453`** the highlight.
- **Contrast rule:** ember (3.01:1 on the current parchment) and gold (1.60:1) never carry small text on parchment. Use them for buttons, fills and large display type. For small accent text (links, inline emphasis) use **`ember-700` `#b8501f`** (4.91:1) or **`gold-700` `#8d6407`** (5.22:1); use ink or moss for ordinary body copy. `error` `#a8301c`, `success` `#3b5a2b` (added to `tailwind.config.js` 2026-11-06 — `tokens.json` had documented it as `state-success` since 2026-10-01, but it had never actually been exposed as a usable class until a real success-state UI need, the social-post "published" status, surfaced the gap) and `state-warning` (= `gold-700`) are the three status colors, each AA-passing at any size on parchment.
- **Type:** **Anton** for display (headlines, hero, wordmark) at its native weight 400, often gradient-clipped ember→gold. Page and section titles are uppercase with leading ~0.92. Headings *inside* long-form articles (lessons, blog, leader resources) stay in normal case so long headings read easily. **Source Serif 4** for reading (lessons, blog). **Archivo** for UI (buttons, labels, nav, forms), with semibold headings. All three load from Google Fonts.
- **Article text** (lessons, blog, leader resources): body, headings, links and quotes in ink; lead text, list markers and captions in moss; links underlined in ember; quote borders ember. These pages use the site's standard `max-w-5xl mx-auto px-4` content width (see "Web app — current state"), with the prose column itself capped narrower for readability.
- **Spacing:** 4px-based scale. Narrow, centered columns: 24rem login, 36rem checkout, 42rem lesson reading. Admin forms are **not** one of these narrow columns — every admin form spans the full `max-w-5xl` page width as of 2026-11-07, matching the nav bar exactly (edge to edge, logo to Log out), per explicit direction after an initial attempt to standardize them at a narrower 32rem was corrected. The admin shell's own content column was widened from 56rem (`max-w-4xl`) to the site's full standard 80rem (`max-w-5xl`) on 2026-11-05 — it's no longer a narrower exception either.
- **Borders over shadows:** 1px `border-default` and 8px corners on cards, fields, dividers and buttons. The only shadow is `shadow-popover`, on the admin's one popover menu.
- **Focus:** every interactive element gets a 2px outline with a 2px offset (WCAG 2.4.7). Use `focus-ring` (ink) on light grounds (15.8:1+ on parchment) and `focus-ring-on-dark` (gold) on ink and dusk sections. Never use gold on parchment, where it's only 1.60:1. Never remove the ring.
- **Motion:** functional only (progress-bar fill, hover/focus transitions) and always honors `prefers-reduced-motion`. The hero's rising dust motes are the one decorative motion. A `.mottle` cloud-blotch/grain/vignette texture (ported from the cover system's own mottle treatment, see `CoverMottleLibrary`) is applied to the homepage's dusk band and the site footer as of 2026-11-05 — the one place cover texture and web-app surface share a treatment; not applied elsewhere.
- **App backgrounds** are flat parchment or a light fill, except the one `.mottle` application above. Gradients, photography and texture otherwise belong to the marketing hero and the book covers.

## Iconography

No icon set. The few icons are Unicode glyphs in text: `⠿` drag handle, `↑`/`↓` reorder, `✓` success, `+` add, and a text "Remove"/"Delete" link. No emoji. If an icon set is ever needed, Lucide is the closest match.

## Brand marks

`assets/brand-marks/`: the stacked wordmark (primary), the monogram + wordmark lockup (used in the site's shared nav-bar shell — see below — and footers) and the SDR monogram badge (favicons, avatars). Each comes as an SVG (text converted to outlines, safe for print at any size), a PNG at 2x and a PNG at 4x. See `LogoVariations` for all five lockup options.

## Web app — current state

The web app is the actively-developed product and changes far more often than this system has been kept current with. This section is the honest status as of **2026-11-05**, written from the live site's own source and its `CLAUDE.md` build log, not from the (now stale) `AdminConsole`/`Storefront`/`StudyApp` page compositions below, which were compiled once from the original scaffold's pre-customization `ui_kits/*.jsx` on 2026-09-21 and have not been resynced since. Read this section for what's actually true today; treat those three compositions as historical reference only until they're rebuilt from the live site (see each one's own README for what specifically has since changed under it).

**Navigation.** Every top-level nav bar — public and admin — renders through one shared shell (`SiteHeaderShell`: sticky, `bg-ink/95` with backdrop blur, the monogram+wordmark lockup on the left, routing home) so the two can't drift apart in size or color. The public nav (`SiteNav`) groups public links first (Books & Studies, Blog, Cart, "Log in" when signed out), then a divider, then logged-in-only items (Your Studies, a "Profile" dropdown with Account/Admin-when-admin/Log out). The admin nav (`AdminNav`) sits in the same shell and no longer has its own narrower content column — see Spacing above. Nav links and the logo use a text-color-only focus indicator (color shift, no box) rather than a ring, by explicit decision, scoped to just these two nav bars.

**Commerce / products.** A product's `format` is `physical`, `digital`, or (added 2026-11-05) **`both`** — sold as two fully independent purchases, each with its own price and own Stripe Price, not a combined bundle. See the new `PurchaseOptions` component for the detail-page treatment and the admin's two-fieldset form (also new); a cart line and a checkout/order line both carry which variant (`physical`/`digital`) they are. A product's alt text is encouraged in the admin UI but, as of 2026-11-05, no longer enforced at all (widened from an earlier book-cover-only exemption) — a real, accepted accessibility trade-off, not an oversight.

**Admin delete.** Products, blog posts and studies (added 2026-11-05) can each be deleted from their edit form — see the `AdminFormActions` component. The live buttons' token-compliance gap this component flagged (`neutral-900`/`red-600` instead of `ink`/`error`) was fixed in the site's own code on 2026-11-06. A second gap this component also flagged — the three forms hand-rolling their own button markup instead of sharing one component, so Delete's actual *shape* (plain text vs. a bordered button) never matched this preview even after the color fix — was closed on 2026-11-07 with a new shared `components/ui/Button.tsx`, a direct port of this system's own `Button.jsx`. All three forms now use it for Save/Delete; `AdminFormActions`' preview is the live implementation, not an approximation.

**Rich text.** Blog post bodies moved from markdown to the same Tiptap-HTML editor already used for leader resources and lesson content blocks (`RichTextEditor`) — one authoring experience across all long-form admin content now, not two.

**Storefront rebuilt from live source (2026-11-06).** The checkout/cart page's line-item treatment for a "both"-format purchase is now covered — see `Storefront` below, rebuilt directly from `app/(marketing)/books/page.tsx`, `books/[slug]/page.tsx`, `checkout/page.tsx`, `checkout/success/page.tsx` and `lib/cart/CartContext.tsx`. The same pass found and fixed a second live token-compliance gap: `checkout/success/page.tsx` used `neutral-600`/`neutral-900` instead of `moss`/`ink`.

**Site-wide token-compliance fix (2026-11-06).** What started as the `AdminFormActions` finding (three admin forms using stock `neutral-900`/`red-600`) turned out to be nearly every admin page and several public-facing files — confirmed with the user and fixed across 38 files total. Added a `success` token to `tailwind.config.js` (`#3b5a2b`), finally exposing `tokens.json`'s already-documented `state-success` value as a usable Tailwind class — a real success state (the social-post "published" status) had no mapped token before this and fell back to stock green. See `CHANGELOG.md` for the full file list and mapping.

**`AdminConsole` rebuilt from live source (2026-11-06).** All 8 real admin sections (Products, Studies, Leader Resources, Blog, Social, Users, Reports, Settings) now exist in this composition, closing the structural gap flagged below — the original compile only ever modeled Products → Studies → lesson editor. See `AdminConsole`'s own README for exactly what's modeled with real depth versus as a representative screen.

**`StudyApp` rebuilt from live source (2026-11-06) — the last of the three.** Now models the real entitlement gate (an unentitled study redirects to its own linked product's purchase page, not a generic "forbidden" screen), real progress tracking (per-study and per-lesson, from `lessonProgress`), and the text/callout/question content-block types. See `StudyApp`'s own README for what's modeled with real depth versus not covered at all (video/audio blocks, the real magic-link email flow).

**All three page compositions (`Storefront`, `AdminConsole`, `StudyApp`) are now current as of 2026-11-06** — the resync flagged as an open item on 2026-11-05 is complete.

**Account, Blog, and the remaining admin/lesson gaps closed (2026-11-07).** New `Account` component (login/signup/account-page composition, including the delete-account "type DELETE to confirm" safeguard) and `Blog` component (the public listing/post pages). `AdminConsole` gained its Reports → Engagement/Social-analytics sub-pages and the Social → New post composer. `StudyApp`'s lesson viewer gained video and audio content blocks (placeholder playback, real transcript-disclosure behavior). The same pass found and fixed one more live token-compliance gap: the login/signup heading (`AuthForm.tsx`) used plain `text-xl font-semibold` instead of `font-display`/`ink` — missed earlier because that file lives under `components/`, outside the `app/` sweep the earlier fix searched.

**Not yet audited into this system:** leader-resources pages at their current `max-w-5xl` width (the add-user form and social composer's recurring-schedule config are intentionally out of scope at the representative-depth tier `AdminConsole` uses for secondary sections).

## Components

Under `components/`, each as `<Name>.jsx` + `<Name>.d.ts` + `<Name>.prompt.md`, plus a preview card per folder. `_ds_bundle.js` is the pre-built bundle (namespace `StudyPlatformDesignSystem_d2afba`).

- **Forms:** Button, Checkbox, ColorPicker, Input, Textarea, Select (plus the `AdminFormActions` composition, documented in the Claude system only; the live web app's `components/ui/Button.tsx` ports `Button` since 2026-11-07)
- **Feedback:** Callout, ProgressBar, StatusMessage
- **Navigation:** Tabs
- **Data display:** Badge, ProductRow
- **Commerce:** `PurchaseOptions` (format `"both"` dual-purchase panel; documented in the Claude system only, no repo component)
- **Foundations:** `PaletteOptions` (record of the 2026-11-05 color review; Claude system only)
- **Covers** (`components/covers/`): `WraparoundCover` (live, prop-driven preview of the calibrated cover layout) and `CoverBlendMottlePairings.html` (all darker grounds beside their mottles)

`Button` variants `secondary`/`ghost`/`danger` and the named `Badge`/`StatusMessage` are intentional additions beyond the app source. Callout backgrounds are free-form per instance (`#fef3c7` by default, any hex allowed) and are not tied to the tokens.

## Pages and reference sheets

The top-level HTML files are the brand's source documents. In the Claude system they're grouped as:

- **Foundations:** `Soul Dust Revival Palette.html`, `Soul Dust Revival Logo.html`
- **Covers:** `Blended Cover Grounds.html`, `Book Cover Library - Mottled Colors.html`, `Book Cover Library - Image Treatments.html`, `Hero Image Variations.html`
- **Pages:** `Soul Dust Revival Homepage.html` (current), plus `ui_kits/storefront`, `ui_kits/study-app` and `ui_kits/admin` (also as `templates/`)
- **Archive:** `Soul Dust Revival Homepage v2.html`, `v3.html` and `Homepage Variations.html` (earlier drafts)
- **Also in the Claude system only** (live-source compositions, not ported to `ui_kits/`): `Account` and `Blog` (new 2026-11-07); `Storefront`, `AdminConsole` and `StudyApp` there were rebuilt from the live site's source 2026-11-06/07, while this repo's `ui_kits/` still hold the original scaffold versions.

## Covers

- **Grounds:** `assets/cover-mottles/` (flat color + mottle texture) and `assets/cover-blends/` (the hero photo, duotoned and blended onto that mottle), 38 of each, numbered in pairs. Every ground has one unique name. `components/covers/CoverBlendMottlePairings.README.md` lists every name and hex value. `01`–`15` and the hero variants are full resolution here; `16`–`38` exist only at 480px.
- **Recipe and tooling:** `assets/applied-covers/` holds the rules, `calibration.json`, the build pipeline (`gen_covers.py`, `render.py`, `verify_covers.py`, `to_pdf.py`), one copy file per title in `titles/`, and the Ephesians reference cover.
- **Register:** every shipped title with its trim, spine and ground, so each new title can get its own ground. See `assets/applied-covers/README.md`.

## Open items

- **`surface-sunken` and `border-default`** are literal approximations of what were `color-mix()` blends in the original CSS.


## Index

- `styles.css`: global stylesheet entry point (import this)
- `tokens/`: `colors.css`, `fonts.css`, `typography.css`, `spacing.css`, `borders.css`
- `guidelines/`: foundation specimen cards
- `components/`: primitives and cover components; `_ds_bundle.js` is the built bundle and `_ds_manifest.json` its manifest
- `ui_kits/`, `templates/`: product recreations
- `assets/`: brand marks, hero and cover imagery, the cover recipe and build pipeline (`applied-covers/`)
- `CHANGELOG.md`: change history (mirrors the Claude system's)
- `github.md`: sync log
- `SKILL.md`: portable skill file for use in Claude Code or elsewhere
