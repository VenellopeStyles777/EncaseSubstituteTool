# Fixtures

Purpose: tiny legal fixtures and fixture-generation notes for tests.

Rules:

- Do not commit private or real case evidence.
- Prefer generated dummy files and mocked EWF adapters for Stage 1.
- Keep fixtures small enough for Git.

Stage 1 fixture policy:

- S1-T02 should use temporary dummy segment files created during tests, such as `sample.E01`, `sample.E02`, and `sample.E04`.
- Dummy segment files do not need real EWF bytes for segment-discovery tests.
- Do not commit large E01 files.
- Do not commit real evidence.
- If a stable mock fixture becomes necessary, keep it tiny, clearly fake, and document why it is committed.
