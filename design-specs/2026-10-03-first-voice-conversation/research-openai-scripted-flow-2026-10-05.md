# Research: scripted, survey-based opening on OpenAI Realtime (gpt-realtime-2.1 / gpt-realtime-2)

Date of research: 2026-10-05. Read-only. Sources: official OpenAI docs, OpenAI GitHub repos, OpenAI Developer Community (trail only).

## 0. Method and caveats (read first)

- All pages were fetched with WebFetch. WebFetch passes pages through a small summarizer model, so quotes can be slightly compressed. For every load-bearing snippet I re-fetched with a "copy character-for-character" prompt and kept the more literal version. Treat code blocks as "as returned by fetch"; spot-check against the page before copying them into production prompts.
- Per the output rule of this task, every long or short dash inside quoted text (for example "2-3 sentences per turn", "10am-12pm ET", "That's frustrating, let's fix it") was replaced with a plain hyphen or comma. The original pages use en/em dashes in a few places.
- Official docs pages carry no visible publication date. Model dates: gpt-realtime-2 released 2026-05-07 (Azure doc lists version 2026-05-07; OpenAI announcement per search result), gpt-realtime-2.1 released 2026-07-06/07 (OpenAI community announcement; Azure lists 2026-07-07).
- There are THREE separate OpenAI voice products in the docs now. Do not mix them: (a) Realtime API (gpt-realtime-2.1, gpt-realtime-2, gpt-realtime-1.5; events `session.update`, `response.create`), (b) GPT-Live (gpt-live-1, GA 2026-09-10 per changelog; events `session.start`, `session.instructions.append`; different prompting guide), (c) chained STT -> LLM -> TTS. Your app uses (a). I cite (b) only where it is explicitly labelled as such.
- IMPORTANT STRUCTURAL FINDING: the single prompting page `https://developers.openai.com/api/docs/guides/realtime-models-prompting` has two tabs. The `gpt-realtime-2` tab has NO "Conversation Flow", NO "Sample Phrases", NO state machine section. Those live only in the `gpt-realtime-1.5` tab (same content as the older cookbook "Realtime Prompting Guide"). The gpt-realtime-2 tab defers to "reasoning voice agent" style: short labeled sections, trigger/action/exception rules. There is no separate gpt-realtime-2.1 prompting guide; the 2.1 model page and announcement say 2.1 "updates GPT-Realtime-2 with improved alphanumeric recognition, silence and noise handling, and interruption behavior" and contain no migration or prompting notes.

## 1. Most actionable findings (my synthesis, flagged where it is inference)

1. OpenAI's own verbatim-first-line recipe is NOT "tell the model to build the line". It is "Say exactly ...". Docs example (Realtime conversations guide, section "Create responses with no context"): `response.create` with `input: []` and `instructions: "Say exactly the following: ..."`. OpenAI's own Agents SIP example does it belt-and-braces: session instructions say "Always begin the call by saying exactly: '<WELCOME>' before collecting details" AND a `response.create` carries "Say exactly '<WELCOME>' now before continuing the conversation."
2. Per-response `instructions` OVERRIDE (not append to) the session instructions for that one response. Official wording: "If these are set, they will override the Session's configuration for this Response only." A third-party project (MulmoChat PR #244) measured exactly that: the per-response instructions replaced the session prompt, and they fixed it by sending follow-up instructions as a `system` conversation item + plain `response.create`.
3. Two official ways to keep the full session prompt active on the first turn: (a) system-role `conversation.item.create` ("can be added at any point in the conversation") then plain `response.create`; (b) the openai-realtime-agents pattern: a simulated user message `hi` via `conversation.item.create` then `response.create`, with the instruction text containing "Always greet the user with ...".
4. Fix the race: set `instructions` (and `reasoning`) when the session is minted (`/v1/realtime/client_secrets` accepts `session.instructions`, `session.reasoning`, `session.prompt`; or `/v1/realtime/calls` for the unified interface) so the first `response.create` can never run on server default instructions. If you send `session.update` after connecting, wait for `session.updated` before `response.create`. Server default instructions are used when `instructions` is not set (official: "The server sets default instructions which will be used if this field is not set and are visible in the `session.created` event"). Those defaults are the likely source of generic "How can I help you today?" greetings (inference; third-party reports of the race exist, see 3.5).
5. Strict sequence of 3 questions + hand-over: OpenAI's pattern is "phases with Goal / How to respond / Sample phrases / Exit when". The only OpenAI mechanism that actually ENFORCES a sequence is the "Dynamic Conversation Flow": swap `instructions` per phase via `session.update` ("Instead of exposing the model to all possible rules and tools at once, you only provide what's relevant to the active phase"). Caveat from the cost guide: changing instructions mid-session reduces cache rate. No official "do not skip" wording was found.
6. gpt-realtime-2 follows wording more literally and conflicting `always/never/only/must` rules are costly; OpenAI says "Start simple. Do not over-prompt upfront." and "Start with `low` for most production voice agents." Your effort is `medium`, which the guide reserves for "multi-step tasks". A 3-question script with a hand-over is arguably multi-step, so `medium` is defensible, but the migration list says to set `low` and raise only if needed.
7. Language: no official statement for Realtime on "write prompt in English vs target language". Official examples are English prompts that declare a `## Language` section (French tutor example) and pin the output language. The GPT-Live guide (different product) says "Write the prompt and examples in the language you want the assistant to speak". The Realtime 2 guide says avoid "Mirror the user"-style language rules.

## 2. Q1: Conversation Flow / scripted step-by-step structure

### 2.1 What the gpt-realtime-2 tab recommends (structure, not flow)

Source: https://developers.openai.com/api/docs/guides/realtime-models-prompting?realtime-model=gpt-realtime-2 (undated; fetched 2026-10-05). Confidence: high (producer docs).

Recommended skeleton, verbatim: "Use short, labeled sections. The model should be able to find the relevant instructions quickly."

```text
# Role and Objective
# Personality and Tone
# Language
# Reasoning
# Message Channels
# Preambles
# Verbosity
# Tools
# Unclear Audio
# Entity Capture
# Long Context Behavior
# Escalation
```

Headings of the gpt-realtime-2 tab, in order (verified by listing): Realtime 2.0 Prompting Guide; What changed in Realtime 2; Recommended prompt structure; Set reasoning effort; Use preambles intentionally; Control response length; Design tool behavior; Handle silence and background audio; Use message channels deliberately; Handle unclear audio; Capture exact entities; Avoid literal instruction traps; Control language and accent separately; Maintain state in long sessions; Migrate from earlier realtime models. No Conversation Flow.

One-question-per-turn rules that do exist in the 2 tab (closest analogs to "one question per turn"):

```text
## Verbosity
- Direct answers: Use 1-2 short sentences.
- Clarifying questions: Ask one question at a time.
...
1. Collect the next required value.
- Ask for only one missing value at a time.
- Do not ask for multiple exact values in the same turn.
```

### 2.2 The Conversation Flow pattern (gpt-realtime-1.5 tab, same as the original cookbook guide)

Source: https://developers.openai.com/api/docs/guides/realtime-models-prompting?realtime-model=gpt-realtime-1.5 and cookbook https://developers.openai.com/cookbook/examples/realtime_prompting_guide (the cookbook page itself could not be fetched in full, its text is cut off by embedded base64 audio; the guide page carries the same text). Confidence: high that the text is OpenAI's; medium on exact punctuation (summarizer).

Intro, verbatim:

```text
This section covers how to structure the dialogue into clear,
goal-driven phases so the model knows exactly what to do at each
step. It defines the purpose of each phase, the instructions for
moving through it, and the concrete "exit criteria" for
transitioning to the next.
```

Example (first 3 phases shown in full, the page has 6: Greeting, Discover, Verify, Diagnose, Resolve, Confirm/Close):

```text
# Conversation Flow
## 1) Greeting
Goal: Set tone and invite the reason for calling.
How to respond:
- Identify as NorthLoop Internet Support.
- Keep the opener brief and invite the caller's goal.
- Confirm that customer is a Northloop customer
Exit to Discovery: Caller states they are a Northloop customer and mentions an initial goal or symptom.

## 2) Discover
Goal: Classify the issue and capture minimal details.
How to respond:
- Determine billing vs connectivity with one targeted question.
- For connectivity: collect the service address.
- For billing/account: collect email or phone used on the account.
Exit when: Intent and address (for connectivity) or email/phone (for billing) are known.

## 3) Verify
Goal: Confirm identity and retrieve the account.
How to respond:
- Once you have email or phone, call lookup_account(email_or_phone).
- If lookup fails, try the alternate identifier once; otherwise proceed with general guidance or offer escalation if account actions are required.
Exit when: Account ID is returned.
```

Flow plus sample phrases, verbatim (states 1 and 2):

```text
# Conversation Flow
## 1) Greeting
Goal: Set tone and invite the reason for calling.
How to respond:
- Identify as NorthLoop Internet Support.
- Keep the opener brief and invite the caller's goal.
Sample phrases (do not always repeat the same phrases, vary your responses):
- "Thanks for calling NorthLoop Internet, how can I help today?"
- "You've reached NorthLoop Support. What's going on with your service?"
- "Hi there, tell me what you'd like help with."
Exit when: Caller states an initial goal or symptom.

## 2) Discover
Goal: Classify the issue and capture minimal details.
How to respond:
- Determine billing vs connectivity with one targeted question.
- For connectivity: collect the service address.
- For billing/account: collect email or phone used on the account.
Sample phrases (do not always repeat the same phrases, vary your responses):
- "Is this about your bill or your internet speed?"
- "What address are you using for the connection?"
- "What's the email or phone number on the account?"
Exit when: Intent and address (for connectivity) or email/phone (for billing) are known.
```

Prose around it, verbatim: "Sample phrases act as 'anchor examples' for the model. They show the style, brevity, and tone you want it to follow." and "It is a useful pattern to add sample phrases in the different conversation flow states to teach the model what a good response looks like."

Note for your case: the official example's Greeting phase is "invite the caller's goal", i.e. the pattern itself nudges toward "how can I help". If your prompt copies this shape, the Greeting phase template will bias the model toward a generic opener. Your first phase should be "Opening question" with a concrete, fully specified line (inference).

### 2.3 JSON state machine (openai-realtime-agents)

Source (repo, main branch, fetched 2026-10-05): https://github.com/openai/openai-realtime-agents , file `src/app/agentConfigs/customerServiceRetail/authentication.ts`; the same JSON is shown in the guide (1.5 tab, "Advanced Conversation Flow": "As use cases grow more complex, you'll need a structure that scales while keeping the model effective."). Confidence: high.

First state object, verbatim as fetched:

```json
{
  "id": "1_greeting",
  "description": "Begin each conversation with a warm, friendly greeting, identifying the service and offering help.",
  "instructions": [
    "Use the company name 'Snowy Peak Boards' and provide a warm welcome.",
    "Let them know upfront that for any account-specific assistance, you'll need some verification details."
  ],
  "examples": [
    "Hello, this is Snowy Peak Boards. Thanks for reaching out! How can I help you today?"
  ],
  "transitions": [{
    "next_step": "2_get_first_name",
    "condition": "Once greeting is complete."
  }, {
    "next_step": "3_get_and_verify_phone",
    "condition": "If the user provides their first name."
  }]
}
```

Other state excerpts from the repo (verbatim): state 2 `"Politely ask, 'Who do I have the pleasure of speaking with?'"` and `"Do NOT verify or spell back the name; just accept it."`; state 3 `"If user corrects you, confirm AGAIN to make sure you understand."`; global rule `"Whenever the user provides a piece of information, ALWAYS read it back to the user character-by-character to confirm you heard it right before proceeding."` Repo headings: "# Personality and Tone", "# Task", "# Demeanor", "# Overall Instructions", "# Conversation States". Transitions are expressed as `next_step` + `condition` in prose; the model, not code, decides when the condition is met.

### 2.4 Dynamic Conversation Flow (the only enforcement mechanism in the guides)

Source: gpt-realtime-1.5 tab, "Dynamic Conversation Flow". Verbatim: "In this pattern, the conversation adapts in real time by updating the system prompt and tool list based on the current state. Instead of exposing the model to all possible rules and tools at once, you only provide what's relevant to the active phase."

Code in the guide (Python), the part relevant to prompts only:

```python
INSTRUCTIONS_BY_STATE: dict[State, str] = {
    "verify": (
        "# Role & Objective\n"
        "Verify identity to access the account.\n\n"
        "# Conversation (Verify)\n"
        "- Ask for the email or phone on the account.\n"
        "- Read back digits one-by-one (e.g., '4-1-5... Is that correct?').\n"
        "Exit when: Account ID is returned.\n"
        'When exit satisfied: call set_conversation_state(next_state="resolve").'
    ),
    "resolve": (
        "# Role & Objective\n"
        "Apply a fix by booking a technician.\n\n"
        "# Conversation (Resolve)\n"
        "- Offer two windows: '10-12 ET' or '2-4 ET'.\n"
        "- Book the chosen window.\n"
        "Exit when: Appointment is confirmed.\n"
        "When exit satisfied: end the call politely."
    ),
}

def build_session_update(state: State) -> dict:
    """Return the JSON payload for a Realtime `session.update` event."""
    return {
        "type": "session.update",
        "session": {
            "instructions": INSTRUCTIONS_BY_STATE[state],
            "tools": TOOLS_BY_STATE[state] + [build_state_change_tool(state)],
        },
    }
```

The guide's transition is a function tool `set_conversation_state` whose description says "Call this AFTER exit criteria are satisfied." Your session has no function tools; the same idea can be driven client-side (count user turns, then send `session.update` with the next phase's short instructions). That adaptation is MY inference, not an OpenAI-documented recipe. Cost: see section 5.3 (cache).

### 2.5 "Do not skip" / "move on only when"

Not found as explicit wording. What exists: the "Exit when:" / "Exit to X:" convention, one-question-per-turn rules (2.1 above), `Do NOT use when:` per-tool rules (1.5 tab), and capitalised emphasis: "Use capitalized text for emphasis: Capitalizing key rules makes them stand out and easier for the model to follow." (1.5 General Tips). The gpt-realtime-2 tab warns about hard-constraint words, see section 6.

## 3. Q2: Making the agent speak first with a specific opening

### 3.1 Official reference facts

Source: https://developers.openai.com/api/reference/resources/realtime/client-events (fetched 2026-10-05). Confidence: high.

- response.create: "This event instructs the server to create a Response, which means triggering model inference. When in Server VAD mode, the server will create Responses automatically."
- Per-response config overrides: "The `response.create` event includes inference configuration like `instructions` and `tools`. If these are set, they will override the Session's configuration for this Response only."
- `instructions` (both session and response): "The default system instructions (i.e. system message) prepended to model calls. This field allows the client to guide the model on desired responses." and "The instructions are not guaranteed to be followed by the model, but they provide guidance to the model on the desired behavior."
- Session `instructions` default: "The server sets default instructions which will be used if this field is not set and are visible in the `session.created` event at the start of the session." (https://developers.openai.com/api/reference/resources/realtime/server-events)
- `conversation`: "Controls which conversation the response is added to. Currently supports `auto` and `none`, with `auto` as the default value."
- `input`: "Input items to include in the prompt for the model. Using this field creates a new context for this Response instead of using the default conversation."
- Per-response fields listed by the reference (fetched once, medium confidence on `reasoning`, not independently re-verified): audio, conversation, input, instructions, max_output_tokens, metadata, output_modalities, parallel_tool_calls, prompt, reasoning (effort minimal/low/medium/high/xhigh), tool_choice, tools.
- session.update: "Send this event to update the session's configuration. The client may send this event at any time to update any field except for `voice` and `model`." and "Only the fields that are present in the `session.update` are updated. To clear a field like `instructions`, pass an empty string."
- Conversation items, system role: "A system message in a Realtime conversation can be used to provide additional context or instructions to the model. This is similar but distinct from the instruction prompt provided at the start of a conversation, as system messages can be added at any point in the conversation." (role always `system`, content type `input_text`).
- `previous_item_id`: "If not set, the new item will be appended to the end of the conversation. If set to `root`, the new item will be added to the beginning."

Override vs append: OFFICIAL wording is "override ... for this Response only". Docs do not use the word "replace" and do not define precisely whether the session prompt is dropped entirely or merged field-by-field, but for a single string field "override" means the response-level string is used. Empirical third-party confirmation: https://github.com/receptron/MulmoChat/pull/244 ("Those instructions replace the session prompt for that reply"; their fix: "They now go into the conversation as a system message before a plain response.create"; measured 15/30 -> 30/30). Level: third-party observation, one source, confidence medium.

### 3.2 Official recipe for an exact line (verbatim)

Source: https://developers.openai.com/api/docs/guides/realtime-conversations , section "Create responses with no context". Confidence: high.

"You can also insert responses into the default conversation, ignoring all other instructions and context. Do this by setting `input` to an empty array."

```javascript
const prompt = `
Say exactly the following:
I'm a little teapot, short and stout!
This is my handle, this is my spout!
`;

const event = {
  type: "response.create",
  response: {
    // An empty input array removes existing context
    input: [],
    instructions: prompt,
  },
};

// WebRTC data channel and WebSocket both have .send()
dataChannel.send(JSON.stringify(event));
```

Implications (inference from the docs): (a) the response is inserted into the DEFAULT conversation (no `conversation: "none"`), so later turns see "I already asked Q1"; with `conversation: "none"` the line would not be recorded and the model would not know it had spoken. (b) With `input: []` and per-response `instructions`, session instructions/persona and prior items are ignored for that one response; at the very first turn the conversation is empty anyway, so `input: []` mostly just guarantees no stray context. (c) The text of the exact line must be composed in app code from the survey (name, topic, rating) BEFORE sending; then the model cannot default to "how are you".

### 3.3 OpenAI's own greeting examples (official repos)

1. openai-agents-python, Twilio SIP example (`examples/realtime/twilio_sip/server.py`, `agents.py`, main branch). The agent instructions are set at call accept time; the greeting is forced with a raw `response.create`:

```python
await session.model.send_event(
    RealtimeModelSendRawMessage(
        message={
            "type": "response.create",
            "other_data": {
                "response": {
                    "instructions": (
                        "Say exactly '"
                        f"{WELCOME_MESSAGE}"
                        "' now before continuing the conversation."
                    )
                }
            },
        }
    )
)
```

```text
WELCOME_MESSAGE = "Hello, this is ABC customer service. How can I help you today?"
Triage Agent Instructions: "Always begin the call by saying exactly: 'Hello, this is ABC customer service. How can I help you
today?' before collecting details. Once the greeting is complete, gather context and hand off to the
FAQ or Records agents when appropriate."
```

The Agents Python realtime guide (https://openai.github.io/openai-agents-python/realtime/guide/) says: "For an opening greeting, send a raw `response.create`" and "The SIP example uses a raw `response.create` to force an opening greeting."  Note the double-lock: the same exact line is in the session instructions AND in the per-response instruction. (Inference: OpenAI's own sample does not trust session instructions alone for the first line.)

2. openai-realtime-agents (`src/app/App.tsx`, main): first turn is triggered by a simulated user message, not a bare `response.create`:

```javascript
sendClientEvent({
  type: 'conversation.item.create',
  item: {
    id,
    type: 'message',
    role: 'user',
    content: [{ type: 'input_text', text }],
  },
});
sendClientEvent({ type: 'response.create' }, '(simulated user text message)');
```

with `if (shouldTriggerResponse) { sendSimulatedUserMessage('hi'); }`. The agent instruction then supplies the line, e.g. chatSupervisor: `Always greet the user with "Hi, you've reached NewTelco, how can I help you?"`. In this repo the session instructions are applied after connection via `session.update` events (per fetch summary), and the `hi` message is sent after that.

3. GPT-Live (different product, `session.instructions.append`), official example of an imperative first-turn instruction: "Greet the caller now in English. Introduce yourself as the support assistant and ask how you can help. Then pause and listen." (https://developers.openai.com/api/docs/guides/live-conversations). Useful as phrasing precedent only: imperative, "now", explicit stop condition.

4. Community (level 4, trail only): developers on the OpenAI forum use `conversation.item.create` (role user, text "Greet the user with ...") followed by `response.create`; one noted "The `item.content[0].text` behaves like an instruction, meaning that the voice agent says only the greeting text" (https://community.openai.com/t/make-agent-speak-first-when-using-realtimesession/1328354, 2025-07-29, no OpenAI staff reply).

### 3.4 Ordering and race (first-turn pitfalls)

- WebRTC guide (https://developers.openai.com/api/docs/guides/realtime-webrtc): session configuration is supplied server-side when you create the session. Unified interface: config goes in the multipart `session` field to `/v1/realtime/calls`; ephemeral token: config goes to `/v1/realtime/client_secrets`. Sample: `const sessionConfig = JSON.stringify({ type: "realtime", model: "gpt-realtime-2.1", audio: { output: { voice: "marin" } } });`. The data channel is `oai-events`.
- Client secrets reference (https://developers.openai.com/api/reference/resources/realtime/subresources/client_secrets/methods/create): `session` accepts `instructions`, `reasoning`, `prompt`, tools, audio etc. Verbatim: "You can also attach session configuration options to the client secret, which will be applied to any sessions created using that client secret, but these can also be overridden by the client connection."
- NOTE: the WebRTC page contains the sentence "Do not send `session.start` on the data channel", but it belongs to the "Connect a browser to GPT-Live" section (GPT-Live product), NOT to the Realtime API. I initially read it as a Realtime rule; it is not.
- The docs I fetched do not say "wait for `session.updated` before `response.create`" and do not describe an ordering guarantee. `session.updated` is documented as: "Returned when a session is updated with a `session.update` event, unless there is an error."
- Third-party evidence of the race (level 4, github issue, not OpenAI): https://github.com/pipecat-ai/pipecat/issues/5354 states the Realtime backend "can generate a session's first response before session.update has taken effect", "settings passed at construction (like system_instruction) silently don't apply to that turn", intermittent, reproducible "against OpenAI's own realtime backend directly". That report concerns server-VAD user-speech-first turns, but the mechanism (first inference before instructions applied) is the same as `response.create` sent before `session.updated`.
- Community thread "How can I get a consistent initial greeting" (https://community.openai.com/t/how-can-i-get-a-consistent-initial-greeting/1357844, 2025-09-12, unresolved): developer used an initial `response.create` "wake up" and kept getting the generic "Hello, what can I help you with today." despite putting instructions in client_secrets, stored prompts and session init. Only reply (juberti, 2025-09-13) pointed to a sample app. I could not read that sample's code. Level 4.
- Azure/Microsoft doc (not OpenAI) shows the generic outcome with default instructions: `response.create` with `instructions: "Please assist the user."` yields transcript "Hello! How can I assist you today?" (https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/realtime-audio, updated 2026-09-23).

### 3.5 What I could not confirm for Q2

- No OpenAI statement that "the model may ignore session instructions on the very first turn" as a known model behaviour. Only the race (third-party) and default-instructions fallback (official wording above).
- No OpenAI statement about too-long instructions degrading the first turn specifically. See section 6 for general "start simple".
- No official wording on whether per-response `instructions` fully replace session instructions vs merge. Only "override ... for this Response only" plus the one third-party measurement.

## 4. Q3: Sample phrases, verbatim lines, variety, fixed sequence

All 1.5-tab (and cookbook) unless noted. Confidence: high that OpenAI says it.

- "Guide with examples: The model closely follows sample phrases." So any generic sample in your prompt (for example "Hi, how are you today?") WILL be copied. Keep examples consistent with the intended opener.
- Variety rule, verbatim: "## Variety\n- Do not repeat the same sentence twice.\n- Vary your responses so they don't sound robotic." Tip: "Reduce repetition: Add a Variety rule to reduce robotic phrasing."
- Sample phrases header, verbatim: "Below are sample examples that you should use for inspiration. DO NOT ALWAYS USE THESE EXAMPLES, VARY YOUR RESPONSES." and, inside the flow: "Sample phrases (do not always repeat the same phrases, vary your responses):".
- When to use exact lines: OpenAI's own examples use exact lines for (a) greeting/welcome ("Say exactly ..."), (b) mandatory disclosure in the realtime-agents repo (disclosure "must be read in full exactly as written" per the fetch summary of authentication.ts, not re-verified verbatim), (c) tool output wrapped in an envelope: `{"response_text": "...", "require_repeat_verbatim": true}` ("Wrap complex tool outputs in JSON envelope to keep in-distribution and prevent truncation/paraphrasing" is the summarizer's paraphrase of the section; the JSON example is verbatim), (d) escalation phrase: "What to say at same time as calling escalate_to_human tool (MANDATORY)".
- For a fixed sequence of questions: no dedicated recipe. Closest: numbered phases with Exit criteria (2.2), one question per turn (2.1), and per-phase instruction swapping (2.4).
- Trade-off (my reasoning, not in docs): exact lines kill repetition risk for the OPENING (it happens once per user) but make Polish names/declension and survey wording rigid; paraphrase keeps naturalness but is exactly where the model drifts to generic openers. Between the two, "Say exactly" for line 1 and phase-based paraphrase with Sample phrases (varied) for questions 2 and 3 matches OpenAI's own patterns.

## 5. Q4: Dynamic per-user context placement and caching

### 5.1 Official prompt skeletons (where "Context" sits)

- gpt-realtime-1.5 skeleton (verbatim, verified in two fetches): "# Role & Objective / # Personality & Tone / # Context / # Reference Pronunciations / # Tools / # Instructions / Rules / # Conversation Flow / # Safety & Escalation". So `# Context` sits SECOND-TO-FOURTH, before rules and flow. The 1.5 page gives no example content for it beyond "retrieved context, relevant info".
- gpt-realtime-2 skeleton has no `Context` section, only `Long Context Behavior`. Its context template (verbatim, "Maintain state in long sessions") structures injected context as labeled blocks:

```text
## Context

### Current State

- **Current task:** [current task]
- **Latest known state:** [current value]
- **Next safe step:** [what the assistant should do next]

### Authoritative Sources

- **Fact or record:** [fact or record]
- **Source:** [tool result / active policy / verified record]
- **Status:** current
- **Retrieved:** [date/time or this turn]

### Historical or Background Sources

- **Older fact or record:** [older fact or record]
- **Source:** [prior conversation / older record / summary]
- **Status:** stale or background
- **Note:** Do not use for current decisions if it conflicts with a current source.

### Relevant Policy or Rules

- [decision rule or constraint]

### Other Context

- [potentially useful but non-authoritative background]
```

  The guide frames this for long sessions (128k context) and for "injected context"; it does not say whether to inject via `instructions` or via conversation items, and does not say top vs bottom.
- Dashboard prompts with variables exist (`prompt` field on session and on `response.create`: "Reference to a prompt template and its variables"; Developer notes post: "You can now use prompts with the Realtime API as a convenient way to have your application code refer to a prompt that can be edited separately." https://developers.openai.com/blog/realtime-api). This is OpenAI's official mechanism for static template + per-user variables. Not verified how Realtime renders variables in practice.

### 5.2 Prompt caching (official)

- Realtime cost guide (https://developers.openai.com/api/docs/guides/realtime-costs): "Realtime API supports prompt caching, which is applied automatically and can dramatically reduce the costs of input tokens during multi-turn sessions." "Caching applies when the input tokens of a Response match tokens from a previous Response, though this is best-effort and not guaranteed." "keep a session's history static. Removing or changing content in the conversation will 'bust' the cache up to the point of the change" and "instructions and tool definitions are at the beginning of a conversation, thus changing these mid-session will reduce the cache rate for subsequent turns."
- Developer notes (https://developers.openai.com/blog/realtime-api): "Prompt caching works by identifying identical, exact-match content prefixing your prompts."
- General prompt caching guide (https://developers.openai.com/api/docs/guides/prompt-caching; generic, NOT Realtime-specific, it states no Realtime/audio mention): "Put stable developer instructions and shared reference material first. If developer instructions or shared material contain timestamps, user-specific content, or other dynamic content, place those at the end rather than the beginning, or move them into later conversation messages." Min cacheable length "1,024 tokens for GPT-5.6 and later" (not stated for realtime models).
- 2.1 changelog line: "reduced p95 latency by at least 25% across Realtime voice models through improved caching" (community announcement, https://community.openai.com/t/new-realtime-models-on-the-api-gpt-realtime-2-1-and-gpt-realtime-2-1-mini/1385896).
- Practical reading (my inference): in a ONE-conversation onboarding session, the prefix is already per-user, so cross-user caching is irrelevant unless the static part is a shared prefix across users. Putting static rules first and the per-user survey block last keeps a shared prefix cacheable across users; per-user data in the middle only matters for cost, not for correctness. For correctness of the first turn, what matters more is that the opener is NOT left for the model to compose.
- Conflict between sources: the 1.5 skeleton puts `# Context` early, the caching guide says dynamic content last. They optimise different things (model attention/structure vs cost). No official source resolves this for Realtime.

## 6. Q5: gpt-realtime-2 / 2.1 instruction following

Source: https://developers.openai.com/api/docs/guides/realtime-models-prompting (2 tab) and https://developers.openai.com/api/docs/guides/voice-prompting. Confidence: high.

Verbatim statements:
- "Prompt Realtime 2 as a reasoning voice agent, not as a basic voice bot."
- "Start simple. Do not over-prompt upfront. Begin with a minimal prompt, run evaluations, then add instructions only for behaviors that fail in testing."
- "Prompt precision matters more. Replace broad guidance like 'be helpful' with clear trigger, action, and exception rules: when to act, what to do, and when not to do it."
- "Instruction conflicts are more costly. Remove overlapping `always`, `never`, `only`, and `must` rules unless they are truly required. Define priority when rules compete."
- "Prompts that worked well on older models may need tuning. Use precise language. The model may prioritize the exact wording of an instruction over the broader behavior you intended. Broad or rigid rules can dominate the assistant's behavior in surprising ways, especially when multiple rules overlap."
- "Be careful with constraint words such as `must`, `only`, `never`, and `always`. Use them when the behavior is truly required, not as general emphasis. Overusing hard constraints can make the assistant rigid, overly cautious, or unable to handle reasonable exceptions."
- "Start with `low` for most production voice agents. Tune up or down based on task complexity, latency tolerance, and failure cost."
- Effort table: `minimal` "Lowest latency matters most and the task is simple."; `low` "You need responsiveness plus basic reasoning."; `medium` "The assistant must reason through multi-step tasks."; `high` "Deeper reasoning materially improves success."; `xhigh` "Maximum reasoning is worth added latency and cost."
- Model page: gpt-realtime-2 is "our most capable realtime voice model. It supports speech-to-speech interactions with configurable reasoning effort, stronger instruction following, and more reliable tool use for complex voice-agent workflows." and "Higher reasoning effort can increase latency and output token usage." gpt-realtime-2.1: "updates GPT-Realtime-2 with improved alphanumeric recognition, silence and noise handling, and interruption behavior." Context 128,000, max output 32,000, one snapshot `gpt-realtime-2.1`. (https://developers.openai.com/api/docs/models/gpt-realtime-2 , .../gpt-realtime-2.1)
- Literal trap example from the guide (summarized by fetch, not verbatim): a narrow rule "When a confirmation code is provided, repeat it verbatim and wait for yes" may not fire when the user gives an order ID; the better rule lists all identifier types. Lesson for you: a rule worded around one trigger ("greet by name then ask 3 questions") may be applied only when the model's reading of "greet" matches; spell out the first action and its trigger.

Migration notes, verbatim (gpt-realtime-2 tab, "Migrate from earlier realtime models"):

```text
When migrating from earlier realtime models, treat the prompt as a behavior surface, not just text to port.

1. Use Codex or a strong reasoning model to restructure the prompt around the latest Realtime prompting guidance. Include a link to this prompting guide to ground the migration in best practices.
2. Set reasoning effort to `low` instead of the default. Increase only for workflows that require deeper planning.
3. Audit tool names, parameters, enums, JSON schemas, and other settings to make sure they match the expected implementation.
4. Remove stale examples. Add short examples for happy paths, ambiguity, interruptions, tool calls, and fallback behavior.
5. Compare representative conversations before and after migration. Check for regressions against an existing eval and document intentional behavior changes.
6. Run a final consistency pass. Confirm the prompt clearly separates hard requirements, defaults, tool rules, safety rules, and fallback behavior.
7. Run evals, inspect representative failures, and iterate on the prompt until the target behaviors are reliable.
```

Also relevant (1.5 tab General Tips, verbatim): "Prefer bullets over paragraphs: Clear, short bullets outperform long paragraphs." "Be precise: Ambiguity or conflicting instructions = degraded performance similar to GPT-5." "Iterate relentlessly: Small wording changes can make or break behavior."

Preambles and channels (relevant to a "weird first utterance" hypothesis, NOT confirmed): gpt-realtime-2 can emit a `commentary` channel (preambles, "Before calling tools in the commentary channel, briefly tell the user what you are doing.") and a `final` channel. The guide says to avoid preambles for direct answers. A reasoning model at `medium` may add short spoken bridges before the real content; whether this explains your generic opener is unknown. Hypothesis only.

Community datapoint (level 4): one developer on the 2.1 announcement thread reported "More prompt engineering required for equivalent behaviour" when moving from the older mini to 2.1-mini. Not OpenAI guidance.

Not found: any OpenAI statement that higher reasoning effort improves instruction following or script adherence; any statement on maximum useful prompt length for gpt-realtime-2/2.1 (GPT-Live states instructions up to 16,384 tokens, different product); any 2.1 vs 2 prompting differences.

## 7. Q6: Language handling for non-English (Polish)

- Official Realtime statement on prompt language (English vs target): NOT FOUND. The gpt-realtime-2 page says nothing on it ("The page does not specify whether the system prompt itself should be written in English or the target language" per the fetch; all examples are English).
- Official pattern (1.5 tab, Personality and Tone): English prompt text that declares the speaking language in a Language section, French tutor example, verbatim:

```text
# Role & Objective
- You are a friendly, knowledgeable voice tutor for French learners.
- Your goal is to help the user improve their French speaking and listening skills through engaging conversation and clear explanations.
- Balance immersive French practice with supportive English guidance to ensure understanding and progress.

# Personality & Tone
## Personality
- Friendly, calm and approachable expert customer service assistant.

## Tone
- Warm, concise, confident, never fawning.

## Length
- 2-3 sentences per turn.

## Language
### Explanations
Use English when explaining grammar, vocabulary, or cultural context.

### Conversation
Speak in French when conducting practice, giving examples, or engaging in dialogue.
```

  and the Role example "You are a Quebecois French-speaking customer service bot. Your task is to answer the user's question." (English prompt, French output). Language pinning, verbatim (1.5 tab): "Control language: Pin output to a target language if you see unwanted language switching." and

```text
- The conversation will be only in English.
- Do not respond in any other language even if the user asks.
- If the user speaks another language, politely explain that support is limited to English.
```

- gpt-realtime-2 tab: "A user's accent is not the same as their intended language." Do NOT use broad rules like "Mirror the user. Respond naturally in the user's language. Switch languages when appropriate." (listed as an example to avoid). Template to adapt (verbatim, English default; swap English for Polish):

```text
## Language

English is the default response language.

- Do not infer language from accent alone.
- Ignore short filler sounds, backchannels, and isolated foreign words for
  language detection.
- Only switch languages if the user explicitly asks or provides a substantive
  utterance in another language.
- If language confidence is low, ask a short clarification instead of guessing.
- Keep preambles, spoken bridges, tool-related messages, and final answers in
  the same language.
- Accent adaptation must not change the response language.
```

- Unclear-audio example in the 2 tab uses an ENGLISH phrase: "ask for clarification using a short English phrase such as 'Sorry, could you repeat that clearly?'". For Polish, the phrase should be Polish (inference). The gpt-realtime-2 voice-prompting variant says "ask for clarification using a short English phrase", consistent.
- Accent: "Speak English with a light Australian accent. Keep the accent stable from the first word to the last. ... Do not change response language based on the user's accent." Pattern generalises to "Speak Polish with a standard Polish accent" (inference).
- Different product, explicit statement: GPT-Live guide, "Language and pronunciation": "Write the prompt and examples in the language you want the assistant to speak, and specify any pronunciations that matter." with template `Speak [language] unless the user asks to switch.` and `Say the user's name Rosalia as "roh-sah-LEE-ah", IPA /rosaˈli.a/ (Spanish).` (https://developers.openai.com/api/docs/guides/live-prompting). It is NOT stated for Realtime; treat as a hint, not a rule.
- Net (my reasoning): the official evidence supports "English instructions + explicit Language section + Polish sample phrases" as a safe hybrid, with the exact opening line itself in Polish. No source says one is strictly better.

## 8. Personality & Tone examples (verbatim) and first-turn examples (index)

Personality & Tone, original guide snippets (1.5 tab):

```text
# Personality & Tone
## Personality
- Friendly, calm and approachable expert customer service assistant.

## Tone
- Warm, concise, confident, never fawning.

## Length
2-3 sentences per turn.
```

```text
## Language
- The conversation will be only in English.
- Do not respond in any other language even if the user asks.

## Pacing
- Deliver your audio response fast, but do not sound rushed.
- Do not modify the content of your response, only increase speaking speed.
```

Realtime-agents repo (authentication agent) Personality and Tone is a longer block ("a calm, approachable online store assistant", "a dedicated snowboard enthusiast", tone "warm and conversational, with a subtle undercurrent of excitement for snowboarding"); I could only retrieve it in summarized form.

First-turn examples: see 3.2 (docs "Say exactly"), 3.3 (SIP sample, realtime-agents `hi`, GPT-Live greet).

## 9. NOT confirmed / not found (consolidated)

1. Official wording like "do not skip steps" or "move to next step only when" for gpt-realtime-2: not found. Only "Exit when:" convention and dynamic per-phase `session.update`.
2. Any OpenAI statement that the model can ignore session instructions on the first turn: not found officially; only third-party race report (pipecat #5354) and an unresolved community thread (1357844).
3. Whether response-level `instructions` fully replace or merge with session instructions: only "override ... for this Response only" and one third-party measurement.
4. Top vs bottom placement of per-user context for Realtime, and instructions vs conversation item for survey data: not found. Only the general caching advice (dynamic last) and the 1.5 skeleton (Context early).
5. A gpt-realtime-2.1-specific prompting guide or migration notes 2 -> 2.1: not found (model page and announcement contain none).
6. Default reasoning effort of gpt-realtime-2 / 2.1: not stated in the docs I fetched (migration note says "Set reasoning effort to `low` instead of the default", implying default is higher than low, value not given).
7. Per-response `reasoning` override: reported by one fetch of the reference, not independently re-verified.
8. Whether an English or Polish prompt follows scripts better: not found for Realtime.
9. Full text of the cookbook "Realtime Prompting Guide" (cookbook page truncated by embedded audio; PDF "Seven tips" at https://cdn.openai.com/API/docs/realtime-prompting-guide.pdf could not be parsed here). Content was recovered from the equivalent guide page (1.5 tab).
10. The OpenAI launch posts (openai.com/index/...) returned HTTP 403, so I did not read their instruction-following claims (benchmark chart "Audio MultiChallenge Instruction Following" is only mentioned in the community announcement without numbers).
11. The code of juberti's hello-realtime sample (Val Town) could not be read; the forum reply pointing to it is the only "official-ish" pointer for custom greetings besides the repos above.
12. Whether commentary-phase preambles at `medium` effort cause the generic opener: untested hypothesis.

## 10. Sources

1. Using realtime models / Prompting Realtime models (gpt-realtime-2 tab and gpt-realtime-1.5 tab) - https://developers.openai.com/api/docs/guides/realtime-models-prompting (undated, producer docs)
2. Prompting Realtime models (voice-prompting) - https://developers.openai.com/api/docs/guides/voice-prompting (undated, producer docs)
3. Realtime Prompting Guide (cookbook, Aug 2025 original) - https://developers.openai.com/cookbook/examples/realtime_prompting_guide (partially fetchable)
4. Realtime conversations - https://developers.openai.com/api/docs/guides/realtime-conversations (producer docs)
5. Realtime client events reference - https://developers.openai.com/api/reference/resources/realtime/client-events (producer docs)
6. Realtime server events reference - https://developers.openai.com/api/reference/resources/realtime/server-events (producer docs)
7. Client secrets create reference - https://developers.openai.com/api/reference/resources/realtime/subresources/client_secrets/methods/create (producer docs)
8. Realtime API with WebRTC - https://developers.openai.com/api/docs/guides/realtime-webrtc (producer docs)
9. Realtime costs (prompt caching) - https://developers.openai.com/api/docs/guides/realtime-costs (producer docs)
10. Prompt caching (generic) - https://developers.openai.com/api/docs/guides/prompt-caching (producer docs, not Realtime-specific)
11. Developer notes on the Realtime API - https://developers.openai.com/blog/realtime-api (producer blog, GA of gpt-realtime, 2025)
12. gpt-realtime-2 model page - https://developers.openai.com/api/docs/models/gpt-realtime-2 ; gpt-realtime-2.1 model page - https://developers.openai.com/api/docs/models/gpt-realtime-2.1
13. Announcement gpt-realtime-2.1 - https://community.openai.com/t/new-realtime-models-on-the-api-gpt-realtime-2-1-and-gpt-realtime-2-1-mini/1385896 (OpenAI staff announcement on forum, July 2026); announcement gpt-realtime-2 - https://community.openai.com/t/new-realtime-voice-models-in-the-api/1380471 (May 2026)
14. API changelog - https://developers.openai.com/api/docs/changelog (GPT-Live GA entry 2026-09-10)
15. openai-realtime-agents (App.tsx, chatSupervisor/index.ts, customerServiceRetail/authentication.ts) - https://github.com/openai/openai-realtime-agents (producer repo, main)
16. openai-agents-python Twilio SIP example (server.py, agents.py) - https://github.com/openai/openai-agents-python/tree/main/examples/realtime/twilio_sip ; Agents Python realtime guide - https://openai.github.io/openai-agents-python/realtime/guide/
17. GPT-Live: Prompting GPT-Live - https://developers.openai.com/api/docs/guides/live-prompting ; Managing GPT-Live sessions - https://developers.openai.com/api/docs/guides/live-conversations ; Voice agents comparison - https://developers.openai.com/api/docs/guides/voice-agents (different product, labelled where used)
18. Trail only (level 4): community thread on consistent greeting - https://community.openai.com/t/how-can-i-get-a-consistent-initial-greeting/1357844 ; community thread speak first (Agents JS) - https://community.openai.com/t/make-agent-speak-first-when-using-realtimesession/1328354 ; community thread on starting conversations - https://community.openai.com/t/openai-realtime-api-for-voice-how-can-i-make-ai-assistant-to-begin-the-conversation/1149489 ; pipecat issue - https://github.com/pipecat-ai/pipecat/issues/5354 ; MulmoChat PR - https://github.com/receptron/MulmoChat/pull/244 ; Microsoft Learn Realtime doc - https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/realtime-audio
