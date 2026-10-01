A reusable, parametrized render of the Soul Dust Revival wraparound cover system — front panel, back panel, and spine — built from calibration.json's own measured numbers rather than a fresh approximation, so a new title's cover can be assembled by filling in props instead of re-running the print pipeline just to see how it will look.

## Why this exists

It reads the same calibrated fractions and constants as `assets/applied-covers/calibration.json`. It's a second renderer of that one calibration, not an independent design. If `calibration.json` changes, update the `CAL` object in the `WraparoundCover` block of `_ds_bundle.js` and `components/covers/WraparoundCover.jsx` to match.

Two invariants are built in and cannot be defeated by props:

- **The front-cover title never wraps to a second line.** Its font size is solved from the title's own character count (capped at the calibrated maximum), the same fit formula `gen_covers.py` uses.
- **Spine text is sized in fixed pixels at the calibration's own reference resolution, scaled only by the preview's overall height — never by that title's own spine width.** Every title's spine text renders at the same physical size: title 62px, series name and imprint 56px, diamonds 12px at 300dpi. Pass two covers with very different page counts side by side (see the preview) and their spine type should look identical in size.

## What this component does NOT do

It renders the calibrated **typography and layout system** — panel keylines, text placement, sizing — over a flat background color, for fast, accurate preview and iteration. It does not render the mottled-texture/duotone-photo background treatment (see the `CoverBlendMottlePairings` and `CoverTreatments` components) or produce a print-ready file. For an actual deliverable PDF, the build still goes through the cover pipeline in `assets/applied-covers/README.md`, which composites this same layout over the full background treatment at 300dpi. Use this component to check a new title's copy, title length, and page-count-driven spine width before running that pipeline — not as a replacement for it.

## Props

| Prop | Type | Default | Notes |
|---|---|---|---|
| `view` | `'full' \| 'front' \| 'back' \| 'spine'` | `'full'` | `'full'` renders back + spine + front side by side, matching the real wrap's left-to-right order. |
| `height` | `number` (px) | `480` | Drives every other measurement — panel width, spine width, and all font sizes scale from this one number, matching the calibration's own reference proportions. |
| `pages` | `number` | `150` | Page count; spine width = `pages × 0.0025in` (cream paper) scaled to `height`, exactly as `gen_covers.py` computes it. |
| `bg` | CSS color | `'#241a12'` | Panel background color (flat — see "What this does NOT do" above). |
| `title` | `string` | `'Title'` | Front-cover and spine title. Sized to always fit on one line regardless of length. |
| `tagline` | `string` | `''` | Italic line under the title. |
| `themeLine` | `string` | `''` | The gold "FROM DUST TO —" line near the foot of the front panel. |
| `kicker` | `string` | `'A STUDY OF'` | e.g. `'PART ONE · A STUDY OF'`. Also used as the back panel's kicker unless `backKicker` is set. |
| `publisher`, `seriesName`, `byline`, `kindLine`, `teamLine` | `string` | series defaults | Rarely need overriding — same on every title. |
| `anchorText`, `anchorRef` | `string` | Psalm 119:25 (NKJV) | The anchor-verse pull-quote shown on both front and back panels. |
| `backKicker`, `backHook`, `backParaOne`, `backParaTwo` | `string` | `''` | Back-panel kicker, italic hook line, and the two body paragraphs. |
| `backItems` | `string[]` | `[]` | The "EACH WEEK INCLUDES" diamond-bulleted list. |
| `footerName`, `footerSub` | `string` | byline / publisher line | Back-panel footer, two lines. |

## Usage

```js
React.createElement(StudyPlatformDesignSystem_d2afba.WraparoundCover, {
  view: 'full',
  height: 360,
  pages: 219,
  bg: '#241a12',
  title: 'Out of the Dust',
  tagline: 'Named in the Dust, Raised in Christ',
  themeLine: 'FROM DUST TO UNION',
  kicker: 'PART ONE · A STUDY OF',
  backHook: 'A man does not dust himself off. He is raised.',
  backParaOne: '...',
  backParaTwo: '...',
  backItems: ['A Scripture Study Dive essay', '...'],
});
```
