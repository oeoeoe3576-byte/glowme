# Skincare-first GLOWME

User intent: make skincare the main experience, support future affiliate commerce, and let skincare community posts present step-by-step photos.

- Home: today's AM/PM routine, skin check-in, care builder, skincare product discovery and routine community. Keep color/face analysis reachable.
- Product cards: configurable per-product offers, safe HTTPS links, explicit affiliate disclosure only for configured affiliate offers. No invented partner IDs/prices or tracking personal skin data.
- Community: skincare routine composer, 1–6 ordered steps with title, instructions, optional compressed photo and catalog product. Draft persistence through existing private state; local saved posts remain accessible. Editor examples clearly labeled.
- Public sharing: separate routine_posts table with authenticated ownership, published-only public read, JSON schema/size constraints. Configure backend only when project access is available; fail honestly when unavailable. Public action is distinct from private save.
- Validation: test URL validation, affiliate attribution, step schema, ordering, import limit, legacy posts, routine import and duplicate prevention. Mobile browser verifies home, categories, compose/edit/reorder/photo preview, save/detail and purchase links. Preserve auth and saved analysis tests.

Implementation order: commerce and validation helpers; skincare home; routine editor/detail + backend adapter/schema; mobile QA; independent review; deployment.
