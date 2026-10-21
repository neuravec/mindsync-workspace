# Research: making the OpenAI Realtime voice sound natural and warm (MindSync / "Orca")

Date of research: 2026-10-05 (every "seen" date below = 2026-10-05).
Method: WebFetch on current official pages (developers.openai.com docs, API reference, changelog, deprecations, OpenAI Developer Community announcement posts). WebFetch returns small-model summaries, so quotes below are as reported by the fetch; the key ones were cross-checked by fetching the same page twice with different prompts.
Typography note: source quotes contain en/em dashes in a few places ("2-3", "frustrating, let's fix it"); these were normalised to hyphen/comma here. The originals use a dash.

Evidence-level legend: [DOC] = official OpenAI documentation/API reference; [STAFF] = official OpenAI staff/announcement post on community.openai.com; [3P] = third-party article/benchmark; [FORUM] = developer forum report, a lead only, never proof.

---------------------------------------------------------------------
## 0. Key context discovered (not asked, but material)

- gpt-realtime-2.1 exists (released 2026-07-06). gpt-realtime-2 released 2026-05-07. gpt-realtime-1.5 released 2026-02-23 (non-reasoning).
- GPT-Live (gpt-live-1), a NEW full-duplex voice model, went GA on 2026-09-10. It is NOT a drop-in for our case: documented voices are English and Brazilian Portuguese only (see Q1 section D).
- DEPRECATION that hits us: `gpt-4o-mini-transcribe` (our transcription model) is removed 2027-02-26, replacement `gpt-live-transcribe` or `gpt-transcribe`. Original `gpt-realtime` is removed 2027-01-20. gpt-realtime-2 and gpt-realtime-1.5 are NOT in the deprecation list.
  Source [DOC]: https://developers.openai.com/api/docs/deprecations (seen 2026-10-05). Quote: "On August 26, 2026, we notified developers using `whisper-1`, `gpt-4o-transcribe`, `gpt-4o-mini-transcribe`, and `gpt-4o-transcribe-diarize` of their deprecation and removal from the API on February 26, 2027." Table row: "Feb 26, 2027 | gpt-4o-mini-transcribe | gpt-live-transcribe or gpt-transcribe". Second entry: "On July 20, 2026 ... removal from the API on January 20, 2027": gpt-realtime -> gpt-realtime-2.1; gpt-realtime-mini -> gpt-realtime-2.1-mini. Confidence: high.
  Caveat: https://developers.openai.com/api/docs/guides/realtime-transcription says "Start with `gpt-live-transcribe`" and that "gpt-live-transcribe transcription sessions require omitting or setting turn_detection to null" (that sentence is about transcription-type sessions; I did NOT verify how gpt-live-transcribe behaves as `audio.input.transcription.model` inside a speech-to-speech conversation session, even though the API reference enum lists it there). Confidence on this caveat: medium.

---------------------------------------------------------------------
## Q1. Voices, model versions, quality, Polish

### A. Does gpt-realtime-2.1 exist, what changed vs 2
- Yes. "gpt-realtime-2.1 updates GPT-Realtime-2 with improved alphanumeric recognition, silence and noise handling, and interruption behavior." Also "we've also reduced p95 latency by at least 25% across Realtime voice models through improved caching." Released 2026-07-06 with gpt-realtime-2.1-mini.
  Source [STAFF]: https://community.openai.com/t/new-realtime-models-on-the-api-gpt-realtime-2-1-and-gpt-realtime-2-1-mini/1385896 (seen 2026-10-05). Confidence: high.
- Model page [DOC]: https://developers.openai.com/api/docs/models/gpt-realtime-2.1 : "Reasoning model with tool use"; context window 128,000; "32,000 max output tokens"; knowledge cutoff 2024-09-30; only the Realtime endpoint (`v1/realtime`); pricing per 1M tokens: text in $4, audio in $32, audio out $64. Confidence: high.
- Microsoft Foundry (3P mirror of OpenAI model, updated 2026-09-21): "`gpt-realtime-2.1` (version `2026-07-07`) is an incremental update to `gpt-realtime-2` with improved silence and noise handling." https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/realtime-2 . Confidence: medium (second independent source on the same fact).
- The official prompting guide page (https://developers.openai.com/api/docs/guides/realtime-models-prompting) still lists only two models in "Choose a model": gpt-realtime-2 and gpt-realtime-1.5. I found NO 2.1-specific prompting guide. Presumably the 2.0 guide applies. Confidence: medium.

### B. Built-in voices on the Realtime API
- API reference, `audio.output.voice` enum for realtime sessions: `alloy, ash, ballad, coral, echo, sage, shimmer, verse, marin, cedar`. Description: "The voice the model uses to respond... We recommend marin and cedar for best quality." Source [DOC]: https://developers.openai.com/api/reference/resources/realtime/subresources/client_secrets/methods/create and https://developers.openai.com/api/reference/resources/realtime/client-events (seen 2026-10-05). Confidence: high.
- fable, onyx, nova are in the TTS endpoint list (13 voices) but NOT in the Realtime enum. TTS guide: "For best quality, we recommend using `marin` or `cedar`." https://developers.openai.com/api/docs/guides/text-to-speech . Confidence: high. (One forum thread claims realtime-1.5's enum includes fable/onyx/nova; the current API reference contradicts it, trust the reference.)
- OpenAI's own WebRTC examples use marin: `{ type: "realtime", model: "gpt-realtime-2.1", audio: { output: { voice: "marin" } } }` https://developers.openai.com/api/docs/guides/realtime-webrtc and https://developers.openai.com/api/docs/guides/voice-webrtc . Confidence: high.
- Origin of marin/cedar [STAFF], 2025-08-28 gpt-realtime launch: "We've added two API voices, Cedar and Marin, and improved voice quality overall for more humanlike speech that can adapt to tone." and "our existing eight voices" were updated "to benefit from these improvements". https://community.openai.com/t/introducing-gpt-realtime-and-realtime-api-updates-for-production-voice-agents/1355039 . (openai.com/index/introducing-gpt-realtime returned HTTP 403 to WebFetch, so I used the community mirror.) Confidence: high for the quote, but see below on "lower quality".
- Descriptions "Cedar = warm mid-range male, Marin = brighter female" come from a third-party blog (Handy AI, 2026-05-12): https://handyai.substack.com/p/model-drop-gpt-realtime-2 . Confidence: low (single 3P source).

### C. Are the older voices lower quality on the new models?
- NOT stated anywhere I found. OpenAI only says (a) existing 8 voices were improved in Aug 2025, (b) "We recommend marin and cedar for best quality." The recommendation implies the other 8 are lesser, but there is no official comparative statement. Confidence: high that no explicit claim exists in what I fetched; the inference "marin/cedar are the best default" is mine.
- [FORUM] Marin/Cedar do NOT reproduce a regional dialect that coral could (Flemish Dutch): https://community.openai.com/t/bug-unexpected-behavior-marin-cedar-voices-repeat-greeting-no-dialect-flemish/1367693 (2025-11-27, no staff reply). Lead only.

### D. Non-English / Polish quality
- NO official OpenAI statement about Polish quality or accent for Realtime. Not found in: realtime guides, voices reference, announcement posts. Searched developers.openai.com docs, community announcements, and web.
- Related official statements:
  - TTS guide [DOC]: the model "generally follows the Whisper model in terms of language support", "voices being optimized for English" (https://developers.openai.com/api/docs/guides/text-to-speech). This is the TTS endpoint, not Realtime; applicability to Realtime is an inference. Confidence: medium.
  - gpt-realtime launch [STAFF]: improved at "Switching languages" (same community post as above).
  - 2.0 prompting guide [DOC]: "Language and accent should be controlled separately. A user's accent is not the same as their intended language." and "Do not infer language from accent alone. Ignore short filler sounds, backchannels, and isolated foreign words for language detection." https://developers.openai.com/api/docs/guides/realtime-models-prompting?realtime-model=gpt-realtime-2 . Confidence: high.
- [FORUM] reports (leads, none about Polish specifically):
  - "GPT Realtime 2.1 exhibits language drift" (2026-07-15 to 2026-08-08): Spanish/German spoken "with a noticeable English accent" or switching to English; PT-PT/PT-BR regression on 2.1 mini; French "drifts into a strange US/Canadian English accent whilst still speaking French"; "We have tried various prompt changes to hint to the model, but to no effect"; one user says "1.5 is much better on multi language". No OpenAI staff reply. A workaround (all context in the target language) "makes the drift appear less often, but it still appears reliably enough to be a showstopper." https://community.openai.com/t/gpt-realtime-2-1-exhibits-language-drift/1386953
  - "Gpt-realtime-2 voice is extremely slow" (2026-05-22 to 2026-09-07): worse in non-English; "the French accent is really bad compared to gpt-realtime-1.5"; but the OP's root cause was the PROMPT: "Actually my issue was that I said in the prompt 'speak slowly'!" OpenAI_Support (2026-09-07) replied with a link to the prompting guide on "the difference between playback speed and speaking style". https://community.openai.com/t/gpt-realtime-2-voice-is-extremely-slow-speaking-slowly/1381481
  - Names in the conversation can trigger language switching (2025-11): staff-adjacent advice from "juberti": use a simple instruction like "Respond in English" rather than complicated logic. https://community.openai.com/t/realtime-api-language-switching/1366289
- Takeaway for PL/DE/FR/ES/NO/SV: no official quality guarantee; only forum evidence that 2.x non-English accent can drift and that gpt-realtime-1.5 may be better in non-English. Needs an A/B listening test in our own languages. Confidence in the forum claims: low.

### E. GPT-Live (gpt-live-1), relevant because it is marketed as "natural"
- GA 2026-09-10. Changelog [DOC]: "GPT-Live 1 General Availability (Sep 10): Build full-duplex voice conversations that can continue while a backend model or agent handles reasoning." https://developers.openai.com/api/docs/changelog
- Model page [DOC] https://developers.openai.com/api/docs/models/gpt-live-1: "A full-duplex voice model for real-time conversations. It can listen and speak at the same time, and delegate reasoning and tool use to a backend agent." $0.05 per minute voice, backend billed separately; endpoint `v1/live/sessions`; languages and voices "not specified" on that page.
- Voices [DOC] https://developers.openai.com/api/docs/guides/live-conversations : 12 voices, 10 English (Australian, British, Irish, North American, Filipino, Southern U.S.) and 2 Brazilian Portuguese (bossa, tempo). Quote: "Test the voice with the languages and pronunciation your application needs." No Polish, German, French, Spanish, Norwegian or Swedish voice listed. Confidence: high that these are the documented voices; unknown whether the model can speak other languages with an English voice.
- Microsoft doc (3P mirror, updated 2026-09-30): "Quality varies by language and locale, with no guarantee of uniform quality or parity with `gpt-realtime-*`." https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/gpt-live
- Community announcement [STAFF] (2026-09-10): "GPT-Live-1 brings ChatGPT's natural, full-duplex voice conversations to the API." claims 0.798 s turn-taking latency vs 1.41 s for 2.1; testers noted "accent inconsistency in non-English languages". https://community.openai.com/t/introducing-gpt-live-1-in-the-api/1396471
- Verdict: GPT-Live is not a documented fit for our 7-language app today. Confidence: medium (absence of Polish in docs, not an explicit "unsupported").

---------------------------------------------------------------------
## Q2. Session parameters that affect how speech sounds

All from the API reference [DOC]: https://developers.openai.com/api/reference/resources/realtime/subresources/client_secrets/methods/create (also .../client-events), seen 2026-10-05, confidence high unless noted.

- `audio.output.speed`: "The speed of the model's spoken response as a multiple of the original speed. 1.0 is the default speed. 0.25 is the minimum speed. 1.5 is the maximum speed." Also: "This value can only be changed in between model turns, not while a response is in progress." No recommended value is stated by OpenAI; 1.0 is the default.
- IMPORTANT, `speed` is playback rate only. Prompting guide [DOC]: "In the Realtime API, the `speed` parameter changes playback rate, not how the model composes speech. To actually sound faster, add instructions that can guide the pacing." (https://developers.openai.com/api/docs/guides/realtime-models-prompting). Corollary documented by forum thread + staff link: putting "speak slowly" in the prompt produced half-speed speech on gpt-realtime-2 (leads, see Q1 D).
- `audio.output.voice`: built-ins above, OR a custom voice object `{ "id": "voice_123abc" }`. "Voice cannot be changed during the session once the model has responded with audio at least once." Also guide https://developers.openai.com/api/docs/guides/realtime-conversations : "Once the model has emitted audio in a session, the `voice` cannot be modified for that session." Other session properties can be changed with `session.update`. Max session length 60 minutes (same guide).
- Output format: `audio.output.format` (e.g. `{"type": "audio/pcm", "rate": 24000}`), PCM 24 kHz, G.711 PCMU/PCMA over WebSocket/SIP. Over WebRTC: "WebRTC negotiates the audio format through SDP, so omit `audio.format` from session configuration." (https://developers.openai.com/api/docs/guides/realtime-webrtc). I did not find the exact codec (Opus) stated; not confirmed.
- `max_output_tokens`: "integer between 1 and 4096 ... or `inf` ... Defaults to `inf`." Model max output is 32,000 tokens per model page. OpenAI says nothing about naturalness here (a low cap would likely cut speech mid-sentence: my inference, not documented).
- `reasoning.effort`: "minimal, low, medium, high, xhigh" ("Constrains effort on reasoning for reasoning-capable Realtime models"). The reference page lists no default. NOTE the Microsoft Foundry doc lists only minimal/low/medium/high (3P, older).
- `audio.input.transcription`: `model` (enum includes whisper-1, gpt-transcribe, gpt-live-transcribe, gpt-4o-mini-transcribe, gpt-4o-transcribe, gpt-4o-transcribe-diarize, gpt-realtime-whisper), `language` (ISO-639-1 improves accuracy), `prompt`. This is input-side only; no evidence it affects how the voice sounds. (My inference: the speech model hears audio directly.)
- `instructions`: "The default system instructions (i.e. system message) prepended to model calls. This field allows the client to guide the model on desired responses."
- Style/expressiveness controls: NO dedicated parameter in Realtime (no emotion/style knob). Expressiveness is steered only through `instructions` (and the voice choice, `speed`). Confidence: high that none appear in the reference. The TTS endpoint model gpt-4o-mini-tts does have an explicit steering prompt: "can prompt the model to control aspects of speech, including: Accent, Emotional range, Intonation, Impressions, Speed of speech, Tone, Whispering." (https://developers.openai.com/api/docs/guides/text-to-speech). That would imply a chained STT->LLM->TTS architecture; OpenAI does not claim it sounds more natural than Realtime.
- Custom voices / "voice design": https://developers.openai.com/api/docs/guides/custom-voices [DOC]
  - "Custom voices enable you to create a unique voice for your agent or application." "Custom voices are limited to eligible customers. Contact our sales team to learn more."
  - Staff, 2026-08-27 (https://community.openai.com/t/custom-voices-in-the-api-not-available/1377611): OpenAI "removed the enterprise-only eligibility wording from the documentation" but "Custom Voices can still only be enabled for eligible/approved customers, and the documented path to request enablement is through OpenAI Sales."
  - Process: a consent recording (voice actor reads an OpenAI-provided phrase in a supported language) plus a sample of 10-30 s (at least five seconds of actual speech and at least 15 transcribed tokens, same speaker). Max 20 voices per organization; formats mpeg, wav, ogg, aac, flac, webm, mp4; 10 MiB per file.
  - Consent-phrase languages include Polish, German, French, Spanish, English (not Norwegian or Swedish in the list I got). Doc does not say whether a custom voice can speak languages other than the recorded one (not confirmed).
  - Works in: Text-to-Speech API, Realtime API (doc example uses gpt-realtime-2), Chat Completions audio, GPT-Live (English accents only). The doc's supported-model line reads "gpt-4o-mini-tts, gpt-realtime-2, and gpt-live-1" (gpt-realtime-2.1 not named in that line; unverified for 2.1).
  - Quote: "The quality of your custom voice is highly dependent on the quality of the sample you provide." No pricing in the docs.
  - Voice cloning of arbitrary people is NOT offered as self-serve (consent flow mandatory). Confidence: high.

---------------------------------------------------------------------
## Q3. Official prompting guidance for human-sounding delivery

Sources [DOC]: current guide https://developers.openai.com/api/docs/guides/realtime-models-prompting (has two parts: "Realtime 2.0 Prompting Guide" and "Realtime 1.5 Prompting Guide"); the original cookbook "Realtime Prompting Guide" (Aug 2025, gpt-realtime) https://developers.openai.com/cookbook/examples/realtime_prompting_guide (page is mostly base64 audio, WebFetch could not extract its body; its content is reproduced in the 1.5 part of the guide above, and its structure/tips were confirmed on the cookbook page itself). Seen 2026-10-05.

### A. Recommended prompt structure
Realtime 2.0 guide skeleton (verbatim headings): `# Role and Objective`, `# Personality and Tone`, `# Language`, `# Reasoning`, `# Message Channels`, `# Preambles`, `# Verbosity`, `# Tools`, `# Unclear Audio`, `# Entity Capture`, `# Long Context Behavior`, `# Escalation`. "Not every use case needs every section. Add the sections that are relevant for your product."
Realtime 1.5 / cookbook skeleton (verbatim): `# Role & Objective` (who you are and what "success" means), `# Personality & Tone` (the voice and style to maintain), `# Context` (retrieved context, relevant info), `# Reference Pronunciations` (phonetic guides for tricky words), `# Tools` (names, usage rules, and preambles), `# Instructions / Rules` (do's, don'ts, and approach), `# Conversation Flow` (states, goals, and transitions), `# Safety & Escalation` (fallback and handoff logic). Cookbook adds: remove sections you do not need and add domain ones (Compliance, Brand Policy).
Confidence: high.

### B. Personality and tone (exact snippets)
From the 1.5/cookbook part (verbatim):
```
# Personality & Tone
## Personality
- Friendly, calm and approachable expert customer service assistant.

## Tone
- Warm, concise, confident, never fawning.

## Length
- 2-3 sentences per turn.
```
Statement: the model "follows instructions well when imitating particular personality or tone" (guide text as reported). Role examples in the guide: "You are a Quebecois French-speaking customer service bot." and "You are a high-energy game-show host guiding the caller to guess a secret number from 1 to 100 to win 1,000,000$."
Emotion-trajectory demo in the guide (shows the model obeys tone descriptors):
```
# Personality & Tone
- Start your response very happy
- Midway, change to sad
- At the end change your mood to very angry
```
Confidence: high (page fetched 3 times with consistent text).

### C. Variety (anti-robotic repetition), verbatim
```
# Personality & Tone
## Variety
- Do not repeat the same sentence twice.
- Vary your responses so they don't sound robotic.
```
General tips list (verbatim): "Iterate relentlessly: Small wording changes can make or break behavior." / "Prefer bullets over paragraphs: Clear, short bullets outperform long paragraphs." / "Guide with examples: The model closely follows sample phrases." / "Be precise: Ambiguity or conflicting instructions = degraded performance." / "Control language: Pin output to a target language if you see unwanted language switching." / "Reduce repetition: Add a Variety rule to reduce robotic phrasing." / "Use capitalized text for emphasis: Capitalizing key rules makes them stand out." / "Convert non-text rules to text: ... write, 'IF MORE THAN THREE FAILURES THEN ESCALATE'." (the cookbook also adds the sample-phrase warning that the realtime model "may overuse" them and sound "robotic or repetitive").
2.0 guide on the same: "Adding a repetition rule helps maintain variety while preserving clarity and brand voice." and "Sample phrases act as 'anchor examples' for the model. They show the style, brevity, and tone you want it to follow, without locking it into one rigid response."

### D. Sample phrases and avoiding robotic repetition (verbatim)
```
# Sample Phrases
- Below are sample examples that you should use for inspiration.
  DO NOT ALWAYS USE THESE EXAMPLES, VARY YOUR RESPONSES.

Acknowledgements: "On it." "One moment." "Good question."
Clarifiers: "Do you want A or B?" "What's the deadline?"
Bridges: "Here's the quick plan." "Let's keep it simple."
Empathy (brief): "That's frustrating, let's fix it."   [original has an em dash]
Closers: "Anything else before we wrap?" "Happy to help next time."
```
And in Conversation Flow:
```
Sample phrases (do not always repeat the same phrases, vary your responses):
- "Thanks for calling NorthLoop Internet, how can I help today?"
```
[original has an em dash]. So the official pattern = give anchors AND explicitly say "do not always use these, vary".

### E. Pacing / speed in the prompt (verbatim)
```
## Pacing
- Deliver your audio response fast, but do not sound rushed.
- Do not modify the content of your response, only increase speaking speed for the same response.
```
Plus the "speed parameter = playback rate" statement (see Q2). The guide gives NO official sample for "slower, calmer"; it only shows a "faster" example. A "slow, calm" pacing rule is therefore my extrapolation. The forum case (Q1 D) shows a blunt "speak slowly" can halve the speech rate.

### F. Language pinning (2.0 guide, verbatim)
English-only variant:
```
## Language
English is the default response language.

- Do not infer language from accent alone.
- Ignore short filler sounds, backchannels, and isolated foreign words for language detection.
- Only switch languages if the user explicitly asks or provides a substantive utterance in another language.
- If language confidence is low, ask a short clarification instead of guessing.
```
Multilingual variant:
```
## Language
Default to English unless the user clearly uses another language.

Switch languages only when:
- the user explicitly asks to use another language;
- the user provides a substantive utterance in another language.

Do not switch languages based on accent, pronunciation, filler words, names, or isolated foreign words.
```
Also from the 2.0 guide: avoid broad instructions like "mirror the user" or "sound local" (as reported by the fetch; the exact sentence was not captured verbatim, confidence medium).
1.5 version: "- The conversation will be only in English. - Do not respond in any other language even if the user asks. - If the user speaks another language, politely explain that support is limited to English."

### G. Unclear audio (2.0 guide, verbatim)
```
## Unclear Audio
- Only respond to clear audio or text.
- If the user's audio is not clear, ask for clarification using a short English phrase such as "Sorry, could you repeat that clearly?"
- Don't repeat the same unclear-audio clarification twice.
- Treat audio as unclear if it is ambiguous, noisy, silent, unintelligible, partially cut off, or if you are unsure of the exact words the user said.
- Do not guess what the user meant from unclear audio.
- Do not reason when the audio is unclear.
- Do not provide a preamble or call tools in the commentary channel when the audio is unclear.
```
Cookbook tip: swapping the word "inaudible" for "unintelligible" improved noisy-input handling.

### H. Reference pronunciations (verbatim)
```
# Reference Pronunciations
When voicing these words, use the respective pronunciations:
- Pronounce "SQL" as "sequel."
- Pronounce "Kyiv" as "KEE-iv."
```
(Useful for the product name and "Orca" if mispronounced in PL/DE.) Alphanumerics: "When reading numbers or codes, speak each character separately, separated by hyphens (e.g., 4-1-5)."

### I. Filler words / disfluencies
- 2.0 guide treats FILLER in preambles as a negative: style "keep it natural, calm, and concise / vary the wording across turns / describe the action, not the internal reasoning / avoid filler". Prefer: "I'll check that order now." "I'll look up your appointment details." "I'll verify that before we make any changes." Avoid: "Let me think...", "One moment while I process that...", "I am now going to access the tool..." (one fetch also listed "Hmm..." among the avoided phrases, the other fetch did not; treat "Hmm..." as unconfirmed). Length: "Use one short sentence. Do not exceed two short sentences unless the user needs an explanation before a high-impact action."
- A "Filler Words" knob exists only in OpenAI's older openai-realtime-agents "Voice Agent Metaprompt" (https://raw.githubusercontent.com/openai/openai-realtime-agents/main/src/app/agentConfigs/voiceAgentMetaprompt.txt, file date not visible; the repo's demo still uses gpt-4o-realtime-mini, so it is stale): "Filler Words: Helps make the agent more approachable, e.g. 'um,' 'uh,' 'hm,' etc.. Options are generally 'none', 'occasionally', 'often', 'very often'"; "Level of Enthusiasm: Degree of energy in responses (e.g., highly enthusiastic vs. calm and measured)"; "Pacing: Rhythm and speed of delivery"; "Level of Emotion: How emotionally expressive or neutral the AI should be (e.g., compassionate vs. matter-of-fact)"; and "be creative and verbose when defining Personality and Tone qualities, and use multiple sentences if possible." Confidence: medium (stale repo, but still OpenAI-authored).
- Backchannels: the GPT-Live guide (not Realtime) has "Use moderate backchannels. Acknowledge naturally without competing with the main response." https://developers.openai.com/api/docs/guides/live-prompting
- I found NO official instruction to add disfluencies on gpt-realtime-2.x.

### J. CAPS, bullets, absolute words (note the tension between guides)
- 1.5/cookbook: bullets over paragraphs; capitalised text for emphasis.
- 2.0 guide does NOT repeat the CAPS, bullets-over-paragraphs, sample-phrases or Variety advice (checked explicitly) and instead warns (verbatim): "Use precise language. The model may prioritize the exact wording of an instruction over the broader behavior you intended. Broad or rigid rules can dominate the assistant's behavior in surprising ways, especially when multiple rules overlap. Be careful with constraint words such as `must`, `only`, `never`, and `always`. Use them when the behavior is truly required, not as general emphasis. Overusing hard constraints can make the assistant rigid, overly cautious, or unable to handle reasonable exceptions."
- "What changed in Realtime 2" table: "Prompt precision: Replace broad guidance like 'be helpful' with clear trigger, action, and exception rules." / "Instruction conflicts: Remove overlapping `always`, `never`, `only`, and `must` rules unless truly required."
- Takeaway: for gpt-realtime-2.x, a prompt full of ALWAYS/NEVER/MUST in caps likely makes delivery stiff; keep hard rules minimal. (Inference from the quote; OpenAI does not link this to voice "robotic" feel explicitly.)

### K. Reasoning-model specifics (2.0 guide)
- Intro: "gpt-realtime-2 is our state-of-the-art reasoning voice model for low-latency speech-to-speech applications. It can think before it speaks, follow instructions more reliably, use a larger context window, and call tools with greater precision than earlier realtime models."
- "Set reasoning effort: gpt-realtime-2 can trade latency for deeper reasoning. Use the lowest reasoning level that still gives the assistant enough intelligence for the workflow." "Start with `low` for most production voice agents. Tune up or down based on task complexity, latency tolerance, and failure cost." (table in Q5)
- Preambles: "Short spoken updates that keep a voice agent feeling responsive while it reasons, looks something up, or calls a tool." "Use short preambles only when they help the user understand that work is happening." NOT to be used when "the answer is direct and can be given immediately", "the user is only confirming, correcting, or declining something", "the audio is unclear", "the latest audio is silence, background noise...". Message channels: "gpt-realtime-2 can produce user-visible intermediate messages in the commentary channel and final user-facing responses in the final channel. Use channel-specific instructions when the behavior depends on where it appears."
- Verbosity per task type, verbatim: "Direct answers: Use 1-2 short sentences. Clarifying questions: Ask one question at a time. ... Escalations: Briefly explain why escalation is needed and what will happen next." and "gpt-realtime-2 follows length guidance best when the prompt specifies how much detail to give for each task type."
- Migration advice: "Set reasoning effort to `low` instead of the default." (the phrase "instead of the default" suggests the doc author thinks the default is higher than low; see Q5 conflict.) "Remove stale examples. Add short examples for happy paths, ambiguity, interruptions, tool calls, fallback behavior."
- Silence handling: `wait_for_user` no-op tool. Instruction block verbatim: "If the latest audio is silence, background noise, hold music, TV audio, side conversation, or speech not addressed to you, call `wait_for_user`. Do not respond conversationally after calling this tool. Do not say 'I'm here,' 'I didn't catch that,' 'Take your time,' or 'Let me know when you're ready.' Resume normal responses only when the user clearly addresses you or asks for help." Intro: "Voice agents tend to respond by default."
Confidence on all of K: high (page fetched several times).

---------------------------------------------------------------------
## Q4. Turn-taking naturalness

All [DOC] API reference (create / client-events) + VAD guide https://developers.openai.com/api/docs/guides/realtime-vad , seen 2026-10-05.
- `audio.input.turn_detection`: "Configuration for turn detection, ether Server VAD or Semantic VAD. This can be set to `null` to turn off, in which case the client must manually trigger model response."
- `server_vad` (default per VAD guide, "Automatically chunks the audio based on periods of silence"): `silence_duration_ms` "Defaults to 500ms"; `threshold` "0.0 to 1.0, this defaults to 0.5"; `prefix_padding_ms` "Defaults to 300ms"; `idle_timeout_ms` "Optional timeout after which a model response will be triggered automatically. This is useful for situations in which a long pause from the user is unexpected, such as a phone call." (emits `input_audio_buffer.timeout_triggered`); `interrupt_response` "Whether or not to automatically interrupt (cancel) any ongoing response with output to the default conversation when a VAD start event occurs."; `create_response` "Whether or not to automatically generate a response when a VAD stop event occurs."
- `semantic_vad`: "a semantic classifier to detect when the user has finished speaking, based on the words they have uttered", "less likely to interrupt the user during a speech-to-speech conversation." `eagerness`: "`low` will wait longer for the user to continue speaking, `high` will respond more quickly. `auto` is the default and is equivalent to `medium`. `low`, `medium`, and `high` have max timeouts of 8s, 4s, and 2s respectively." VAD guide: low "will let the user take their time to speak".
- `input_audio_noise_reduction` (`audio.input.noise_reduction`): "`near_field` is for close-talking microphones such as headphones, `far_field` is for far-field microphones" (laptops, conference-room mics); "Noise reduction filters audio added to the input audio buffer before it is sent to VAD and the model." Can be `null`.
- `create_response` and `interrupt_response` apply to conversation mode only (VAD guide).
- 2.1 improvement relevant here: "improved ... silence and noise handling, and interruption behavior" (community announcement).
- What OpenAI recommends for a calm, unhurried companion: NO use-case-specific recommendation exists in the docs I fetched. The only documented levers are: semantic_vad + `eagerness: low` (explicitly described as letting the user take their time, 8 s cap), the `wait_for_user` pattern for silence, and the prompt rule above. Everything else below is MY INFERENCE:
  - semantic_vad with eagerness "low" fits a user pausing mid-thought; server_vad with the 500 ms default would cut in sooner.
  - do not set `idle_timeout_ms` (it forces a model reply after silence; doc frames it for phone calls), or set it long.
  - near_field for earbuds/phone at ear; far_field if speakerphone. Which fits a phone held in hand is not specified by OpenAI.
- Also (WebSocket-oriented doc, applies to ours only by analogy): for push-to-talk, set `turn_detection: null`.
Confidence: high on parameter semantics, low on "best for companion" (inference).

---------------------------------------------------------------------
## Q5. Latency vs reasoning

- Official levels table [DOC] (2.0 guide): minimal = "Lowest latency matters most and the task is simple" (smart-home commands, timers); low = "You need responsiveness plus basic reasoning" (customer support, order lookup); medium = "The assistant must reason through multi-step tasks" (technical support, diagnostics, complex routing); high = "Deeper reasoning materially improves success" (high-precision workflows, escalation decisions); xhigh = "Maximum reasoning is worth added latency and cost" (complex planning, critical triage).
- Official recommendation [DOC]: "Start with `low` for most production voice agents." and "Use the lowest reasoning level that still gives the assistant enough intelligence for the workflow." Model page: configurable reasoning effort "may increase both latency and token consumption" (as reported by the fetch).
- Default when unspecified: `low`. Source [STAFF] community rep "sps", 2026-07-22: "For Realtime models that support reasoning, the default reasoning level is `low` when no value is specified." ... "I also noticed that this default is not currently documented in the Realtime API reference. I'll flag this with the team for review." https://community.openai.com/t/gpt-realtime-model-default-reasoning/1387803 . Confidence: medium-high (staff-labelled forum post, not in official reference; the guide's "instead of the default" wording is slightly inconsistent with a default of low, see below).
- Numbers: [3P] "1.12 seconds to first audio at minimal reasoning, 2.33 seconds at high reasoning" (Artificial Analysis via The Batch, 2026-05-15, https://www.deeplearning.ai/the-batch/openai-challenges-speech-to-speech-leaders ; also Handy AI 2026-05-12). Benchmark was Big Bench Audio, i.e. reasoning-heavy prompts, not casual chat. DataCamp tutorial (2026-05-12): "When `reasoning.effort` is above `low`, silence becomes noticeable." Confidence: medium (3P, benchmark conditions differ from a chat).
- Microsoft doc [3P]: "If the model is interrupted during thinking, it discards the current chain of thought and starts a new turn." and preambles such as "Let me think about that..." can fill silence. https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/realtime-2
- Our current setting "medium" is documented for multi-step tasks; OpenAI's guidance leans "low" for conversational agents. Whether "medium" is what makes Orca sound robotic is NOT established by any source; it could add pauses and trigger preambles though.
- Not found: any OpenAI-published latency-by-effort table for gpt-realtime-2.1 (the openai.com blog posts returned 403).

---------------------------------------------------------------------
## Q6. "Too cheerful / assistant-like" and how OpenAI suggests correcting it

- Realtime 1.5/cookbook [DOC]: "Warm, concise, confident, never fawning." and "Friendly, calm and approachable expert ..." with "2-3 sentences per turn" (see Q3 B).
- GPT-Live prompting guide [DOC] https://developers.openai.com/api/docs/guides/live-prompting : starter line "You are [name], a calm, friendly voice assistant for [service]. Speak warmly and naturally, at an unhurried pace." and "Be clear and direct, not overly cheerful. If the user is frustrated, acknowledge it briefly and focus on the next helpful step." Also: "Keep listening while the user pauses to think. Do not treat a cough, music, or nearby conversation as a new request." Response length: "For routine questions, give one or two short sentences." This is guidance for gpt-live-1, but the wording is the closest official text to "calm, unhurried, not overly cheerful"; applying it to gpt-realtime-2.x is an extrapolation.
- Older OpenAI demo repo (openai-realtime-agents chatSupervisor agent): "Maintain an extremely neutral, unexpressive, and to-the-point tone at all times" and "Do not use sing-song-y or overly friendly language"; also "don't say the same thing twice, always vary it to ensure the conversation feels natural". (Stale repo; extreme example, not a model for a warm companion.)
- Voice Agent Metaprompt: "Level of Enthusiasm ... calm and measured", "Level of Emotion ... compassionate vs. matter-of-fact" as descriptors to fill in.
- No OpenAI document I found has a section literally about "model sounds too cheerful/assistant-like". The documented levers are descriptors (role, personality, tone, length, pacing), Variety rule, sample phrases as anchors, avoiding preambles on conversational turns, minimal hard rules, and voice choice (marin/cedar).
- [FORUM] one thread reports the voice "randomly getting super excited" every 30-45 s (search snippet only, not fetched; ignore unless reproduced).

---------------------------------------------------------------------
## Not confirmed / not found (gaps)
1. Any OpenAI statement that older voices (alloy/ash/ballad/coral/echo/sage/shimmer/verse) are lower quality on 2/2.1. Only "We recommend marin and cedar for best quality."
2. Any OpenAI statement on Polish (or Norwegian/Swedish) Realtime quality or accent. No Polish-specific forum report either.
3. A 2.1-specific prompting guide; the guide page covers only 2 and 1.5.
4. Default reasoning effort in the official API reference (only a staff forum reply, and the guide's "instead of the default" wording is ambiguous).
5. OpenAI-published latency numbers per reasoning level (only third-party Artificial Analysis).
6. Exact WebRTC output codec (Opus not stated).
7. Whether custom voices can speak languages other than the recorded one; whether a custom voice is usable with gpt-realtime-2.1 specifically (doc names gpt-realtime-2); pricing.
8. Behavior of gpt-live-transcribe / gpt-transcribe as `audio.input.transcription.model` inside a speech-to-speech conversation session.
9. openai.com/index/* pages (introducing-gpt-realtime, advancing-voice-intelligence-with-new-models-in-the-api, introducing-gpt-live) returned HTTP 403, so I used the community-forum copies of the announcements and the developers.openai.com docs instead.
10. The original cookbook page body could not be extracted (base64 audio); its text was obtained through the equivalent "Realtime 1.5 Prompting Guide" on developers.openai.com.
11. Whether "Hmm..." is on the official avoid-list for preambles (one extraction yes, one no).
12. Any OpenAI-documented effect of "medium" reasoning on conversational feel.

---------------------------------------------------------------------
## Sources (all seen 2026-10-05)
1. Realtime prompting guide (2.0 + 1.5): https://developers.openai.com/api/docs/guides/realtime-models-prompting (DOC; page undated, covers gpt-realtime-2 released 2026-05-07)
2. Original Realtime Prompting Guide cookbook: https://developers.openai.com/cookbook/examples/realtime_prompting_guide (DOC, Aug 2025)
3. Realtime API reference, session create: https://developers.openai.com/api/reference/resources/realtime/subresources/client_secrets/methods/create (DOC)
4. Realtime client events reference: https://developers.openai.com/api/reference/resources/realtime/client-events (DOC)
5. VAD guide: https://developers.openai.com/api/docs/guides/realtime-vad (DOC)
6. Realtime conversations guide: https://developers.openai.com/api/docs/guides/realtime-conversations (DOC)
7. WebRTC guides: https://developers.openai.com/api/docs/guides/realtime-webrtc , https://developers.openai.com/api/docs/guides/voice-webrtc (DOC)
8. Model pages: https://developers.openai.com/api/docs/models/gpt-realtime-2 , https://developers.openai.com/api/docs/models/gpt-realtime-2.1 , https://developers.openai.com/api/docs/models/gpt-live-1 (DOC)
9. Changelog: https://developers.openai.com/api/docs/changelog (DOC)
10. Deprecations: https://developers.openai.com/api/docs/deprecations (DOC)
11. TTS guide: https://developers.openai.com/api/docs/guides/text-to-speech (DOC)
12. Custom voices: https://developers.openai.com/api/docs/guides/custom-voices (DOC)
13. GPT-Live guides: https://developers.openai.com/api/docs/guides/live , .../live-prompting , .../live-conversations , .../voice-agents (DOC)
14. Realtime transcription guide: https://developers.openai.com/api/docs/guides/realtime-transcription (DOC)
15. gpt-realtime-2.1 announcement (2026-07-06): https://community.openai.com/t/new-realtime-models-on-the-api-gpt-realtime-2-1-and-gpt-realtime-2-1-mini/1385896 (STAFF)
16. gpt-realtime-2 announcement (2026-05-07): https://community.openai.com/t/new-realtime-voice-models-in-the-api/1380471 (STAFF)
17. gpt-realtime announcement (2025-08-28): https://community.openai.com/t/introducing-gpt-realtime-and-realtime-api-updates-for-production-voice-agents/1355039 (STAFF)
18. Default reasoning thread (2026-07-22): https://community.openai.com/t/gpt-realtime-model-default-reasoning/1387803 (STAFF reply)
19. Custom voices access thread (2026-08-27 staff reply): https://community.openai.com/t/custom-voices-in-the-api-not-available/1377611 (STAFF reply)
20. GPT-Live-1 announcement (2026-09-10): https://community.openai.com/t/introducing-gpt-live-1-in-the-api/1396471 (STAFF)
21. Slow-speech thread: https://community.openai.com/t/gpt-realtime-2-voice-is-extremely-slow-speaking-slowly/1381481 (FORUM + staff link 2026-09-07)
22. Language drift thread: https://community.openai.com/t/gpt-realtime-2-1-exhibits-language-drift/1386953 (FORUM)
23. Marin/Cedar dialect thread: https://community.openai.com/t/bug-unexpected-behavior-marin-cedar-voices-repeat-greeting-no-dialect-flemish/1367693 (FORUM)
24. Language switching thread: https://community.openai.com/t/realtime-api-language-switching/1366289 (FORUM)
25. Microsoft Foundry GPT Realtime 2.x overview (updated 2026-09-23): https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/realtime-2 (3P)
26. Microsoft Foundry GPT-Live (updated 2026-09-30): https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/gpt-live (3P)
27. The Batch (2026-05-15): https://www.deeplearning.ai/the-batch/openai-challenges-speech-to-speech-leaders (3P)
28. Handy AI (2026-05-12): https://handyai.substack.com/p/model-drop-gpt-realtime-2 (3P)
29. DataCamp tutorial (2026-05-12): https://www.datacamp.com/tutorial/gpt-realtime-2-api (3P)
30. openai-realtime-agents repo + Voice Agent Metaprompt: https://github.com/openai/openai-realtime-agents , https://raw.githubusercontent.com/openai/openai-realtime-agents/main/src/app/agentConfigs/voiceAgentMetaprompt.txt (DOC, stale)
