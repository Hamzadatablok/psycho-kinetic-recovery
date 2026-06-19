"""
Psycho-Kinetic Recovery — interactive entry point.

Each day you (the athlete) enter your pain and mood. The graph computes the
decision, then the physical and mental agents write tomorrow's dual plan.
State persists across days via the checkpointer (same thread_id), so the
program remembers your history.

Run:  python main.py   (type 'q' as pain to quit)
"""

from graph import build_graph

THREAD_ID = "athlete-yassine"   # same id every day = same memory


def ask_int(label: str) -> int:
    """Ask for a 0-10 value, with simple validation."""
    while True:
        raw = input(label)
        if raw.strip().lower() == "q":
            raise KeyboardInterrupt
        if raw.isdigit() and 0 <= int(raw) <= 10:
            return int(raw)
        print("  Please enter a number from 0 to 10 (or 'q' to quit).")


def main() -> None:
    graph = build_graph()
    config = {"configurable": {"thread_id": THREAD_ID}}

    # The athlete's healthy BASELINE load — the anchor we adjust against.
    # We adjust today's plan relative to this fixed baseline, NOT to
    # yesterday's already-adjusted value (which would spiral downward).
    baseline_load = 400.0
    day = 0

    print("\n🧘 Psycho-Kinetic Recovery — daily check-in")
    print("   (type 'q' at the pain prompt to quit)\n")

    try:
        while True:
            day += 1
            print(f"\n===== Day {day} =====")
            pain = ask_int("Pain today (0-10): ")
            mood = ask_int("Mood today (0-10): ")

            # Run one pass through the graph
            result = graph.invoke(
                {
                    "name": "Yassine",
                    "injury_stage": "mid",
                    "current_load": baseline_load,
                    "day": day,
                    "pain": pain,
                    "mood": mood,
                    "history": [],
                },
                config=config,
            )

            d = result["decision"]
            print(f"\n📊 Decision: next load = {d['next_load']} "
                  f"| mental support = {d['mental_support']} "
                  f"| recovery day = {d['recovery_day']}")
            print("\n🏋️  PHYSICAL PLAN:\n" + result["physical_plan"])
            print("\n🧠 MENTAL PLAN:\n" + result["mental_plan"])

            # Each day is anchored to the fixed baseline, so the plan reflects
            # TODAY's pain/mood — not an accumulating downward error.

    except KeyboardInterrupt:
        print("\n\n👋 Session ended. Recovery progress saved. Take care!")


if __name__ == "__main__":
    main()
