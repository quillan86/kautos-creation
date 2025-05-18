from src.events import EventsExtractor
from src.llm import LLM
from src.generator import Generator
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

    event = generator.complete_event("Tin Bronze invented", 1000, near=True, symmetric=False)
    print(json.dumps(event, indent=4))