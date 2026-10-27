"""CLI entry point:  python main.py "4-day Mussoorie trip, 3 people, Rs 15000, nature and cafes" """
import sys

from graph import build_graph


def main():
    request = " ".join(sys.argv[1:]) or input("Describe your trip: ")
    app = build_graph()
    final = {}
    for update in app.stream({"request": request, "agent_log": []}, stream_mode="updates"):
        for node, data in update.items():
            for entry in data.get("agent_log", []):
                print(f"[{entry['agent']}] {entry['message']}")
            final.update(data)
    print("\n" + "=" * 60 + "\n")
    print(final.get("itinerary", "No itinerary generated."))


if __name__ == "__main__":
    main()
