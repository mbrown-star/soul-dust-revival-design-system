# Admin Console UI kit

The internal management tool from `study-platform-scaffold`: products list/form, studies list/detail with a drag-and-drop lesson block editor (text/image/video/audio/question/callout), and the manual-vs-import tabs for creating a study. Composed from `components/forms/*`, `components/navigation/Tabs.jsx`, `components/data-display/ProductRow.jsx` — no new primitives invented.

Gated by `users.is_admin` in source; no self-serve "become an admin" flow.
