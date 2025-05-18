from src.backend.constants import NOTION_TOKEN, LOCATION_DATABASE_ID, TIMELINE_DATABASE_ID
from notion_client import Client


class EventsExtractor:
    """
    Extracts events from the Notion database.

    Args:
        start_year (int): The start year of the event
        end_year (int | None): The end year of the event
        location (str | None): The name of the location
        near (bool): Whether to include near locations
    """

    def __init__(self):
        self.client = Client(auth=NOTION_TOKEN)

    def get_event_by_name(self, event_name: str) -> dict:
        """
        Gets an event by its name. Parses the event.
        """
        event = self._get_event_by_name(event_name)
        event = self._parse_event(event)
        return event

    def get_similar_events_to_event(
        self, event_name: str, delta_year: int, near: bool = True, symmetric: bool = True
    ) -> tuple[dict, list[dict]]:
        """
        Gets similar events to the given event.

        Args:
            event_name (str): The name of the event
            delta_year (int): The delta rangeyear of the event
            near (bool): Whether to include near locations
            symmetric (bool): Whether the delta year is symmetric around the event.

        Returns:
            dict: The event
            list[dict]: A list of dictionaries with the similar events
        """

        event = self._get_event_by_name(event_name)

        start_year_event = self._extract_number(event, "Start Year")
        end_year_event = self._extract_number(event, "End Year")
        location_id_event = self._extract_relation(event, "Location")
        location_event = self.client.pages.retrieve(page_id=location_id_event)
        location_name_event = self._extract_name(location_event)

        if end_year_event is None:
            end_year_event = start_year_event

        if symmetric:
            start_year_search = start_year_event - delta_year
            end_year_search = end_year_event + delta_year
        else:
            start_year_search = start_year_event - delta_year
            end_year_search = end_year_event

        if event:
            event = self._parse_event(event)
            event_name = event["name"]

            events = self.get_similar_events_in_range(
                start_year=start_year_search,
                end_year=end_year_search,
                location=location_name_event,
                near=near,
                exclude_event=event_name,
            )
            return event, events
        else:
            return []

    def get_similar_events_in_range(
        self,
        start_year: int,
        end_year: int | None = None,
        location: str | None = None,
        near: bool = False,
        exclude_event: str | None = None,
    ):
        """
        Gets similar events to the given location.

        Args:
            start_year (int): The start year of the event
            end_year (int | None): The end year of the event
            location (str | None): The name of the location
            near (bool): Whether to include near locations
            exclude_event (str | None): The name of the event to exclude
        Returns:
            list[dict]: A list of dictionaries with the event details
        """
        location_id = None
        location_result = None  # To pass to _parse_event later
        near_location_ids = []  # Initialize for safety

        if location:
            # Query the Location database to find the main location by its name
            location_query_results = self.client.databases.query(
                **{
                    "database_id": LOCATION_DATABASE_ID,
                "filter": {
                        "property": "Name",  # Assuming "Name" is the title property
                        "title": {"equals": location},
                    },
                }
            ).get("results", [])

            if location_query_results:  # If the main location was found
                location_id = location_query_results[0]["id"]
                location_result = location_query_results[0]  # Save the full page object
                if near:
                    # If near=True, get IDs of locations related via the 'Near' property
                    near_location_ids = self._extract_multi_relation_ids(location_result, "Near")

        # --- Construct the filter for the main events query ---
        top_level_and_filters = []

        # 1. Add year-based filters
        top_level_and_filters.append({"property": "Start Year", "number": {"greater_than_or_equal_to": start_year}})
        if end_year is not None:
            top_level_and_filters.append({"property": "Start Year", "number": {"less_than_or_equal_to": end_year}})

        # Add exclusion filter if exclude_event is provided
        if exclude_event:
            top_level_and_filters.append(
                {
                    "property": "Name",  # Assuming "Name" is the title property of the event
                    "title": {"does_not_equal": exclude_event},
                }
            )

        # 2. Prepare location-based OR sub-filters
        location_or_sub_filters = []

        # Collect all unique location IDs that should be part of the OR condition
        unique_ids_for_location_or_clause = set()
        if location_id:
            unique_ids_for_location_or_clause.add(location_id)
        # near_location_ids is already a list of IDs (or empty)
        for nid in near_location_ids:
            unique_ids_for_location_or_clause.add(nid)

        for loc_id_for_or_filter in unique_ids_for_location_or_clause:
            location_or_sub_filters.append(
                {
                    "property": "Location",  # This is the 'Location' relation property in your Events database
                    "relation": {"contains": loc_id_for_or_filter},
                }
            )

        # 3. Add the combined location OR filter to the top-level AND filters
        if location_or_sub_filters:
            if len(location_or_sub_filters) == 1:
                # If there's only one location condition, no need for an 'or' wrapper
                top_level_and_filters.append(location_or_sub_filters[0])
            else:
                # If multiple location conditions, wrap them in an 'or'
                top_level_and_filters.append({"or": location_or_sub_filters})

        # 4. Construct the final query payload for the Events database
        final_events_query_payload = {"database_id": TIMELINE_DATABASE_ID}
        if top_level_and_filters:  # Should always be true if start_year is mandatory
            final_events_query_payload["filter"] = {"and": top_level_and_filters}

        raw_events: list[dict] = self.client.databases.query(**final_events_query_payload).get("results", [])

        # --- Parse results ---
        events = []
        for raw_event in raw_events:
            # location_result is the page object for the main 'location', or None
            # near_location_ids is the list of IDs for 'near' locations
            events.append(self._parse_event(raw_event))

        return events
    
    def _get_event_by_name(self, event_name: str) -> dict | None:
        """
        Gets an event by its name. Does not parse the event.

        Args:
            event_name (str): The name of the event

        Returns:
            dict: The event
        """
        event = self.client.databases.query(
            **{"database_id": TIMELINE_DATABASE_ID, "filter": {"property": "Name", "title": {"equals": event_name}}}
        )
        return event.get("results", [])[0] if event.get("results", []) else None

    def _parse_event(self, raw_event: dict) -> dict:
        """
        Parses a raw event and returns a dictionary with the event details.

        Args:
            raw_event (dict): The raw event data from Notion

        Returns:
            dict: A dictionary with the event details
        """

        # query the location database to get the location object
        location_id = self._extract_relation(raw_event, "Location")

        if location_id:
            location = self.client.pages.retrieve(page_id=location_id)
            location = self._parse_location(location)
        else:
            location = None

        polity_ids = self._extract_multi_relation_ids(raw_event, "Polity")
        if polity_ids:
            polities = []
            for polity_id in polity_ids:
                polity = self.client.pages.retrieve(page_id=polity_id)
                polity = self._parse_polity(polity)
                polities.append(polity)
        else:
            polities = None

        return {
            #            "id": raw_event['id'],
            "name": self._extract_name(raw_event),
            "start_year": self._extract_number(raw_event, "Start Year"),
            "end_year": self._extract_number(raw_event, "End Year"),
            "event_type": self._extract_select(raw_event, "Event Type"),
            "importance": self._extract_number(raw_event, "Importance"),
            "description": self._extract_rich_text(raw_event, "Description"),
            "excerpt": self._extract_rich_text(raw_event, "Excerpt"),
            "location": location,
            "polities": polities,
        }

    def _extract_relation(self, raw_event: dict, property_name: str) -> str:
        """
        Extracts the ID of the first related page from a relation property in raw_event.properties[property_name]
        and returns the ID.

        Args:
            raw_event (dict): The raw event data from Notion
            property_name (str): The name of the relation property to extract

        Returns:
            str: The ID of the first related page, or None if no relation is found
        """
        relation_property = raw_event.get("properties", {}).get(property_name)
        if relation_property and relation_property.get("type") == "relation":
            relations_list = relation_property.get("relation", [])
            if relations_list and isinstance(relations_list, list) and len(relations_list) > 0:
                return relations_list[0].get("id")
        return None

    def _extract_multi_relation_ids(self, raw_event: dict, property_name: str) -> list[str]:
        """
        Extracts the IDs of all related pages from a multi-relation property in raw_event.properties[property_name]
        and returns a list of IDs.

        Args:
            raw_event (dict): The raw event data from Notion
            property_name (str): The name of the multi-relation property to extract

        Returns:
            list[str]: A list of IDs of the related pages
        """
        relation_property = raw_event.get("properties", {}).get(property_name)
        if relation_property and relation_property.get("type") == "relation":
            relations_list = relation_property.get("relation", [])
            if relations_list and isinstance(relations_list, list) and len(relations_list) > 0:
                return [
                    relation["id"] for relation in relations_list if isinstance(relation, dict) and "id" in relation
                ]
        return []

    def _extract_multi_relation(self, raw_event: dict, property_name: str) -> list[dict]:
        """
        Extracts the names of all related pages from a multi-relation property in raw_event.properties[property_name]
        and returns a list of dictionaries with the page ID and name.

        Args:
            raw_event (dict): The raw event data from Notion
            property_name (str): The name of the multi-relation property to extract

        Returns:
            list[dict]: A list of dictionaries with the page ID and name of the related pages
        """

        relation_ids = self._extract_multi_relation_ids(raw_event, property_name)

        detailed_relations = []

        if not relation_ids:
            return []

        for r_id in relation_ids:
            try:
                entity = self.client.pages.retrieve(page_id=r_id)

                name = None
                # Ensure 'Name' property and 'title' array exist and are not empty
                if (
                    entity.get("properties")
                    and entity["properties"].get("Name")
                    and entity["properties"]["Name"].get("title")
                    and isinstance(entity["properties"]["Name"]["title"], list)
                    and len(entity["properties"]["Name"]["title"]) > 0
                    and entity["properties"]["Name"]["title"][0].get("plain_text")
                ):
                    name = entity["properties"]["Name"]["title"][0]["plain_text"]

                detailed_relations.append(name if name else "Unknown")
            except Exception as e:
                print(f"Error retrieving details for page ID {r_id}: {e}")
                detailed_relations.append("ErrorFetchingName")
        return detailed_relations

    def _extract_name(self, entity: dict) -> str:
        """
        Extracts the name of the entity from the 'Name' property.

        Args:
            entity (dict): The entity data from Notion

        Returns:
            str: The name of the entity, or None if no name is found
        """
        return entity["properties"]["Name"]["title"][0]["plain_text"] if entity["properties"]["Name"]["title"] else None
    
    def _extract_rich_text(self, raw_event: dict, property_name: str) -> str:
        """
        Extracts the rich text of the property from the raw_event.

        Args:
            raw_event (dict): The raw event data from Notion
            property_name (str): The name of the property to extract

        Returns:
        """
        return (
            raw_event["properties"][property_name]["rich_text"][0]["plain_text"]
            if raw_event["properties"][property_name]["rich_text"]
            else None
        )

    def _extract_number(self, raw_event: dict, property_name: str) -> float:
        """
        Extracts the number of the property from the raw_event.
        """
        return (
            raw_event["properties"][property_name]["number"]
            if raw_event["properties"][property_name]["number"]
            else None
        )

    def _extract_select(self, raw_event: dict, property_name: str) -> str:
        """
        Extracts the name of the select property from the raw_event.

        Args:
            raw_event (dict): The raw event data from Notion
            property_name (str): The name of the property to extract

        Returns:
        """
        return (
            raw_event["properties"][property_name]["select"]["name"]
            if raw_event["properties"][property_name]["select"]
            else None
        )

    def _parse_location(self, location_result: dict) -> dict:
        return {
            #            "id": location_result['id'],
            "name": self._extract_name(location_result),
            "biome": self._extract_select(location_result, "Biome"),
            "near": self._extract_multi_relation(location_result, "Near"),
        }

    def _parse_polity(self, polity_result: dict) -> dict:
        """
        Parses a polity and returns a dictionary with the polity details.
        Minimalistic, only returns the name, type, start year, and end year.
        Does not return the location, langauge family, religion, etc
        as these are relations and are not needed for the event.

        Args:
            polity_result (dict): The polity data from Notion

        Returns:
            dict: A dictionary with the polity details
        """
        return {
            "name": self._extract_name(polity_result),
            "type": self._extract_select(polity_result, "Type"),
            "start_year": self._extract_number(polity_result, "Start Year"),
            "end_year": self._extract_number(polity_result, "End Year"),
        }
