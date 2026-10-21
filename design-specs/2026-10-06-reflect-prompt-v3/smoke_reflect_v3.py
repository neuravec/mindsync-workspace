def smoke():
    import json
    from app.core.config import settings
    from app.models import models
    from app.services import reflect_prompt as rp
    from app.services import reflect_entry as rentry
    from app.services import first_conversation as fc
    from app.services import openai_audio_service as oas
    out = {"prompt_version": rp.PROMPT_VERSION, "GPT_AGENT_MODEL": settings.GPT_AGENT_MODEL, "REALTIME_REASONING_EFFORT": settings.REALTIME_REASONING_EFFORT, "LEGACY_REALTIME_KEY": settings.LEGACY_REALTIME_KEY, "REFLECT_SYSTEM_MESSAGE_len": len(settings.REFLECT_SYSTEM_MESSAGE or "")}
    ctx = rp.ReflectContext(first_name="Ania", language="Polish", grammatical_gender="feminine", tone_archetype="friend")
    seed = rentry.ReflectSeed(source="prep_card", source_id=1, label="Rozmowa z szefem", context=None, verified_owner=True)
    prompts = {"voice_fresh": rp.build_prompt(ctx, "voice", seed=None, has_user_turns=False), "voice_seeded": rp.build_prompt(ctx, "voice", seed=seed, has_user_turns=False), "text_seeded": rp.build_prompt(ctx, "text", seed=seed, opening_question="Co w tym jest najtrudniejsze?", has_user_turns=False)}
    checks = {}
    for name, p in prompts.items():
        checks[name] = {"chars": len(p), "safety": ("SAFETY AND ESCALATION" in p) and ("THIS SECTION OVERRIDES EVERYTHING ELSE" in p), "about_heading": rp.ABOUT_HEADING in p, "no_dashes": (chr(0x2014) not in p) and (chr(0x2013) not in p), "no_placeholders": "{" not in p, "greeting_block": "OPENING GREETING" in p, "opening_turn_block": "OPENING TURN" in p}
    out["checks"] = checks
    out["start_event_voice"] = rp.start_event_properties(models.ConversationModality.VOICE.value)
    out["start_event_text"] = rp.start_event_properties("text")
    out["first_conversation_model"] = fc.realtime_model()
    out["first_conversation_overrides"] = fc.client_session_overrides()
    captured = {}
    def fake_post(body):
        captured["body"] = body
        return "ek_smoke_not_minted"
    oas.log_token_usage = lambda **kw: None
    oas.audio_service._post_client_secrets_raw = fake_post
    res = oas.audio_service.create_realtime_session(instructions=prompts["voice_fresh"], voice="marin", language="pl")
    sess = captured.get("body", {}).get("session", {})
    out["mint_body_model"] = sess.get("model")
    out["mint_body_reasoning"] = sess.get("reasoning")
    out["mint_client_session_config_reasoning"] = (res.client_session_config or {}).get("reasoning")
    out["mint_instructions_is_v3"] = sess.get("instructions") == prompts["voice_fresh"]
    ok = rp.PROMPT_VERSION == "reflect-v3" and all(c["safety"] and c["about_heading"] and c["no_dashes"] for c in checks.values()) and checks["voice_fresh"]["greeting_block"] and checks["voice_seeded"]["opening_turn_block"] and out["mint_body_model"] == settings.GPT_AGENT_MODEL
    out["SMOKE_OK"] = bool(ok)
    print(json.dumps(out, indent=1, ensure_ascii=False, default=str))

smoke()
