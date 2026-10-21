# Research: realtime mini models (OpenAI), 2026-10-06

Sources seen 2026-10-06. Research by general-web-search-agent, saved by the lead (the agent's environment did not allow writing the file).

## Answer

gpt-realtime-2.1-mini (released 2026-07-06) costs exactly the same as gpt-realtime-mini (audio input $10, output $20 per 1M tokens). It is a "distilled reasoning model" with a 128k context instead of 32k and supports reasoning.effort (default low according to an OpenAI staff member). The old gpt-realtime-mini has an official removal date of 2027-01-20 with gpt-realtime-2.1-mini as the recommended successor. No official OpenAI benchmark of conversation quality or instruction following exists for 2.1-mini; community reports mention regressions versus the old mini in rigidly structured prompts.

## Table

| Model | Release | Audio in / cached / out ($ per 1M) | Reasoning | Voices |
|---|---|---|---|---|
| gpt-realtime-mini (alias, points to snapshot 2025-12-15) | 2025-10-06 (alias moved 2026-01-13) | 10.00 / 0.30 / 20.00 | none | shared Realtime list, incl. marin and cedar |
| gpt-realtime-mini-2025-10-06 | 2025-10-06 (shut down 2026-07-23) | same | none | same |
| gpt-realtime-mini-2025-12-15 | 2025-12-15 | same | none | same |
| gpt-realtime-2-mini | does not exist | | | |
| gpt-realtime-2.1-mini | 2026-07-06 | 10.00 / 0.30 / 20.00 | yes, minimal/low/medium/high/xhigh, default low | same |
| gpt-realtime-2.1 (comparison) | 2026-07-06 | 32.00 / 0.40 / 64.00 | yes, default low | same |

Text: 2.1-mini and mini: input $0.60, cached $0.06, output $2.40. gpt-realtime-2.1: input $4.00, cached $0.40, output $24.00.

## Findings

1. Pricing for 2.1-mini, mini and 2.1 matches in two places: https://developers.openai.com/api/docs/pricing and the announcement https://community.openai.com/t/new-realtime-models-on-the-api-gpt-realtime-2-1-and-gpt-realtime-2-1-mini/1385896 (2026-07-06, OpenAI staff). Model page "Quick comparison" 2.1 Mini vs GPT-Realtime Mini: same text prices. https://developers.openai.com/api/docs/models/gpt-realtime-2.1-mini. Confidence: high.
2. gpt-realtime-2.1 costs the same as gpt-realtime-2. Confidence: high.
3. Changelog https://developers.openai.com/api/docs/changelog: "Oct 6, 2025: Released GPT-Realtime mini"; "Jan 13, 2026: Updated the gpt-realtime-mini slug to point to the 2025-12-15 snapshots"; "Jul 6, 2026: Released GPT-Realtime-2.1 ... Also released GPT-Realtime-2.1 mini, a faster, lower-cost distilled reasoning model for realtime voice applications." Confidence: high.
4. Alias gpt-realtime-mini points to gpt-realtime-mini-2025-12-15 today. Confidence: high.
5. gpt-realtime-2-mini is not in the changelog, the API reference or the pricing page. Confidence: medium (negative evidence).
6. Deprecations https://developers.openai.com/api/docs/deprecations: "Jan 20, 2027 | gpt-realtime-mini | gpt-realtime-2.1-mini" (also gpt-realtime -> gpt-realtime-2.1). Side note: tts-1, tts-1-hd, gpt-4o-mini-tts removal on 2027-01-06. Confidence: high.
7. Context and output: 2.1-mini 128,000 context, 32,000 max output, cutoff Sep 30, 2024. gpt-realtime-mini 32,000 context, 4,096 max output. Confidence: high.
8. 2.1-mini description: "a distilled reasoning model for faster, lower-cost realtime voice interactions. It supports audio and text inputs over WebRTC, WebSocket, or SIP connections and improves alphanumeric recognition over GPT-Realtime-2." Function calling and prompt caching supported. Confidence: high.
9. reasoning.effort enum in the API reference: minimal, low, medium, high, xhigh. Default low per OpenAI staff (2026-07-22, https://community.openai.com/t/gpt-realtime-model-default-reasoning/1387803), not in the reference. Set it explicitly. Confidence: medium.
10. Voices: "alloy, ash, ballad, coral, echo, sage, shimmer, verse, marin, and cedar. For best quality, we recommend using marin or cedar." No per-model voice matrix found. https://developers.openai.com/api/docs/guides/realtime-conversations. Confidence: medium.
11. Latency: only "reduced p95 latency by at least 25% across Realtime voice models through improved caching" (staff, 2026-07-06). No absolute numbers.
12. Prompting guide https://developers.openai.com/api/docs/guides/realtime-models-prompting: "Start with low for most production voice agents"; "gpt-realtime-2 generates preambles by default"; migration: "treat the prompt as a behavior surface ... Set reasoning effort to low ... Remove stale examples ... Compare representative conversations before and after migration." OpenAI support (2026-05-26): no dedicated mini prompting guide; "keep prompts shorter", "simplify tool instructions" (https://community.openai.com/t/prompting-guide-gpt-real-time-mini/1381758). Confidence: medium.
13. Known issues, community only (not staff), same announcement thread: one production outbound agent moved from realtime-mini to 2.1-mini reported instruction leakage ("Let me continue with the call..."), commentary-channel narration, literal matching of prompt examples, less stable conditional flow; reverting to realtime-mini fixed it. Another reported 2.1-mini "respects prompt rules more consistently" but stopped calling functions in a SIP flow. Confidence: low to medium.
14. Third-party benchmark (Cekura, updated 2026-09-29, 2,460 simulated calls): gpt-realtime-2.1 89.0% vs 2.1-mini 61.4% overall, almost all of the gap from one category; median response 1.94 s vs 2.08 s. https://benchmarks.cekura.ai/speech-to-speech/compare/openai-realtime-vs-openai-realtime-mini. Does not compare with gpt-realtime-mini. Confidence: low.

## Not found

- An official OpenAI benchmark for 2.1-mini, or any comparison 2.1-mini vs mini vs 2.1.
- Official multilingual (Polish) quality data for 2.1-mini.
- How reasoning and commentary (preamble) tokens are billed in Realtime: same per-token price, but per-conversation cost can change if 2.1-mini emits more output tokens. Not measured.
- Official confirmation that gpt-realtime-mini rejects the reasoning field (seen only in third-party repos).
- A voice x model matrix.

## Recommendation (researcher)

Migration away from gpt-realtime-mini is required before 2027-01-20 anyway, and gpt-realtime-2.1-mini is the official successor at the same per-token price. "Better quality" is not proven by OpenAI and community reports mention regressions with rigidly structured prompts. Before switching, A/B on real MindSync scenarios in Polish and English: set reasoning.effort explicitly (low, also try minimal for latency), keep the prompt short, no examples inside transition conditions, check the model never speaks instructions aloud, and compare cost per conversation from response.done usage.

## Sources

1. https://community.openai.com/t/new-realtime-models-on-the-api-gpt-realtime-2-1-and-gpt-realtime-2-1-mini/1385896
2. https://developers.openai.com/api/docs/models/gpt-realtime-2.1-mini
3. https://developers.openai.com/api/docs/models/gpt-realtime-mini
4. https://developers.openai.com/api/docs/models/gpt-realtime-2.1
5. https://developers.openai.com/api/docs/pricing
6. https://developers.openai.com/api/docs/changelog
7. https://developers.openai.com/api/docs/deprecations
8. https://developers.openai.com/api/reference/resources/realtime/subresources/client_secrets/methods/create
9. https://developers.openai.com/api/docs/guides/realtime-models-prompting
10. https://developers.openai.com/api/docs/guides/realtime-conversations
11. https://developers.openai.com/api/docs/guides/realtime-costs
12. https://community.openai.com/t/gpt-realtime-model-default-reasoning/1387803
13. https://community.openai.com/t/prompting-guide-gpt-real-time-mini/1381758
14. https://benchmarks.cekura.ai/speech-to-speech/compare/openai-realtime-vs-openai-realtime-mini
