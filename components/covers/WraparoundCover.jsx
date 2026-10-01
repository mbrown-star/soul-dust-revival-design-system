import React from "react";

// Mirrors assets/applied-covers/calibration.json. Originally hand-authored directly into the
// Claude design system's bundle; promoted here into a real source file with unchanged behavior.

const CREAM = '#EFE6C2';
const GOLD = '#B08D2E';
const GOLD2 = '#AD9A5F';
const REF_FULLH = 3375;  // calibration.json's reference: 11in trim + 0.25in bleed @ 300dpi
const REF_PANEL = 2588;  // 8.5in trim + 0.125in bleed @ 300dpi
const SPINE_MULT = 0.75; // page count * 0.0025in (cream paper) * 300dpi

// Mirrors calibration.json's keyline / back_panel / front_panel / spine sections
// (assets/applied-covers/calibration.json). This component and gen_covers.py
// are two renderers of the SAME calibrated numbers, not two independent designs --
// if calibration.json is ever re-measured against a revised reference cover, update
// the constants below to match, the same way gen_covers.py would be updated.
const CAL = {
  keyline: { tb: 0.065, lr: 0.07, gap: 0.006 },
  back: { padTop: 0.065 + 0.085, padBottom: 0.065 + 0.085, padX: 0.10 },
  front: {
    fPub: 0.011, fSeries: 0.0255, fTag: 0.0222, fByline: 0.0228,
    fTitleMax: 0.081, fTitleMin: 0.05, titleWeight: 500,
    yPub: 0.13, ySeries: 0.175, yDia: 0.22, yKicker: 0.35, yTitle: 0.42,
    yTag: 0.50, yRule: 0.545, yByline: 0.585, yAnchor: 0.64, yTheme: 0.825, yKind: 0.874,
  },
  // Fixed absolute px @ 300dpi -- see calibration.json spine.critical_rule: NEVER
  // scale these by a title's own spine width or the series' narrowest spine width.
  // Scaled here only by the preview's own height vs. the 300dpi reference height,
  // which is the one scaling that keeps every title's spine text physically identical.
  // As rendered on the shipped covers (calibration.json spine, rebuilt 2026-10-01).
  spine: { series: 56, dia: 12, title: 54, team: 54 },
};

// Same single-line-fit rule as gen_covers.py's f_title_fit: capped at the
// calibrated maximum, scaled down only as far as needed to keep the title on one
// line (never let it wrap -- the tagline/rule/byline below sit at fixed offsets that
// assume a one-line title; this is the exact bug the seventh build pass fixed).
function fitTitlePx(title, availableWidth, fullH) {
  const max = CAL.front.fTitleMax * fullH;
  const min = CAL.front.fTitleMin * fullH;
  const fit = (availableWidth * 0.92) / (Math.max(1, title.length) * 0.52);
  return Math.max(min, Math.min(max, fit));
}

function Keyline(el, w, h) {
  const keyTB = CAL.keyline.tb * h, keyLR = CAL.keyline.lr * w, keyGap = CAL.keyline.gap * h;
  const weight = Math.max(1, h * 0.0012);
  return el('div', { style: { position: 'absolute', top: keyTB, left: keyLR, right: keyLR, bottom: keyTB, border: `${weight}px solid ${GOLD2}`, pointerEvents: 'none' } },
    el('div', { style: { position: 'absolute', top: keyGap, left: keyGap, right: keyGap, bottom: keyGap, border: `${weight}px solid ${GOLD2}` } })
  );
}

function FrontPanel({ w, h, bg, publisher, seriesName, kicker, title, tagline, byline, anchorText, anchorRef, themeLine, kindLine }) {
  const el = React.createElement;
  const padX = CAL.back.padX * w;
  const titlePx = fitTitlePx(title, w - 2 * padX, h);
  const line = (text, extra) => el('div', { style: { position: 'absolute', left: 0, width: '100%', textAlign: 'center', color: CREAM, whiteSpace: 'nowrap', ...extra } }, text);
  return el('div', { style: { position: 'relative', width: w, height: h, background: bg, overflow: 'hidden', fontFamily: 'Georgia, "Liberation Serif", serif', flexShrink: 0 } },
    Keyline(el, w, h),
    line(publisher, { top: CAL.front.yPub * h, fontWeight: 'bold', letterSpacing: '0.12em', color: GOLD2, fontSize: CAL.front.fPub * h }),
    line(seriesName, { top: CAL.front.ySeries * h, fontWeight: 'bold', letterSpacing: '0.16em', fontSize: CAL.front.fSeries * h }),
    line('◆ ◆ ◆', { top: CAL.front.yDia * h, color: GOLD2, letterSpacing: '0.5em', fontSize: h * 0.011 }),
    line(kicker, { top: CAL.front.yKicker * h, fontWeight: 'bold', letterSpacing: '0.14em', color: GOLD2, fontSize: h * 0.0135 }),
    el('div', { style: { position: 'absolute', top: CAL.front.yTitle * h - titlePx * 1.06 / 2, left: '50%', transform: 'translateX(-50%)', width: w - 2 * padX, textAlign: 'center', color: CREAM, fontWeight: CAL.front.titleWeight, fontSize: titlePx, lineHeight: 1.06, whiteSpace: 'nowrap' } }, title),
    line(tagline, { top: CAL.front.yTag * h, fontStyle: 'italic', color: GOLD2, fontSize: CAL.front.fTag * h }),
    el('div', { style: { position: 'absolute', top: CAL.front.yRule * h, left: '50%', transform: 'translateX(-50%)', width: w * 0.43, borderTop: `${Math.max(1, h * 0.0004)}px solid ${GOLD2}` } }),
    line(byline, { top: CAL.front.yByline * h, fontSize: CAL.front.fByline * h }),
    el('div', { style: { position: 'absolute', top: CAL.front.yAnchor * h, left: padX, right: padX, textAlign: 'center', fontStyle: 'italic', color: CREAM, fontSize: h * 0.0135, lineHeight: 1.35 } },
      anchorText, el('span', { style: { display: 'block', marginTop: '0.35em', fontStyle: 'normal', color: GOLD2, fontSize: '0.7em', letterSpacing: '0.08em' } }, anchorRef)
    ),
    line(themeLine, { top: CAL.front.yTheme * h, color: GOLD, fontSize: h * 0.013, letterSpacing: '0.12em', fontWeight: 'bold' }),
    line(kindLine, { top: CAL.front.yKind * h, fontSize: h * 0.0115, letterSpacing: '0.1em' })
  );
}

function BackPanel({ w, h, bg, kicker, hook, paraOne, paraTwo, items, anchorText, anchorRef, footerName, footerSub }) {
  const el = React.createElement;
  const padTop = CAL.back.padTop * h, padBottom = CAL.back.padBottom * h, padX = CAL.back.padX * w;
  const bodyFont = h * 0.0135, gapLg = h * 0.022;
  return el('div', { style: { position: 'relative', width: w, height: h, background: bg, overflow: 'hidden', fontFamily: 'Georgia, "Liberation Serif", serif', color: CREAM, flexShrink: 0 } },
    Keyline(el, w, h),
    el('div', { style: { position: 'absolute', top: padTop, left: padX, right: padX, bottom: padBottom, overflow: 'hidden' } },
      el('div', { style: { fontWeight: 'bold', letterSpacing: '0.14em', color: GOLD, fontSize: h * 0.0135 } }, kicker),
      el('div', { style: { fontStyle: 'italic', fontSize: h * 0.022, lineHeight: 1.3, marginTop: gapLg, maxWidth: w - 2 * padX } }, '“' + hook + '”'),
      el('div', { style: { fontSize: bodyFont, lineHeight: 1.5, marginTop: gapLg } }, paraOne),
      el('div', { style: { fontSize: bodyFont, lineHeight: 1.5, marginTop: gapLg } }, paraTwo),
      el('div', { style: { fontWeight: 'bold', letterSpacing: '0.08em', color: GOLD, fontSize: h * 0.0145, marginTop: gapLg } }, 'EACH WEEK INCLUDES'),
      el('div', { style: { marginTop: h * 0.012 } }, items.map((item, i) => el('div', { key: i, style: { fontSize: h * 0.0128, lineHeight: 1.42, marginTop: h * 0.009, paddingLeft: h * 0.02, position: 'relative' } },
        el('span', { style: { position: 'absolute', left: 0, top: '0.15em', color: GOLD2, fontSize: '0.8em' } }, '◆'), item
      ))),
      el('div', { style: { marginTop: gapLg, fontStyle: 'italic', fontSize: h * 0.015, lineHeight: 1.4, textAlign: 'center' } },
        '“' + anchorText + '”', el('span', { style: { display: 'block', marginTop: '0.35em', color: GOLD2, fontStyle: 'normal', fontWeight: 'bold', fontSize: '0.72em', letterSpacing: '0.05em' } }, anchorRef)
      )
    ),
    el('div', { style: { position: 'absolute', bottom: padBottom, left: 0, width: '100%', textAlign: 'center' } },
      el('span', { style: { display: 'block', fontSize: h * 0.017 } }, footerName),
      el('span', { style: { display: 'block', color: GOLD2, fontSize: h * 0.0115, letterSpacing: '0.08em', marginTop: '0.5em' } }, footerSub)
    )
  );
}

function Spine({ w, h, bg, seriesName, title, teamLine, scale }) {
  const el = React.createElement;
  const vw = { writingMode: 'vertical-rl', textOrientation: 'sideways' };
  const spTitle = CAL.spine.title * scale, spSeries = CAL.spine.series * scale, spTeam = CAL.spine.team * scale, spDia = CAL.spine.dia * scale;
  return el('div', { style: { position: 'relative', width: w, height: h, background: bg, overflow: 'hidden', flexShrink: 0 } },
    el('div', { style: { position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%,-50%)', display: 'flex', flexDirection: 'column', alignItems: 'center', fontFamily: 'Georgia, "Liberation Serif", serif' } },
      el('div', { style: { ...vw, color: GOLD, fontWeight: 'bold', fontSize: spSeries, letterSpacing: '0.14em' } }, seriesName),
      el('div', { style: { ...vw, color: GOLD2, fontSize: spDia, marginTop: h * 0.019 } }, '◆'),
      el('div', { style: { ...vw, color: CREAM, fontWeight: 600, fontSize: spTitle, letterSpacing: '0.01em', marginTop: h * 0.007 } }, title),
      el('div', { style: { ...vw, color: GOLD2, fontSize: spDia, marginTop: h * 0.010 } }, '◆'),
      el('div', { style: { ...vw, color: GOLD2, fontSize: spTeam, letterSpacing: '0.1em', marginTop: h * 0.035 } }, teamLine)
    )
  );
}

/**
 * WraparoundCover -- a reusable, parametrized render of the Soul Dust Revival
 * wraparound cover typography system (front panel, back panel, spine), built from
 * the exact numbers in calibration.json rather than a fresh approximation. Pass a
 * title's own content and page count; the component derives spine width, per-title
 * front-cover title size (never wrapping to a second line), and spine text sized at
 * the calibrated fixed pixel values -- scaled only by the preview's own height, so
 * every title's spine text stays physically identical to every other title's, the
 * same invariant gen_covers.py's print pipeline enforces.
 */
export function WraparoundCover(props) {
  const {
    view = 'full',
    height = 480,
    pages = 150,
    bg = '#241a12',
    publisher = 'MARKETLIFE MINISTRIES',
    seriesName = 'SOUL DUST REVIVAL',
    kicker = 'A STUDY OF',
    title = 'Title',
    tagline = '',
    byline = 'The Soul Dust Team',
    anchorText = 'My soul clings to the dust;\nRevive me according to Your word.',
    anchorRef = 'PSALM 119:25 (NKJV)',
    themeLine = '',
    kindLine = 'A TWELVE-WEEK TOPICAL STUDY',
    backKicker = kicker,
    backHook = '',
    backParaOne = '',
    backParaTwo = '',
    backItems = [],
    footerName = byline,
    footerSub = 'MARKETLIFE MINISTRIES · MARKETLIFEMINISTRIES.ORG',
    teamLine = 'THE SOUL DUST TEAM',
  } = props;

  const el = React.createElement;
  const scale = height / REF_FULLH;
  const panelW = REF_PANEL * scale;
  const spineW = Math.max(pages * SPINE_MULT * scale, 8);

  const front = () => FrontPanel({ w: panelW, h: height, bg, publisher, seriesName, kicker, title, tagline, byline, anchorText, anchorRef, themeLine, kindLine });
  const back = () => BackPanel({ w: panelW, h: height, bg, kicker: backKicker, hook: backHook, paraOne: backParaOne, paraTwo: backParaTwo, items: backItems, anchorText, anchorRef, footerName, footerSub });
  const spine = () => Spine({ w: spineW, h: height, bg, seriesName, title, teamLine, scale });

  const panels =
    view === 'front' ? [front()] :
    view === 'back' ? [back()] :
    view === 'spine' ? [spine()] :
    [back(), spine(), front()];

  return el('div', { style: { display: 'flex', boxShadow: '0 4px 24px rgba(0,0,0,0.35)' } }, panels);
}
