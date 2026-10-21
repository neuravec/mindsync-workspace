---
name: feedback-posthog-instrumentation-mandatory
description: Kazda nowa funkcja/ekran/flow musi na koniec dostac podpiecie do PostHoga z tabela pokrycia zdarzen; regula w CLAUDE.md od 2026-10-02
metadata:
  node_type: memory
  type: feedback
  originSessionId: 11ef1d1a-7b6d-4b0b-b417-08a34feccc91
  modified: 2026-10-02T16:23:24.083Z
---

Podpiecie do PostHoga to obowiazkowy ostatni krok kazdego zadania, na rowni z testami. Zadanie nie jest skonczone bez tabeli pokrycia (surface | akcja | event | properties | plik) i zerowej liczby luk, chyba ze operator jawnie zaakceptuje luke.

**Why:** operator 2026-10-02 przy redesignie subskrypcji i onboardingu: "dodaj w rules projektu ze zawsze jak cos powstaje to podpiecie do posthoga to wymagany step na koncu". Wczesniej braki pomiaru (brak trial_started/trial_ended, paywall niemierzalny) blokowaly diagnozy.

**How to apply:** w kazdym prompcie do agenta implementujacego dopisz wymog tabeli pokrycia i testu zdarzen; na koniec batcha osobny audyt pokrycia. Regula: sekcja "PostHog Instrumentation (Mandatory final step)" w `CLAUDE.md` projektu. Zero wolnego tekstu uzytkownika w eventach. Powiazane: [[project-subscription-redesign-2026-10-02]], [[reference-posthog-integration]].
