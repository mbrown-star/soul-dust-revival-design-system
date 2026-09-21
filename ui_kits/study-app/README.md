# Study App UI kit

The gated, interactive study experience from `study-platform-scaffold`: passwordless (magic-link) login, a studies index, and a lesson viewer rendering every content-block type (text, image, video, audio, question, callout) plus a progress bar. Composed from `components/forms/*`, `components/feedback/*` — no new primitives invented.

Access model from source: lessons require login (`app/(study-app)/studies/[slug]/[lessonId]/page.tsx`) and a purchase entitlement; unentitled users are sent to the purchase page instead.
