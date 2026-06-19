"""
The shared graph state.

In LangGraph everything flows through a single State object that nodes read
from and write to. This TypedDict is the "memory" that carries the athlete's
recovery across days.
"""

from typing import TypedDict, List


class RecoveryState(TypedDict):
    # --- Athlete context ---
    name: str
    injury_stage: str          # e.g. "early", "mid", "late"
    current_load: float        # today's physical load

    # --- Daily feedback (the human-in-the-loop input) ---
    day: int
    pain: int                  # 0-10
    mood: int                  # 0-10

    # --- Decision computed from the feedback ---
    decision: dict             # output of science.adjust_plan

    # --- Plans produced by the agents ---
    physical_plan: str
    mental_plan: str

    # --- Running history of all days ---
    history: List[dict]
