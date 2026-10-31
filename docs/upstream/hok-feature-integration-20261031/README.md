# HOK feature integration source snapshot - 2026-10-31

Immutable upstream delta: `860efe7a3513148dc6964b7e0e3dfafd19addfb7` -> `07de265c1e992abb6584bdfcdf140320188c07f9`. All source snapshots retain exact Git blob bytes. Their source hashes, blob IDs, classifications and expected compatibility outputs are recorded in `tools/hok_feature_update_lock.json`.

`runtime/` and `documents/` are donor evidence. `previous/` preserves the five exact compatibility ancestors used for narrow merges. `integrated/` stores reviewed expected output bytes, including migrated Korean state/province references and new British English localisation. Source English files containing Korean fallback text remain unchanged in `runtime/`. The English naval-captain fallback is classified `USE_RT56` and has no runtime output; its 13 shared vanilla UI keys retain host English. Korean fallback text is retained.

The four donor history updates are recorded as already implemented doctrine migrations and produce no new history output. Existing RT56 Hanjin organisation access rules and corrected lower-case event IDs remain in merged outputs. No donor descriptor identity or broad runtime tree is imported.

The donor validation records describe donor-only runs. They are provenance, not validation of this RT56 port. Current civil nuclear content uses 35 + 245 days, without the historical five-day discount; earlier 240-day runtime evidence does not validate the final reward/period revision.
