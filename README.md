<div align="center">
  <img src="https://raw.githubusercontent.com/Linux5Real/Linux5Real/main/assets/finance-telemetry/finance-hero.png?v=3" alt="Linus / Linux5Real — Finance AI desk" />
</div>

---

## [01] DESK PROFILE

I am Linus, building private AI systems where stocks, live market context, model routing, and execution workflow meet.

I am not interested in generic AI wrappers or polished demo software with no operating depth behind it. My focus is building tools that sharpen real market decisions before, during, and after execution.

### Operator Bias

- swing-to-day trading focus
- signal quality over noise
- market context over isolated prompts
- private systems before public packaging
- execution discipline over automation theater

### Working Style

- Linux, Debian, Git, GitHub, VS Code
- builder-first mindset with fast iteration
- AI-native workflow with live model testing
- earlier FiveM scripting background with shipped work
- systems built for actual use, not presentation

---

## [02] ACTIVE POSITION — FINANCE AI PLATFORM

> A private finance workspace built around deterministic execution, institutional tick data, and calibrated AI routing: dual-core architecture combining a 1-minute market volatility measurement engine with a strict execution journal.

The project is a live private trading platform built around actual market mechanics, not LLM predictions. It enforces strict mathematical boundaries (G1/G2/G3), separating deterministic Python calculations from AI synthesis to eliminate hallucination and maintain absolute execution discipline.

### Current Surface

<div align="center">
  <img src="https://raw.githubusercontent.com/Linux5Real/Linux5Real/main/assets/finance-telemetry/table-current-surface.png?v=3" alt="Current Surface" />
</div>

### Current System Layer

<div align="center">
  <img src="https://raw.githubusercontent.com/Linux5Real/Linux5Real/main/assets/finance-telemetry/table-system-layer.png?v=3" alt="Current System Layer" />
</div>

### Why It Exists

- eliminate AI hallucination through deterministic pre-computed metrics
- keep rich market context and order book depth attached to every decision
- log execution quality (MAE / MFE / slippage) to evaluate statistical edge
- enforce pre-trade checklists and risk boundaries before capital deployment
- reach the desk everywhere: browser, TradingView overlay, iPhone, Windows desktop, voice and phone-call alerts
- build a private operator stack grounded in real data before considering public releases

---

## [03] MODEL DESK

`Python` `Flask` `FastAPI` `PostgreSQL` `SQLite` `ChromaDB` `Databento (XNAS.ITCH)` `TradingView` `OpenRouter` `Docker`

The model layer is governed by the **10 Binding Rules**: the LLM never calculates prices, percentages, or indicators. All metrics are computed deterministically in Python before being passed as read-only context.

- **User-picked models** — `DeepSeek V4.1 Flash` · `GPT 5.6 Luna` · `GPT 5.6 Sol` · `Grok 4.7` · `Gemini 3.8 Flash`, chosen per chat and never hardcoded. New OpenAI-compatible models plug in by config, no code change.
- **No sampling tuning** — no temperature, no top-p, no reasoning budget. Only `max_tokens` per mode; the context window belongs to the model.
- **Visible smart routing** — models are health-checked every 60 s. A request is rerouted only when the chosen model is measurably down, and the reroute is always announced. No silent fallback.
- **Jev decision layer** — a fast decision model answers yes/no and selection questions at 12 points (search depth, URL triage, headline filter, report updates). Any Jev error falls back to the default path; journal and trade data never leave the app.

---

## [04] WHAT'S NEXT

Execution edge requires empirical proof. The measurement pipeline is in place: Databento 1-minute data is ingested daily and MAE/MFE is recomputed automatically for every logged trade. The open step is the data itself, a statistically significant sample of 150–200 live trades, before any pattern evaluation or risk-adjusted edge claim.

### Near-Term Build Path

<div align="center">
  <img src="https://raw.githubusercontent.com/Linux5Real/Linux5Real/main/assets/finance-telemetry/table-build-path.png?v=3" alt="Near-Term Build Path" />
</div>

---

## [05] TELEMETRY

<div align="center">
  <img src="https://raw.githubusercontent.com/Linux5Real/Linux5Real/main/assets/finance-telemetry/finance-repo-telemetry.png?v=3" alt="Finance AI platform — repo telemetry" />
</div>

<div align="center">
  <img src="https://raw.githubusercontent.com/Linux5Real/Linux5Real/main/assets/finance-telemetry/finance-repo-activity.png?v=3" alt="Finance AI platform — repo activity" />
</div>

---

<div align="center">
  Building private finance AI systems where market context, signal routing, and execution discipline converge.
</div>
