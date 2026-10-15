# GLOWME — Working PWA prototype

A dependency-free, English-first, mobile-focused GLOWME beauty app prototype.

## Included
- Today: AM/PM routine checklists and completion progress
- Analyze: 3-question face-style and color-preference explorers, save results
- Beauty Lab: educational beauty guides
- Community: locally saved post drafts, filter, like and delete (NOT public/social)
- My Beauty: skin profile, product shelf, AM/PM routine builder, skin diary
- Local JSON export and complete data deletion
- Installable PWA manifest and service worker

## Run locally
Run `python3 -m http.server 8000` inside this directory, then open `http://localhost:8000`.

## Important limitations
- No backend, accounts, cross-device sync, real community, payment, affiliate links, camera AI, or automatic product database.
- All data stays in the browser's localStorage; clearing browser data removes it.
- Educational style exploration only, not diagnostic AI or medical advice.
- The sample community posts are fictional placeholders, not real people.

## Production next steps
1. Choose a commercial-use-permitted hosting plan and deploy via GitHub.
2. Add Supabase Auth, row-level-security, cloud persistence and backups.
3. Build moderation/report/blocking workflows before enabling public community posting.
4. Privacy policy, terms, deletion controls, security audit and accessibility QA.
5. Add monetization only after validation, with explicit user approval for costs.

## Iteration 2 improvements
- Browser-local date calculation (avoids UTC date rollover issues).
- Prevents duplicate product names, case-insensitively.
- Replaces the day's diary entry instead of creating multiple entries.
- JSON backup import (max 1 MB) with basic schema checks and explicit overwrite confirmation.
- Updated service worker cache version to v2.

## Deployment status (2026-10-15)
Not deployed. Connected GitHub returned no accessible repositories; connected Vercel team uses Hobby plan, which is not appropriate to assume for a commercial service. No payment or plan upgrade authorized.

## Important security note
The JSON importer checks top-level structure but is not a secure trust boundary for untrusted backups. This browser-local demo is not ready for public multi-user use. Before cloud launch: replace inline event handlers, implement a proper backend with authentication/RLS, rate limits, content moderation, and production QA.


## Supabase account sync (v3)

The app uses Supabase Auth and `public.user_data` with row-level security. Apply the SQL in `supabase/schema.sql` before testing. Confirm the Supabase Auth Site URL matches the deployed site. Email verification may be required. Personal data is stored per signed-in user. Community posts remain local drafts only, not a multi-user backend. Supabase publishable key is safe for browser use; never add secret/service-role keys to the frontend.
