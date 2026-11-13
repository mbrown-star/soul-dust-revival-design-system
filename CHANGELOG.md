# Changelog

Newest first. Dates before 2026-10-01 are approximate, reconstructed from the old READMEs. Each entry says what changed and why. The current rules are in the README and each group's README. Detailed per-title build notes for finished covers are in the shared drive under *Claude Code Covers → <title> → Build notes*.

## 2026-11-13: Brought current with the site's work from 2026-11-07 to 2026-11-12
- **Why:** asked to update the design system with everything since 11-07. The site shipped many builds in those days (the store, sign-in, the readers, the Journey, admin tools) and none had reached this system. Each composition below was rebuilt from the live source files, read fresh, not from the site's build notes.
- **Tokens unchanged.** `tailwind.config.js`, `app/globals.css` and `app/layout.tsx` have no changes since 2026-11-07, so no color, type or spacing token moved.
- **`Storefront` rebuilt:** the featured Journey band; search with Type and Sort pills; one slot shape for every cover tile with each cover at its own shape; the simplified eyebrow; Coming soon; "Coming soon on Amazon"; the Buy on Amazon dialog; the "Buying on Amazon? You get both:" box; bundles' "What's included"; account-only checkout; one line per variant on the confirmation; and `/claim`.
- **`Account` rebuilt:** sign-in by emailed code (email, then "Enter your code", with no link or password); the no-account and blocked-email errors; order history on the account page; the new Contact page with screenshot attachments.
- **`StudyApp` rebuilt as the app shell:** My Library (search, Type and Status filters, Continue / Not started / Completed, Start over, Sneak peek cards and lock lines, the Journey card), the study contents page with locked sample lessons and Resources, and a plain lesson's navigation with "Mark complete & continue" and the end-of-sample card.
- **New `StudyReader`:** the five-tab study week (progress ring, dotted tab bar with scroll fades, week picker and word-study sheets, station stepper, prayer timer, Lift Up as the one saved completion).
- **New `DevotionalReader`:** Today, The Year, Journal and Six Faces of the Dust, plus the Bible Journey's variant (readings card, no question, no psalm counts).
- **New `Journey`:** the home page (mottled hero, gold year ring, this week, the trail map, "Your rhythm"), the not-begun state, and a Part's threshold.
- **New `SiteNav`:** desktop signed in and out, and the mobile hamburger menu; "Store" and "App" replace "Books & Studies" and "Your Studies".
- **`AdminConsole` extended:** Bundles (with "Present as a Journey"), product Kind, Binding, Coming soon and the Amazon choice; the "Saved" status; lesson-list badges, toggles and inline add; the drag-and-drop lesson builder with draft and publish; user delete with email blocking and the Blocked emails list; Reports → Amazon claims. Its sample study is now Colossians (the Foundations placeholder data was deleted from the site on 2026-11-09).
- **`PurchaseOptions`:** helper copy corrected; a printed book now includes its digital edition, and every order needs an account.
- **README:** "Web app — current state" updated, with what's still not covered; components table lists the new compositions.
- **Checked:** every changed preview rendered in a local harness with React 18.3.1 and this system's own `bundle.js`, clicked through, scripts parse clean, and nothing overflows sideways.
- **Copied to the GitHub backup repo** (`mbrown-star/soul-dust-revival-design-system`) the same day: this changelog and the readme's "Web app — current state" section. The compositions themselves stay in this system only, as in earlier syncs.

## 2026-11-07 (later still): Save/Delete buttons now literally share the system's Button component
- **Why:** the user noticed `AdminFormActions`' Delete button rendered as a bordered box in this preview but as plain colored text on the live site, and asked why — a real, separate gap from the color-token fix on 2026-11-06. The color fix made both sides use `error`, but never addressed that the three forms hand-rolled their own `<button>` markup instead of sharing a component, so Delete's actual shape (bordered box vs. plain text) never matched.
- **Live site fix:** added `components/ui/Button.tsx`, a line-for-line port of this system's own `Button.jsx` (read directly from the compiled bundle to match exactly: same base styles, the same `primary`/`secondary`/`ghost`/`danger` variant-to-token mapping, the same `md`/`sm` sizes). `ProductForm`, `BlogPostForm`, and `StudyForm` now import and use it for Save/Delete instead of hand-rolling. Verified computed styles in-browser on all three forms — background, text color, and border now match the design system's `Button` `danger`/`primary` variants exactly (previously confirmed by color alone, now confirmed by full style).
- **`AdminFormActions` README:** updated to say the preview is now the live implementation, not an approximation — the gap it originally flagged (2026-11-05) is fully closed, not just color-matched.
- `npm run verify` and `npm test` (202, unchanged) both clean.

## 2026-11-07 (correction): admin forms widened to the full page width, not narrowed
- **Why:** the entry just below this one standardized every admin form at a narrower `max-w-lg` (32rem) column, reasoning from `tokens.json`'s own `content-md` usage note ("Admin form column width"). The user corrected this immediately: every page component should span the *same width as the nav bar* (logo to Log out), not a narrower column — the opposite direction from what was applied.
- **Live site fix:** removed `max-w-lg` from all 9 admin forms/settings pages that had just received it (`ProductForm`, `StudyForm`, `BlogPostForm`, `LeaderResourceForm`, `ImportStudyForm`, `AddUserForm`, and the three settings/social pages) — they now fill the admin layout's `max-w-5xl` container exactly like the nav bar. Verified in-browser: the study edit form's inputs now stretch edge-to-edge at the nav bar's own width.
- **`tokens.json`:** corrected `content-md`'s usage note — it no longer describes real admin UI (its one remaining live use is the leader-access-denied message block); kept the token itself rather than deleting it, since removing a token outright needs its own decision.
- **`AdminConsole` composition:** removed the matching `maxWidth: 420`/`maxWidth: 576` inline-style caps from `ProductEdit` and `SocialComposer`, so the composition's forms stay accurate to the (now full-width) real site.
- **README.md:** corrected the Spacing section, which had just listed "32rem admin forms" as one of the standard narrow columns — admin forms are explicitly *not* one of those now.

## 2026-11-07: Account and Blog added; AdminConsole and StudyApp extended; code-review findings fixed
- **Why:** closes the remaining gaps named as deferred/not-yet-audited across the 2026-11-05/06 entries — the account/login pages, the public blog, the admin Reports sub-pages and social composer, and video/audio lesson blocks — plus 4 of the 5 code-review findings deferred on 2026-11-05.
- **Live site fixes (code-review follow-up):** checkout now merges cart lines sharing `{productId, variant}` before pricing/order-creation (a direct API call could previously be charged twice for one entitlement); the sales report shows `order_items.variant`; two non-null assertions on `digitalPriceCents` are now explicit guards; the duplicated `isDigitalItem`/`isPhysicalItem` logic in checkout and the Stripe webhook handler is now one shared `isDigitalVariant`/`isPhysicalVariant` helper. Investigated and did *not* change a 5th deferred finding (a claimed `getDb()` race) — it isn't actually racy; JS's single-threaded event loop rules it out. Also fixed 5 headings (account, checkout success, the lesson viewer, login/signup) still using plain `text-*xl font-semibold` instead of `font-display`/`ink` — the login/signup one was missed in the earlier sweep because `AuthForm.tsx` lives under `components/`, not `app/`.
- **New `Account` component**: login, signup, and the signed-in account page, from `components/auth/AuthForm.tsx` and `app/(marketing)/account/AccountPageClient.tsx` — including the real "type DELETE to confirm" safeguard on account deletion and the no-account-found error's link to Signup.
- **New `Blog` component**: the public listing and post pages, from `app/(marketing)/blog/page.tsx`/`[slug]/page.tsx`.
- **`AdminConsole` extended**: Reports gained its Engagement and Social-analytics sub-pages (previously only Sales existed); Social gained its New Post composer (platform checkboxes, live per-platform character counts against real limits, the Instagram-requires-an-image rule).
- **`StudyApp` extended**: the lesson viewer's content-block set now includes video and audio (placeholder playback, the real transcript-disclosure behavior, and audio's gold-700 "Transcript not yet available" message) — all six real block types are now modeled.
- All new/extended compositions tested click-through in a browser harness; no console errors. `npm run verify` and `npm test` (202, 2 new) clean for the code fixes.

## 2026-11-06 (final): StudyApp rebuilt from live source — all three page compositions now current
- **Why:** closes the last item from the three-composition resync started with `Storefront` and continued with `AdminConsole` earlier today.
- **`StudyApp` rebuilt from real current source** (`app/(study-app)/studies/page.tsx`, `studies/[slug]/page.tsx`, `studies/[slug]/[lessonId]/page.tsx`, `components/study/LessonBlock.tsx`/`ProgressBar.tsx`/`QuestionBlock.tsx`), replacing the 2026-09-21 compile. Now models the real entitlement gate (`hasEntitlement()` — an unentitled study redirects to its own linked product's page, never a generic "forbidden" screen, and never the study's own slug), real per-study and per-lesson progress tracking from `lessonProgress`, and the text/callout/question content-block types. Video/audio blocks aren't modeled. Tested click-through in a browser harness (login → studies list with both an entitled and a gated study → study detail with progress → a lesson's blocks, including the question field's save-on-blur behavior) — no console errors.
- **README.md:** updated the Components table (all four Pages compositions now current, no stale flags left) and removed the now-closed "needs a resync" Open item — **the three-composition resync flagged on 2026-11-05 is complete.**

## 2026-11-06 (later): site-wide token fix, AdminConsole rebuilt from live source
- **Why:** rebuilding `AdminConsole` from real source (the next composition after `Storefront`, per the Open items below) surfaced that the admin-forms token gap just fixed was far from isolated — nearly every admin page used the same stock colors, and so did a handful of public-facing files. Confirmed scope with the user at each step before fixing at increasing scale (3 forms → 16 admin files → 38 files total including 5 public-facing ones).
- **Live site fix:** every remaining admin page/component (`products`/`studies`/`blog`/`leader-resources` lists, all three `reports` pages, `settings/connections`, `social` scheduling, the lesson block editor, color picker, rich-text toolbar) plus `AccountPageClient.tsx`, `AuthForm.tsx`, and the Audio/Question/Video study-content blocks now use `ink`/`moss`/`error`/`gold`/`gold-700`/`ember-700` instead of stock `neutral`/`red`/`amber`/`green`/`blue`. Added a `success` token (`#3b5a2b`) to `tailwind.config.js` — `tokens.json` had documented this as `state-success` since 2026-10-01, but it was never exposed as a usable Tailwind class, so the social-post "published" status (a genuine success state with no mapped token) had fallen back to stock green; `scheduled` now uses `ember-700` as an info/upcoming-accent role rather than the stock blue it had no equivalent for either. `npm run verify` and `npm test` (200) both clean; spot-checked admin products, social, and login pages in-browser.
- **`AdminConsole` rebuilt from real current source**, closing the structural gap (not just staleness) the 2026-09-21 compile had — it only ever modeled Products → Studies → a lesson block editor, with no notion of the other five real admin sections. Now all 8 (Products, Studies, Leader Resources, Blog, Social, Users, Reports, Settings) exist and are reachable from the nav, matching `AdminNav.tsx` exactly. Products, Studies/lesson-editor, Users, Reports→Sales, Social, and Settings/Connections are modeled with real depth (click through, real field sets and table structure, from this session's own source reading); Leader Resources and Blog are one representative list screen each. Tested click-through in the same browser-harness approach as `Storefront`, no console errors.
- **README.md:** documented both fixes, updated the Components table (`AdminConsole` now current, `StudyApp` the last composition left stale), and narrowed Open items to just `StudyApp`.
- **Not done:** `StudyApp` — the last of the three compositions still needing the same from-source rebuild.

## 2026-11-06: admin-forms token fix applied, Storefront rebuilt from live source
- **Why:** picks up the two open items the 2026-11-05 (overnight) audit below left explicitly unresolved — the admin forms' live `neutral-900`/`red-600` gap, and a real `from-code` resync of one of the three stale page compositions, started with `Storefront` as the one with the biggest functional drift (it predated the `format: "both"` commerce model entirely).
- **Live site fix (not a design-system change, but closes the gap `AdminFormActions` flagged):** `ProductForm`, `BlogPostForm` and `StudyForm` now use `ink`/`error` instead of Tailwind's stock `neutral-900`/`red-600` for every focus ring, the Save button and all error/Delete text. Verified via computed styles in-browser (`rgb(26,18,12)` on the Save button and inputs' focus rings, `rgb(168,48,28)` on Delete and error text). Found and fixed a second instance of the same gap while rebuilding `Storefront` below: `checkout/success/page.tsx` used `neutral-600`/`neutral-900` instead of `moss`/`ink`.
- **`Storefront` rebuilt from real current source** (`app/(marketing)/books/page.tsx`, `books/[slug]/page.tsx`, `checkout/page.tsx`, `checkout/success/page.tsx`, `lib/cart/CartContext.tsx`), replacing the 2026-09-21 scaffold compile. Now models: the real "both" format dual-purchase flow (two independent cart lines keyed by `{productId, variant}`, matching `lineKey()`); the combined cart/checkout page (there's no separate cart page in the real site); the digital-requires-an-account gate; the guest-email field shown only for a physical-only, logged-out cart; the country-required field on every order; and a success screen whose shipping block and "Log in to access your content" CTA are conditioned on the real order's physical/digital composition. Tested click-through in a browser harness mocking the system's React/Button globals: both-format add-to-cart, the login gate, the guest-email path, and order placement all behave as modeled, no console errors.
- **README.md:** updated "Web app — current state" to reflect both fixes, marked `Storefront` current in the Components table (`StudyApp`/`AdminConsole` remain stale), and narrowed Open items to just the two compositions still owed a resync — `AdminConsole` next, since its gap is structural (missing the Users/Reports/Social areas outright), not just stale.
- **Not done:** `AdminConsole` and `StudyApp` still need the same from-source rebuild `Storefront` just got — left as the next two items, in that order.

## 2026-11-05 (overnight): web-app currency audit, two new components, stale compositions flagged
- **Why:** asked to bring the whole system current for the web app and web app alone — not just covers — since the live `soul-dust-revival` site had drifted far ahead of what this system documented, while only the color tokens had actually been kept in sync (the 2026-11-05 parchment/gold-700 entries below). The three page compositions (`Storefront`, `StudyApp`, `AdminConsole`) turned out to still be exactly what was compiled from the *original, pre-customization* scaffold on 2026-09-21 — none of the real site's subsequent changes (documented at length in the site's own `CLAUDE.md`) had ever reached them.
- **README.md:** fixed the Visual Foundations color section, which still quoted the retired `#f7ecd8` parchment and never mentioned `gold-700` or `error`/`state-success`/`state-warning` — now matches `tokens.json` exactly (tokens.json itself was already current; only the prose had drifted). Added a dated "Web app — current state" section as the honest, current source of truth: shared-shell nav structure, the new `format: "both"` commerce model, admin delete, the Tiptap rich-text unification, and an explicit list of what this audit did *not* reach (checkout/cart line items, account/login/order-confirmation pages, blog/leader-resources at their current width, admin Users/Reports/Social). Reordered the opening paragraph to name the web app as the actively-developed product, with covers framed as the (large, but one-at-a-time) secondary system.
- **Two new components, built from the live site's real source, not the old scaffold:**
  - `PurchaseOptions` (new `Commerce` group) — the format `"both"` dual physical/digital purchase panel from `app/(marketing)/books/[slug]/page.tsx`.
  - `AdminFormActions` (added to `Forms`) — the Save/Delete button pair from `ProductForm`/`BlogPostForm`/`StudyForm`, including an explicitly flagged gap: the live buttons currently use Tailwind's stock `neutral-900`/`red-600`, not this system's `ink`/`error` tokens. Documented as a live-code fix still needed, not quietly matched.
- **`Storefront`, `StudyApp`, `AdminConsole` READMEs** each got a dated "stale as of 2026-11-05" note naming the specific real changes that happened underneath them, so a reader isn't misled into thinking these click-throughs are current.
- **Not done:** an actual rebuild of those three compositions from the live codebase (a proper `from-code.md`/`/design-sync`-style pass) — that's a larger job than an overnight audit, and is now explicit in Open items so it doesn't get lost.

## 2026-11-05: parchment lightened; PaletteOptions component added
- `parchment` changed from `#f7ecd8` (visibly cream/tan) to `#fefdfa` (near-white, a bare hint of warmth), per a nav-bar color review. Every token whose usage note quotes a contrast figure "on parchment" was recomputed against the new value (all improved, since the new background is lighter): `ink` 15.8→18.2:1, `dusk` (as a text-on-ink-surface figure) 11.96→13.76:1, `ember` 2.62→3.01:1, `ember-700` 4.27→4.91:1 (now clears AA for body text on parchment itself, though the large-text-only guidance stays for darker light-surfaces like `surface-sunken`), `gold` 1.39→1.60:1, `gold-700`/`state-warning` 4.53→5.22:1, `moss` 6.09→7.01:1, `text-tertiary` 4.87→5.60:1, `state-error` 5.78→6.65:1, `state-success` 6.69→7.70:1. `surface-sunken` (a documented 92% paper / 8% dusk blend) recomputed to `#eeebe8`.
- `dusk` itself was reviewed against three alternatives — a cool slate-grey "true dusk," a muted indigo-violet twilight, and a desaturated warm-charcoal compromise — for the nav bar specifically, but kept as-is (`#3a281c`); none of the alternatives were adopted.
- Added `PaletteOptions`, a Foundations component recording this review (all four `dusk` options and four `parchment` options, each shown in context — a page-background demo for parchment, the live nav-bar monogram+wordmark treatment for dusk — with the adopted ones marked), alongside the existing `Palette` component.

## 2026-11-05: gold-700 token
- Added `gold-700` `#8d6407`, mirroring `ember-700`: gold itself is 1.39:1 on parchment (fills and large display type only), so small gold-family accent text/links on parchment now has an AA-passing option at 4.53:1, instead of either failing contrast or borrowing `state-warning`'s value for non-warning text.

## 2026-10-19: Benedictions, Blessings & Doxologies study cover
- Benedictions, Blessings & Doxologies cover added: Topical Study, 8.5x11, 176pp, ground Sapphire `#15264A` (new, from the Revelation 5 throne scene), spine 0.44in. Copy file `titles/benedictions-study.json`. It replaces the earlier 14-page Scriptural Catalog cover (Navy `#1E2733`, blank spine) for the same title, whose register row is superseded.
- Rebuilds from the copy file and passes `verify_covers.py` (16/16). The shipped PDF was built outside this repo's checks, so a rebuild may differ from it; no pixel comparison was made.

## 2026-10-12: John covers added, Revive Me page count corrected
- John: That You May Believe, Parts One to Four added: Book Study, 6x9, ground Blue-grey `#385569` (approximate, read off the rendered back panel; not a named ground), 211 / 215 / 212 / 210pp, spines 0.5275 / 0.5375 / 0.53 / 0.525in. Copy files `titles/john-part-1.json` to `john-part-4.json`, transcribed from the delivered covers (no text layer) and confirmed by Matt. They rebuild and pass `verify_covers.py` (69/69), but the shipped PDFs were built outside this pipeline, so a rebuild may differ from them.
- Revive Me page count corrected from 232 to 234, per its interior PDF. The 0.711in spine and 14.2867in x 10.4167in wrap still match the 232-page calculation, so they need rechecking against KDP's hardcover calculator for 234pp before upload.

## 2026-10-10: Revive Me cover
- Revive Me cover added: single-volume hardcover, 6x9, 234pp (corrected 2026-10-12; originally logged as 232), ground Ochre `#3e2c0e`. Spine 0.711in and board/wrap/hinge geometry come from KDP's hardcover calculator, not the pages x 0.0025in paperback formula.
- No copy file: it was built without the pipeline zip (from the John covers as references), so it can't be rebuilt from `titles/` yet. A hardcover mode in `gen_covers.py` is still to do.

## 2026-10-06: 1 Timothy and James covers
- 1 Timothy cover added: Book Study, 6x9, 203pp, ground Gunmetal `#323232`. Copy file `titles/1-timothy.json`.
- James cover added: Book Study, 6x9, 202pp, ground Coal `#1b1b1b`. Copy file `titles/james.json`.
- Both rebuild from the copy files and pass `verify_covers.py` (16/16). Their Drive build notes say they were built with a locally patched pipeline (2026-10-02 directives: no back-panel footer, bottom pad 0.12, `six_by_nine_back_tightening` in `calibration.json`) that isn't saved here yet, so a rebuild from this folder may differ slightly from the shipped PDFs.

## 2026-10-01: cover requests ask for both inputs
- Every cover request now starts by confirming the study's manuscript PDF and `SDR-cover-pipeline.zip` are in hand, asking for whichever is missing.
- The pipeline bundles its own fonts (Liberation Serif, DejaVu Serif Condensed) so it renders identically in a Claude Chat sandbox.

## 2026-10-01: cover pipeline rebuilt
- `gen_covers.py`, `render.py` and `to_pdf.py` rebuilt from the cover rules (the originals were never saved), and `verify_covers.py` generalized to every title. Proven by rebuilding The Ten Commandments (8.5x11) and 1 Peter (6x9): mean pixel difference about 4.5/255 against the shipped PDFs, text within 0-3px, identical page sizes; verify passes 37/37.
- `calibration.json` gained `fixed_px_at_300dpi`: the back panel and the front's secondary lines are fixed pixel sizes on every trim, measured off the shipped covers. Spine sizes corrected to what the shipped covers actually use: DejaVu Serif Condensed, series 56px, title 54px, imprint 54px (the earlier 62px was an ink measurement). `WraparoundCover` updated to match.
- Copy files for both titles are in `assets/applied-covers/titles/`.

## 2026-10-01: article text and heading case
- Anton titles stay uppercase, but headings inside long-form articles (lessons, blog, leader resources) now use normal case.
- Article text uses brand colors: ink body, headings, links and quotes, moss secondary text, ember link underlines and quote borders. Previously the web app used Tailwind's default grey.

## 2026-10-01: ink focus ring
- `focus-ring` changed from gold to ink: gold is only 1.39:1 on parchment, below the 3:1 minimum for focus indicators. Added `focus-ring-on-dark` (gold) for ink and dusk sections. Components that use `focus-ring` pick this up automatically.

## 2026-10-01: error color and web app port
- `state-error` changed from ember (2.62:1, fails as text) to `#a8301c` (5.78:1 on parchment), so error messages pass WCAG AA.
- The study-platform-scaffold web app now takes its colors and fonts from these tokens (CSS variables in `app/globals.css`, mapped in `tailwind.config.js`, Anton via `next/font`).

## 2026-10-01: reorganization
- Finished cover PDFs moved to the shared drive (*Claude Code Covers*, one folder per title with its build notes). Only the Ephesians reference stays here, in `applied-covers`. Duplicate files outside `project/` removed.
- READMEs rewritten as current rules. Their build history moved into this changelog.
- Components regrouped: Foundations, Forms, Feedback, Navigation, Data display, Covers, Pages, Archive (old homepage drafts). The Components tab doesn't show group headings, so the README carries a by-group table, the live components are listed in group order, and divider rows (Forms, Feedback, Navigation, DataDisplay, Covers) head each group.
- Production grounds renamed so every name is unique: 28 Ash → **Soot**, 33 Loam → **Peat**, 30 Oxblood → **Garnet**, 32 Ember → **Smolder**, 36 Rust → **Tannin**. Hex values and images unchanged. Files renamed to match.
- The four inferred tokens (`surface-fill`, `text-tertiary`, `state-success`, `state-warning`) approved as-is.
- Added `ember-700` `#b8501f` for small accent text, since ember and gold are too light for text on parchment.
- `WraparoundCover` spine series-name and imprint sizes 19/22px → 56px, matching `calibration.json` and the printed covers.
- Brand marks regenerated with the real Anton face (they previously used a stand-in font). Added SVGs with outlined text, plus 2x and 4x PNGs. The lockup's two wordmark lines got 3px of space between them because they touched in real Anton, and the "Psalm 119:25" line is now set in Source Serif 4 italic (it was a Georgia fallback).
- GitHub repo synced to this system. From now on it's the backup and is synced at the end of each session.

## 2026-10-01: The Ten Commandments cover
- Topical Study, 8.5x11, 183pp, ground Cinder. Built straight from `calibration.json`, clean on the first render.

## 2026-09-28 to 2026-09-30: series covers
- Built 1 Peter, Benedictions, The Gospel, The Holy Spirit, Prayer, Genesis Parts 1 and 2, Dusty and Holy, Dusty but Hopeful, Colossians, The Sermon on the Mount, the 365-Day Journey, Ecclesiastes, Galatians, In Christ, Law and Gospel and Philippians. Lessons that became rules:
  - Long titles (Benedictions, 365-Day Journey) use the manuscript's own two-line break, and the 365-Day spine carries only the title's first line.
  - Spines under 79 pages stay blank (Benedictions, 14pp).
  - A bounded range within a book is a Topical Study at 8.5x11 even if the book appears on the Book Study list (Dusty but Hopeful, Romans 6–8).
  - Back-panel overflow from a long hook (Colossians, Ecclesiastes) or from cumulative copy length (Philippians): keep the hook to one sentence under ~75 characters.
  - A long subtitle wrapped the tagline into the fixed rule (Law and Gospel), so taglines must stay on one line.
- **Design directive (2026-09-28):** the spine's series name and imprint line render 56px (title 62px minus 6px) on every title. `calibration.json` was updated. Ephesians' already-printed cover was not rebuilt.

## 2026-09-22 to 2026-09-27: four-part study and the calibration pipeline
- Built *Out of the Dust*, *Formed and Sent*, *Confession & Repentance* and *Life* from scratch to match Ephesians. It took nine layout passes. The fixes that stuck: medium-weight one-line title sized by character count; cream series name; separate height/width keyline insets; each spine line as its own vertical-writing element; spine type in fixed 300dpi pixels, never scaled by spine width (scaling by each title's own width made the four look inconsistent, and scaling to the narrowest made them all too small).
- Introduced `calibration.json` (the single source of every layout number, measured from the Ephesians print PDF at 300dpi) and `verify_covers.py` (a rendered-pixel check that must pass before delivery).
- Added "A Journey" / "A Journey Part [N]" to the four-part study only.

## 2026-09-21 to 2026-09-22: cover grounds and spine blend
- Applied pairing 01 (Dusk) to the Ephesians cover at its real trim and spine. The spine went from a hard seam, to a feather that spilled into the back panel, to a smoothstep fade confined to the spine. That fade is now the standard for every wraparound.
- Extended the grounds: `16`–`27` darker variations (soil … slate), built from a recipe reverse-engineered from the originals (≈7/255 mean difference from `01`), then `28`–`38` with the production hex values from shipped covers.

## 2026-09-21: design system created
- Built from `mbrown-star/soul-dust-revival-design-system@828149b`. The sunset palette (ink `#1a120c`, ember `#e2762c`, gold `#f6c453`, Anton display) was made canonical, replacing the earlier `tokens/colors.css` palette (ink `#17231f`, ember `#de3a2e`, gold `#f0b93e`, Fraunces).
- The 12 small components render live from the repo's bundle. Storefront, StudyApp and AdminConsole were compiled from the repo's `ui_kits` JSX. The homepage, logo, palette and cover-library HTML files were added as pages.
