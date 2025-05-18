import json
from src.backend.llm import LLM
from src.backend.events import EventsExtractor
from src.backend.schemas import Event

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
        You are a creative historian and world-builder for the fictional realm of Kautos.
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
    
    def _craft_system_prompt_generate_event(self) -> str:
        return """
        You are a creative historian and world-builder for the fictional realm of Kautos.
        Your primary task is to generate a new, plausible historical event that occurs *within a specified time range and location*.
        You will be provided with:
        1. A target **Time Range** (e.g., -500 to -450) for the new event you must create.
        2. A list of **Contextual Events** from Kautos. These events may be from a similar period or location and serve as inspiration and background.

        When crafting the new event, you must adhere to the following guidelines:
        - **Strict Temporal Adherence:** The new event's start and end years *must fall entirely within the provided target Time Range*.
        - **Strict Spatial Adherence:** The new event's location *must be the same as the provided location*.
        - **Contextual Consistency:** The new event should be thematically and historically consistent with the provided list of Contextual Events. It should feel like it belongs to the same general era, region, or narrative tapestry of Kautos.
        - **Historical Plausibility (within Kautos):** The event must be plausible within the established lore, cultures, geography, magical systems, and known history of Kautos.
        - **Narrative Clarity:** The event should be described clearly, with a discernible beginning, development, and outcome or significance.
        - **Originality:** While drawing inspiration from the contextual events, the new event must be unique and not a direct copy or slight rephrasing of an existing one.
        
        The output must be a single, well-described event that fits all criteria. Pay close attention to the specified Time Range and Location for the new event.
        """

    def generate_similar_event(self, event_name: str, delta_year: int, near: bool = True, symmetric: bool = True) -> dict:
        """
        Generate a similar event to the given event.

        Args:
            event_name: The name of the event to generate a similar event for.
            delta_year: The number of years to offset the event by.
            near: Whether to generate a similar event in the same region.
            symmetric: Whether to generate a similar event in the same time range.

        Returns:
            dict: The generated event.
        """
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
        user_prompt = f"Event:\n```\n{json.dumps(event, indent=4)}\n```\nSimilar Events:\n```\n{json.dumps(events, indent=4)}\n```"
        return self.llm.generate(system_prompt, user_prompt, tools=tools, tool_choice=tool_name, temperature=0.7)
    
    def complete_event(self, event_name: str, delta_year: int, near: bool = True, symmetric: bool = True) -> dict:
        """
        Complete the event.

        Args:
            event_name: The name of the event to complete.
            delta_year: The number of years to offset the event by.
            near: Whether to generate a similar event in the same region.
            symmetric: Whether to generate a similar event in the same time range.

        Returns:
            dict: The completed event.
        """

        # extract the event and similiar events.
        event, events = self.events_extractor.get_similar_events_to_event(event_name, delta_year, near, symmetric)

        print(f"queried event: {json.dumps(event, indent=4)}")
        
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
        user_prompt = f"Event to Complete:\n```\n{json.dumps(event, indent=4)}\n```\nSimilar Events:\n```\n{json.dumps(events, indent=4)}\n```"
        return self.llm.generate(system_prompt, user_prompt, tools=tools, tool_choice=tool_name, temperature=0.7)

    def generate_event_in_range(self, start_year: int, end_year: int, range_start_year: int, range_end_year: int, location: str, near: bool = True) -> dict:
        """
        Generate a new event within a given time range.

        Args:
            start_year: The start year of the event.
            end_year: The end year of the event.
            range_start_year: The start year of the range for contextually seached events.
            range_end_year: The end year of the range for contextually seached events.
            location: The location of the event.
            near: Whether to generate a similar event in the same region.

        Returns:
            dict: The generated event.
        """
        events = self.events_extractor.get_similar_events_in_range(range_start_year, end_year=range_end_year, location=location, near=near, exclude_event=None)
        event_schema = Event.model_json_schema()
        tool_name = "generate_event_in_range"

        tools = [
            {
                "name": tool_name,
                "description": "Generate a new event within a given time range. The event should be a single event, not a list of events.",
                "input_schema": event_schema,
            }
        ]

        system_prompt = self._craft_system_prompt_generate_event()
        user_prompt = f"Time Range:\n```\n{start_year} to {end_year}\n```\nLocation:\n```\n{location}\n```\nEvents:\n```\n{json.dumps(events, indent=4)}\n```"
        return self.llm.generate(system_prompt, user_prompt, tools=tools, tool_choice=tool_name, temperature=0.7)