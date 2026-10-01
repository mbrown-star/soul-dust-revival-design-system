import * as React from "react";
export interface WraparoundCoverProps {
  /** `full` renders back + spine + front side by side, matching the real wrap's left-to-right order. */
  view?: "full" | "front" | "back" | "spine";
  /** Pixel height. Drives every other measurement (panel width, spine width, font sizes). */
  height?: number;
  /** Page count. Spine width = pages × 0.0025in (cream paper), scaled to `height`. */
  pages?: number;
  /** Flat panel background color. The mottle/duotone treatment is not rendered. */
  bg?: string;
  title?: string;
  tagline?: string;
  themeLine?: string;
  kicker?: string;
  publisher?: string;
  seriesName?: string;
  byline?: string;
  kindLine?: string;
  teamLine?: string;
  anchorText?: string;
  anchorRef?: string;
  backKicker?: string;
  backHook?: string;
  backParaOne?: string;
  backParaTwo?: string;
  backItems?: string[];
  footerName?: string;
  footerSub?: string;
}
export function WraparoundCover(props: WraparoundCoverProps): JSX.Element;
