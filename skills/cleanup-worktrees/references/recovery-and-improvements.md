# Recovery and improvements

## Recovery

Each recovery directory contains manifest.json, history.bundle, staged.patch,
unstaged.patch and untracked.tar.gz. The manifest records HEAD, branch, status,
file hashes and restoration verification. Keep these private; do not upload.

Create a new isolated checkout at the saved HEAD using the bundle. Apply the
staged patch with git apply --index, then the unstaged patch with git apply.
Extract reviewed untracked files without escaping the checkout root. Verify
manifest hashes and read the sidelined packet. Reconcile with current Dev;
old deployment/environment claims remain historical.

Dependencies and build caches can be regenerated from retained lockfiles.
Record secret/config bindings by path and retained source, without values.

## Included improvements

- Actual chat message dates instead of folder/sidebar update dates.
- All owning chats and child chats checked together.
- Restorable code preservation, including unmerged and dirty work.
- Restore proof before removal and closeout proof before claiming completion.
- Ownership evidence with uncertain mappings preserved separately.
- One feature group at a time and a durable, resumable action ledger.
- Physical free-space gain separated from folder allocation.
- Generated activity shown separately to explain misleading recency.

## Optional next refinements

- A selectable table with age, size, owners, merge state and recovery status.
- An optional grace window after sidelining; direct authorized cleanup remains
  immediate by default.
- A scheduled audit notifying only on actionable candidates, if requested.
- Checkout-sweep detection from clustered file timestamps plus old commits.
- Cached metadata and targeted scans to avoid expensive global scans.
- A user-chosen encrypted recovery backend and retention period, with restore
  proof before deletion.

These do not automatically authorize scheduling, external uploads, spending,
deployments, provider writes, or deleting recovery artifacts.
