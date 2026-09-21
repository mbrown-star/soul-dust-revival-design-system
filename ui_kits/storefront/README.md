# Storefront UI kit

Recreates the customer-facing commerce surfaces from `study-platform-scaffold`: a product grid, cart drawer, checkout, and order-success page. Composed from `components/forms/Button.jsx`, `components/data-display/ProductRow.jsx`, and `components/feedback/StatusMessage.jsx` — no new primitives invented.

Behavior notes from source (`README.md`, `app/(marketing)/checkout/*`):
- Digital items in the cart require login before checkout; physical-only carts allow guest checkout with just an email.
- Order composition (physical / digital / mixed) drives what the success page shows.
