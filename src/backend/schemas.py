from pydantic import BaseModel, Field
from enum import Enum

class BiomeEnum(str, Enum):
    COLD_DESERT = "Cold Desert"
    HOT_DESERT = "Hot Desert"
    COLD_STEPPE = "Cold Steppe"
    HOT_STEPPE = "Hot Steppe"
    MARITIME = "Maritime"
    MEDITERRAEAN = "Mediterranean"
    TEMPERATE_MONSOON = "Temperate Monsoon"
    TROPICAL_RAINFOREST = "Tropical Rainforest"
    SAVANNA = "Savanna"
    CONTINENTAL = "Continental"
    TAIGA = "Taiga"
    TUNDRA = "Tundra"

class EventTypeEnum(str, Enum):
    TECHNOLOGICAL_ADVANCEMENT = "Technological advancement"
    POLITICAL_EVENT = "Political event"
    POPULATION_MIGRATION = "Population migration"
    MILITARY_ACTION = "Military action"
    CONSTRUCTION = "Construction"
    COLONIZATION = "Colonization"
    ECONOMIC_EVENT = "Economic event"
    CIVIL_ACTION = "Civil action"
    PERSONAL_EVENT = "Personal event"
    RELIGIOUS_EVENT = "Religious event"

class Polity(BaseModel):
    name: str = Field(..., description="Unique name of the polity.")
    type: str = Field(..., description="Political structure or classification (e.g., Empire, Kingdom, Tribal Confederation) within the world.")
    start_year: int = Field(..., description="Founding year or year of emergence of this polity in the timeline.")
    end_year: int = Field(..., description="Year of this polity's dissolution, conquest, or significant transformation in the timeline.")


class Location(BaseModel):
    name: str = Field(..., description="Unique name of the geographical location.")
    biome: BiomeEnum = Field(..., description="The predominant biome of this location, influencing its climate, ecology, and cultures.")
    near: list[str] = Field(..., description="List of names of other locations geographically close or adjacent to this one, used for regional context.")


class Event(BaseModel):
    name: str = Field(..., description="A concise and unique title for this historical event. Should be distinct from other event names.")
    start_year: int = Field(..., description="The year this event began or its primary phase started in the timeline.")
    end_year: int | None = Field(..., description="The year this event concluded or its immediate effects ceased. Use null if the event is punctual.")
    event_type: EventTypeEnum = Field(..., description="The primary classification of this event according to the historical frameworks (e.g., Political, Military).")
    importance: int = Field(..., description="Numerical rating (0-10) of the event's overall impact on the world: 10=era-defining, 8=major widespread, 6=significant regional/national, 4=notable local, 0-2=minor.")
    description: str = Field(..., description="A comprehensive narrative of the event. Detail its causes, key occurrences, involved factions or characters, and immediate to short-term outcomes. Aim for 2-3 well-developed paragraphs that capture the event's significance and unfold its story in the world.")
    excerpt: str = Field(..., description="A brief, engaging summary of the event (typically 1-2 sentences), suitable for quick overviews, timeline entries, or as an introductory hook.")
    location: Location = Field(..., description="The primary geographical `Location` object in the world where this event took place or was centered.")
    polities: list[Polity] = Field(..., description="A list of `Polity` objects representing political entities in the world directly involved in or significantly affected by this event.")
