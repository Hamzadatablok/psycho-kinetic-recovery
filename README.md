# 🧘 Psycho-Kinetic Recovery — Dual Physical + Mental Rehab (LangGraph)

Most sports rehab programs treat the body and ignore the mind.
**Psycho-Kinetic Recovery** adapts *both* every single day.

Built with **LangGraph** as a stateful graph: the athlete checks in daily with
their pain and mood, and the system adjusts tomorrow's physical load **and**
mental-support plan accordingly — remembering progress across days.

---

## ⚙️ How It Works

```
        Daily check-in (pain, mood)   ← human-in-the-loop
                    │
                    ▼
            ┌───────────────┐
            │  feedback     │  ← deterministic decision (science.adjust_plan)
            └───────┬───────┘
                    ▼
            ┌───────────────┐
            │  physical     │  ← Physical Rehab agent writes the body plan
            └───────┬───────┘
                    ▼
            ┌───────────────┐
            │  mental       │  ← Mental Resilience agent writes the mind plan
            └───────┬───────┘
                    ▼
        Tomorrow's dual plan + saved history
```

- **State persists** across days via a `MemorySaver` checkpointer.
- **Decision is deterministic**: pain drives physical load, mood drives mental
  support, and a safety override forces a full recovery day when pain is high
  AND mood is low.
- **Anchored to a baseline** so the plan reflects today's status, never an
  accumulating downward error.

---

## 🛠️ Tech Stack

- **LangGraph** — stateful, multi-actor graph with checkpointing
- **LangChain + OpenRouter** — LLM access
- Deterministic decision logic in `science.py` (reused & extended from my
  earlier injury-prediction projects)

---

## 🚀 Quick Start

```bash
python -m venv venv
venv\Scripts\activate              # Windows
pip install -r requirements.txt
copy .env.example .env             # add your OpenRouter key
python main.py                     # daily interactive check-in (type 'q' to quit)
```

---

## 📂 Structure

| File | Role |
|------|------|
| `science.py` | Deterministic logic: ACWR + `adjust_plan` dual-recovery rule |
| `state.py` | The shared `RecoveryState` (the graph's memory) |
| `nodes.py` | The three graph nodes (feedback, physical, mental) |
| `graph.py` | Builds & compiles the LangGraph with a checkpointer |
| `main.py` | Interactive daily entry point |

---

## ⚠️ Disclaimer

This is an educational project, not a medical diagnostic tool.

## 👤 Author

**Hamza Elouahdani** — Data Scientist & Sports Performance Specialist
