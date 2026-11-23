# Exports are idempotent per job

Date: 2026-11-01
Status: Accepted

Decision: an export job writes to a temporary file in the same directory and renames it over the target when done (atomic replace). Re-running a job with the same job id must produce the same file, never a longer one.

Why: the scheduler retries jobs after a timeout. Partial or appended files have reached customers twice (incidents INC-41, INC-52).

Rejected: append mode with a de-duplication pass afterwards (racy, and a crash leaves a half file).
