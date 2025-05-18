from src.backend.generator import Generator
import json


if __name__ == "__main__":
    #    events = EventsExtractor().get_similar_events(
    #        start_year=-670, end_year=-660, location="Lower Antiyan Basin", near=True
    #    )

    #    print(json.dumps(events, indent=4))
#    event, events = EventsExtractor().get_similar_events_to_event(
#        "Sîdanêgi Empire Foundation through conquest of Merkuna", 300, near=True, symmetric=False
#    )
#    print(json.dumps(event, indent=4))
#    print(json.dumps(events, indent=4))

    generator = Generator()
#    event = generator.generate_similar_event("Sîdanêgi Empire Foundation through conquest of Merkuna", 300, near=True, symmetric=True)
#    print(json.dumps(event, indent=4))

#    event = generator.generate_event_in_range(-1200, -1000, -1400, -1000, "Tirlarli Littoral", near=True)

    event = generator.complete_event("Apollonian Migration to Lower Antiya begins", 600, near=True, symmetric=False)

    print(json.dumps(event, indent=4))

    with open("local/output.json", "w") as f:
        json.dump(event, f, indent=4)
        print(f"Event Description:\n{event.get('description')}")
