import json
from src.llm import LLM
from src.events import EventsExtractor
from src.schemas import Event

class Generator:
    def __init__(self):
        self.llm = LLM()
        self.events_extractor = EventsExtractor()

    def _craft_system_prompt_similar_event(self) -> str:
        return """
        You are a creative historian and world-builder for the fictional realm of Kautos.
        Your task is to generate a new, plausible event that is thematically and historically similar to a provided seed event and its context.
        You will be given details of an existing event from Kautos and a list of other events that share similarities.
        
        Consider the following when crafting the new event:
        - **Thematic Resonance:** What are the core themes (e.g., conquest, discovery, betrayal, innovation) of the seed event? The new event should echo these themes.
        - **Historical Plausibility (within Kautos):** How would such an event unfold in the world of Kautos? Consider its cultures, geography, and known history.
        - **Causality and Consequence:** The new event should feel like it could logically precede or follow events similar to the seed, or run parallel to them, perhaps in a different region or involving different factions.
        - **Uniqueness:** While similar, the new event should be distinct and not a mere copy of the seed event.
        
        The output should be a single, well-described event. Focus on a clear and engaging narrative for this new event.
        """

    def _craft_system_prompt_complete_event(self) -> str:
        return """
        You are a meticulous chronicler and lore-keeper for the fictional realm of Kautos.
        Your task is to take an existing event description from Kautos and enrich it, filling in missing details and expanding upon its narrative to make it a more complete and compelling historical account.
        You will be given the current details of an event to be completed and a list of other, similar events from Kautos for context and inspiration.

        When completing the event, consider the following:
        - **Filling Gaps:** Identify any missing information in the provided event description (e.g., specific outcomes, key figures involved, precise dates or durations, underlying causes, broader consequences).
        - **Narrative Cohesion:** Ensure that the new details flow logically with the existing information and the established lore of Kautos.
        - **Historical Consistency (within Kautos):** All added details must align with the known cultures, geography, magical systems, and historical patterns of Kautos.
        - **Drawing Inspiration:** Use the provided list of similar events to understand common patterns, character archetypes, or types of consequences that might be relevant to the event you are completing.
        - **Enhancing Detail & Vividness:** Add descriptive language and specific details to make the event more immersive and historically rich, without altering the core nature of the event if it's already established.
        
        The output should be the completed, single event. Focus on providing a comprehensive and engaging narrative for this event, ensuring all key aspects are addressed.
        """

    def generate_similar_event(self, event_name: str, delta_year: int, near: bool = True, symmetric: bool = True) -> dict:
        # extract the event and similiar events.
        event, events = self.events_extractor.get_similar_events_to_event(event_name, delta_year, near, symmetric)

        event_schema = Event.model_json_schema()
        tool_name = "generate_similar_event"

        tools = [
            {
                "name": tool_name,
                "description": "Generate a similar event to the given event. The event should be a single event, not a list of events.",
                "input_schema": event_schema,
            }
        ]

        # generate the event
        system_prompt = self._craft_system_prompt_similar_event()
        user_prompt = f"Event:\n{json.dumps(event, indent=4)}\nSimilar Events:\n{json.dumps(events, indent=4)}"
        return self.llm.generate(system_prompt, user_prompt, tools=tools, tool_choice=tool_name, temperature=0.7)
    
    def complete_event(self, event_name: str, delta_year: int, near: bool = True, symmetric: bool = True) -> dict:
        # extract the event and similiar events.
        event, events = self.events_extractor.get_similar_events_to_event(event_name, delta_year, near, symmetric)

        event_schema = Event.model_json_schema()
        tool_name = "complete_event"

        tools = [
            {
                "name": tool_name,
                "description": "Complete the event. The event should be a single event, not a list of events.",
                "input_schema": event_schema,
            }
        ]
        
        # generate the event
        system_prompt = self._craft_system_prompt_complete_event()
        user_prompt = f"Event to Complete:\n{json.dumps(event, indent=4)}\nSimilar Events:\n{json.dumps(events, indent=4)}"
        return self.llm.generate(system_prompt, user_prompt, tools=tools, tool_choice=tool_name, temperature=0.7)
    