# Skincare-first release verification — 2026-10-18

Implemented: skincare-first home, AM/PM routine toggle, skin diary entry points, 140-item skincare discovery, six-step photo routine composer, private save/edit, draft persistence, JSON import/export, optional product links, and configurable future affiliate offers with disclosure. Existing beauty analysis and shelf flows remain available.

Verification: 21 regression checks and 6 focused routine/commerce checks pass; JavaScript syntax checks and git diff --check pass. Browser checks at 360 and 390 px covered home, community layout, photo upload/compression, two-step reorder (photo/product identity preserved), private save, reload persistence, editing entry, AM/PM switching, and skincare-only filters. Export download event was not confirmed by the browser tool. No real-account cross-device login or public posting test was completed.

Public sharing is NOT active: the existing Supabase REST endpoint reports missing routine_posts (PGRST205). Apply supabase/skincare-routines.sql using project admin access, then verify anonymous read, authenticated publish, owner-only deletion, and cross-account visibility. SQL has been reviewed but not executed. UI clearly distinguishes private save from public publish and retains drafts on failed publication.

Merchant is undecided. data/offers.js is intentionally empty; existing official product/source links are ordinary links, not affiliate links. Configure verified merchant URLs before claiming commission tracking is live.

An independent review agent could not finish because of the account usage limit. Self-review checked input escaping, photo limits, private-save rollback, publish retry IDs, account-switch races, RLS ownership, and compatibility with existing data. Public feed pagination, moderation/reporting, and image object storage are future scale work.
