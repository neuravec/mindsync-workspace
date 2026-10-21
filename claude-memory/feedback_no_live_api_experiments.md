---
name: No live API experiments on production
description: Never push untested API migration changes directly to production — use staging or separate endpoints first
type: feedback
---

Do not push experimental API changes (e.g., OpenAI endpoint migrations) directly to production. The Realtime API migration from `/v1/realtime/sessions` to `/v1/realtime/client_secrets` broke voice features for a full day because each body format attempt was deployed live.

**Why:** Production was down for 24+ hours while iterating on the correct request body format. Multiple deploy cycles with wrong parameters (`session.voice`, `session.input_audio_noise_reduction`, flat `model`).

**How to apply:** When migrating external API endpoints, first verify the new format works (e.g., with a test script or staging env) before touching production code. If unsure, revert to working version and develop the new version under separate endpoints (e.g., `/v2/`) until validated.
