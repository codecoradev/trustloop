# Orders list moves to cursor pagination

Date: 2026-09-02
Status: Accepted

Decision: GET /orders returns `next_cursor` (opaque, encodes created_at and id) and accepts `cursor` and `limit`. `offset` stays accepted for one release, then is removed.

Why: offset scans timed out above 1M rows (incident INC-77); clients saw duplicates when new orders arrived between pages.
