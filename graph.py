"""
Build the recovery graph.

Flow each day:
    feedback  ->  physical  ->  mental  ->  END

- feedback runs the deterministic decision.
- physical and mental then phrase the plan.
A MemorySaver checkpointer persists the state across days (same thread_id),
so the program remembers the athlete's history between runs.
"""

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from state import RecoveryState
from nodes import feedback_node, physical_node, mental_node


def build_graph():
    # 1) Create the graph bound to our state schema
    builder = StateGraph(RecoveryState)

    # 2) Register the nodes
    builder.add_node("feedback", feedback_node)
    builder.add_node("physical", physical_node)
    builder.add_node("mental", mental_node)

    # 3) Wire the edges (the path)
    builder.add_edge(START, "feedback")
    builder.add_edge("feedback", "physical")
    builder.add_edge("physical", "mental")
    builder.add_edge("mental", END)

    # 4) Compile with memory so state persists across days
    checkpointer = MemorySaver()
    return builder.compile(checkpointer=checkpointer)
