# GLOWME

Mobile beauty journal and personal beauty shelf, deployed at https://glowme-bice.vercel.app/.

## Run and verify

Serve this directory with `python -m http.server 8000`, then open http://localhost:8000. No build step or npm dependencies are required. Run `node tests/regression.cjs` for regression checks.

## Features

- Editorial home with categories, real product photography, magazine articles and daily routines.
- Six face-shape guides with distinct illustrated models and blush/contour placements.
- Four facial-proportion comparisons, each with hairstyle and makeup references.
- Four skin texture references with answer-based reasoning and care guidance.
- Seasonal palettes, realistic hair-texture swatches and shade-specific lip, blush and eye recommendations.
- Twelve official rom&nd product variants with local photos, exact shade names and official variant links.
- Existing Supabase login and user_data sync, personal shelf, AM/PM routines, custom product registration, analysis history and JSON backup/import.

## Structure

`app.js` retains application state, questionnaires, authentication and persistence. `ui.js` renders editorial screens. `styles.css` provides responsive styling. `data/editorial.js` maps images to guidance; `data/products.js` maps verified variants to photos. `sw.js` caches the static app for offline use.

## Image and recommendation provenance

Human illustrations, skin references, hair swatches and the photorealistic home hero are AI-generated educational/editorial assets, explicitly labeled in the app. They are not clinical photographs or real product photographs. Product images come from official romandbeauty.com variant records. See `docs/product-evidence.json`, `docs/source-*.json` and `docs/image-provenance.json`. Seasonal pairings are editorial recommendations, not manufacturer-certified personal-color classifications.

## Existing backend

Supabase setup is described in `supabase/schema.sql`. The browser uses a publishable key only. Live authentication, RLS and cross-device synchronization need an authorized test account to verify end to end. Product review requests depend on the existing backend table and policies. Community remains local drafts rather than a public social backend.

## Validation

See `docs/qa-report.md` for tested flows and remaining limitations. Questionnaire results are styling/self-observation guidance, not photographic analysis or medical diagnosis.
