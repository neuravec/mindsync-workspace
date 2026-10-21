# Enum drift sweep: model bind labels vs prod `pg_enum` (2026-10-07)

**Author:** database-administrator (read-only)
**Data as of:** 2026-10-07 ~20:00 UTC, prod Postgres (alembic head `m316a1b2c3d4`), slug v568 (`79f1787`)
**Access:** one Heroku one-off dyno (`run.4413`, `--no-tty`, exited on its own). The connection was forced read-only at connect time (`transaction_read_only=on` verified). Only catalog SELECTs were run (`pg_type`/`pg_enum`, `information_schema.columns`). No DML or DDL, no PII.
**Follow-up to:** `2026-10-07-first-conversation-prep-card-missing.md`

## Method

1. Inside the dyno, all 9 modules under `app/models` were imported (`app_insight_shown`, `clinician`, `clinician_v2`, `habit`, `hero_insight`, `models`, `notification_moment`, `user_memory`, `workspace`). Every column in `Base.metadata` whose type is `sqlalchemy.Enum` was enumerated: **34 columns, 20 PG type names**.
2. For each column, the labels SQLAlchemy binds were read from `Column.type.enums`. That is SQLAlchemy's own computed list: member NAMES, or the values if `values_callable` is set. No model uses `values_callable` or `native_enum=False`.
3. The comparison is against the labels of the type **the prod column actually uses** (`information_schema.columns.udt_name`), not only the type name the model declares. Postgres coerces the bound literal to the column's real type.
4. Writer-side sweep (local grep): SQLAlchemy `Enum` does not validate plain strings (`validate_strings=False`), so a raw string literal that is not a member is sent to Postgres as-is. Every `track_usage(...)` / `feature_override` literal was checked against `FeatureEnum` and the prod labels. So was every string literal assigned to a column name that is enum-typed somewhere (`input_type`, `processing_status`, `source_type`, `moment_type`, `role`, and the rest). Those hits were then checked one by one against the actual column type.

## Result table

| pg type (as used by the prod column) | python enum | bound labels missing on prod | extra prod labels | columns using it | known writers of the missing values |
|---|---|---|---|---|---|
| `inputtypeenum` | `InputTypeEnum` | **`AUTO`** | `auto` (0 rows use it) | `session_prep_cards.input_type`, `session_debriefs.input_type`, `between_session_notes.input_type` | `app/tasks/first_conversation_prep_card.py:264`, `app/tasks/prep_card_auto_generate.py:226`, `app/api/v1/endpoints/prep_cards.py:576` (all `InputTypeEnum.AUTO`) |
| `featureenum` | `FeatureEnum` | none from the enum itself; **`MOOD_TREND`** is written as a raw string that is in **neither** `FeatureEnum` nor prod | none | `token_usage_log.feature` | `app/tasks/mood_trend.py:171` `track_usage("MOOD_TREND", "generate_mood_trend_summary", ...)`; fails hourly (prod log 2026-10-07 19:00:58, `invalid input value for enum featureenum: "MOOD_TREND"`) |
| `apitypeenum` | `ApiTypeEnum` | none | none | `model_pricing.api_type`, `token_usage_log.api_type` | |
| `chart_name_enum` (model says `chartnameenum`) | `ChartNameEnum` | none | none | `ai_chart_explanations.chart_name` | |
| `conversationtypeenum` | `ConversationTypeEnum` | none | none | `conversations.conversation_type` | |
| `first_day_enum` (model says `firstdayenum`) | `FirstDayEnum` | none | none | `user_profile.first_day_of_week` | |
| `form_factor_enum` | `FormFactorEnum` | none | none | `app_insights_shown.form_factor` | |
| `genderenum` | `GenderEnum` | none | none | `user_profile.gender` | |
| `goalstatusenum` | `GoalStatusEnum` | none | none | `user_goals.status` | |
| `insight_type_enum` | `InsightTypeEnum` | none | none | `app_insights_shown.insight_type` | |
| `moment_status_enum` | `MomentStatusEnum` | none | none | `notification_moments.status` | |
| `moment_type_enum` | `MomentTypeEnum` | none | none | `notification_moments.moment_type` | |
| `period_scope_enum` (model says `periodscopeenum`) | `PeriodScopeEnum` | none | none | `ai_chart_explanations.time_scope` | |
| `processingstatusenum` | `ProcessingStatusEnum` | none | none | 13 columns: `between_session_notes`, `hero_insights`, `monthly_therapy_audits`, `period_snapshots`, `reflect_summary_cards`, `session_debriefs`, `session_prep_cards`, `session_recordings`, `therapy_health_checks`, `therapy_tracking_signals`, `user_goals`, `weekly_therapy_summaries` (`.processing_status`) | |
| `ragsourceenum` | `RAGSourceEnum` | none | none | `rag_documents.source_type` | |
| `roleenum` | `RoleEnum` | none | none | `messages.role` | |
| `statusenum` | `StatusEnum` | none | none | `conversations.status` | |
| `subenum` | `SubEnum` | none | none | `user_subscription.subscription_type` | |
| `symptomsuggestionstatusenum` | `SymptomSuggestionStatusEnum` | none | none | `symptom_suggestions.status` | |
| `voicetypeenum` | `VoiceTypeEnum` | none | none | `user_preferences.agent_voice` | |

**Confirmed:** `inputtypeenum` is missing `AUTO`, and `featureenum` is missing `MOOD_TREND`. These are the only two labels missing on prod.

## Other structural findings

1. **No Python enum is missing its PG type on prod.** All 20 model-declared type names exist.
2. **Twin types: three columns use a different type than the model names.** Prod has both twins, with identical labels today:
   - `ai_chart_explanations.chart_name` uses `chart_name_enum` (the model names `chartnameenum`)
   - `ai_chart_explanations.time_scope` uses `period_scope_enum` (the model names `periodscopeenum`)
   - `user_profile.first_day_of_week` uses `first_day_enum` (the model names `firstdayenum`)

   No bind problem now. But a future migration that adds a label must alter the **snake_case** type the column actually uses, ideally both twins, or the new value will be rejected even though "the enum has it".
3. **Prod enum types not referenced by any model column:** `chart_name_enum`, `period_scope_enum`, `first_day_enum` (these are the twins above, and the prod columns do use them), plus `uploadsessionstatusenum` (`in_progress`, `completed`, `aborted`). That last one is an orphan, left over from before `UploadSession.status` moved to `String` (the 2026-06-21 H10 incident). It is harmless, and dropping it is optional cleanup, not part of this fix.
4. Writer-side literal sweep: 41 literal hits, all false positives. They are comments, prompt labels (`role = "User"`), the `input_type="AUTO"` argument passed to the model prompt (not the DB), and `String` columns with CHECK constraints (`clinician_voice_notes`, `clinician_brief_cache`, workspace `source_type`, `therapy_health_checks.input_type="QUICK"`). Apart from `MOOD_TREND`, no raw string reaches an enum column with a label prod lacks.

## Migration guidance for backend-api

One idempotent migration, with the `ADD VALUE` statements inside `op.get_context().autocommit_block()` per project convention:

```python
op.execute("ALTER TYPE inputtypeenum ADD VALUE IF NOT EXISTS 'AUTO'")
op.execute("ALTER TYPE featureenum ADD VALUE IF NOT EXISTS 'MOOD_TREND'")
```

- **`AUTO`**: no code change needed. `InputTypeEnum.AUTO` already binds `'AUTO'`. Do not switch the column to `values_callable`, because `VOICE`/`TEXT` would then bind as `voice`/`text`, which prod rejects. The lowercase `auto` label stays as an unused orphan (0 rows). After the upgrade, the three AUTO writers start working, including the hourly cron, which has never produced a card on prod.
- **`MOOD_TREND`**: also add `MOOD_TREND = "MOOD_TREND"` to `FeatureEnum` in `app/models/models.py`, **in the same deploy as, or before, the label goes live**. If the PG label exists while the Python enum lacks the member, inserts succeed, but any ORM load of those `TokenUsageLog` rows raises `LookupError` in SQLAlchemy's enum result processor. The ORM reader is `app/crud/usage.py:48-71` (it queries `TokenUsageLog` and groups by `feature`). Shipping the Python member alone is harmless (the insert just keeps failing, as it does today).
- Sequence: deploy (with the `FeatureEnum` member), then `heroku run alembic upgrade head --app mindsync` right away (there is no release phase), then verify with `SELECT enumlabel FROM pg_enum JOIN pg_type ... WHERE typname IN ('inputtypeenum','featureenum')`.
- Guard against recurrence (CLAUDE.md rule 4): a Postgres-dialect test that, for every `Enum` column in `Base.metadata`, asserts `Column.type.enums` is a subset of the labels the migrations declare. Also add a lint or test that `track_usage` feature literals are members of `FeatureEnum`.

## Reproduce

Script (scratchpad, not committed): `enum_src.py`, wrapped in the chunked `exec(compile(...))` runner and piped through `heroku run --no-tty -a mindsync python`. Core of it:

```python
for t in Base.metadata.sorted_tables:
    for c in t.columns:
        if isinstance(c.type, sqlalchemy.Enum):
            c.type.name, list(c.type.enums)           # what SQLAlchemy binds
# vs
SELECT t.typname, e.enumlabel FROM pg_type t JOIN pg_enum e ON e.enumtypid=t.oid ORDER BY 1, e.enumsortorder;
SELECT table_name, column_name, data_type, udt_name FROM information_schema.columns WHERE table_schema='public';
```
