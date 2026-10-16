# GLOWME implementation plan — 2026-10-16

Goal: implement the approved mobile shopping/editorial redesign in the existing PWA without replacing account or local data storage.
Architecture: retain existing auth and storage functions; extract stylesheet and app script; load explicit editorial and verified-product catalogs before app startup.

- [x] Add regression tests for face answer semantics, unknown answers, color depth, saved skin reports, and preserved shelf/routine flows.
- [x] Generate and inspect six distinct face/makeup triptychs, four ratio comparisons, skin texture references, hair texture samples and home hero.
- [x] Verify official product variant identifiers, names and images. Save source evidence and optimized local images.
- [x] Implement responsive home, reports, magazine and image-backed product/shelf components. Remove obsolete drawing assets and CSS.
- [x] Run automated regressions and actual browser checks at 360, 390, 430px. Test every result type and relevant existing flows.
- [ ] Review final diff, commit/push authorized changes, verify Vercel production deployment and live mobile rendering.

Constraints: no fabricated product photos; no CSS drawing replacements; generated references clearly labeled; retain storage key glowme_mvp_v1 and Supabase user_data schema; no credentials or account creation in tests.

Review focus: uncertain results, wrong face scoring, different product variants, mobile clipping, old saved records without new metadata, offline updates.

Ruling: proceed inline per user instruction; no extra design approval round. Existing clone is isolated to this task, initially clean at fcb7797.

