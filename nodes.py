"""
Graph nodes. In LangGraph a "node" is just a function:
it receives the current state and returns a dict of fields to update.

- feedback_node : runs the deterministic decision (science.adjust_plan)
- physical_node : the Physical Rehab agent writes the body plan
- mental_node   : the Mental Resilience agent writes the mind plan
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from state import RecoveryState
from science import adjust_plan

load_dotenv()

# Shared LLM, routed through OpenRouter
llm = ChatOpenAI(
    model=os.getenv("MODEL_NAME", "openai/gpt-4o-mini"),
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.3,
)


# ---------- Node 1: Feedback / decision (deterministic, no LLM) ----------
def feedback_node(state: RecoveryState) -> dict:
    """Turn the athlete's pain & mood into a concrete decision."""
    decision = adjust_plan(
        pain=state["pain"],
        mood=state["mood"],
        current_load=state["current_load"],
    )
    return {"decision": decision}


# ---------- Node 2: Physical Rehab agent ----------
def physical_node(state: RecoveryState) -> dict:
    """Generate the physical rehab plan for tomorrow."""
    d = state["decision"]
    prompt = (
        f"You are a physical rehabilitation specialist. "
        f"Injury stage: {state['injury_stage']}. "
        f"Tomorrow's target load: {d['next_load']} "
        f"(factor {d['load_factor']}). Recovery day: {d['recovery_day']}. "
        f"Reasons: {d['reasons']}. "
        f"Write a short, concrete physical plan for tomorrow (3-4 bullet points). "
        f"If it is a recovery day, prescribe gentle recovery only."
    )
    response = llm.invoke(prompt)
    return {"physical_plan": response.content}


# ---------- Node 3: Mental Resilience agent ----------
def mental_node(state: RecoveryState) -> dict:
    """Generate the mental resilience plan for tomorrow."""
    d = state["decision"]
    prompt = (
        f"You are a sports mental-resilience coach. "
        f"The athlete reported pain {state['pain']}/10 and mood {state['mood']}/10. "
        f"Required mental support level: {d['mental_support']}. "
        f"Write a short, concrete mental plan for tomorrow (3-4 bullet points): "
        f"breathing, meditation, visualization or motivation as appropriate. "
        f"Be supportive and avoid clinical claims."
    )
    response = llm.invoke(prompt)
    return {"mental_plan": response.content}
