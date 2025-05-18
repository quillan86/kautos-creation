from src.events import EventsExtractor
import json


if __name__ == "__main__":
#    events = EventsExtractor().get_similar_events(
#        start_year=-670, end_year=-660, location="Lower Antiyan Basin", near=True
#    )

#    print(json.dumps(events, indent=4))

    events = EventsExtractor().get_similar_events_to_event("Sîdanêgi Empire Foundation through conquest of Merkuna", 300, near=True)
    print(json.dumps(events, indent=4))