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

class Polity(BaseModel):
    name: str = Field(..., description="The name of the polity")
    type: str = Field(..., description="The type of the polity")
    start_year: int = Field(..., description="The start year of the polity")
    end_year: int = Field(..., description="The end year of the polity")


class Location(BaseModel):
    name: str = Field(..., description="The name of the location.")
    biome: BiomeEnum = Field(..., description="The biome of the location.")
    near: list[str] = Field(..., description="The near locations of the location - these are names of locations that are near the location.")


class Event(BaseModel):
    name: str = Field(..., description="The name of the event. Should be unique")
    start_year: int = Field(..., description="The start year of the event.")
    end_year: int = Field(..., description="The end year of the event.")
    importance: int = Field(..., description="The importance of the event - a number between 0 and 10, with 10 being an era-changing event, 8 being a major global event, 6 being a national event, 4 being a minor event, etc")
    description: str = Field(..., description="A detailed description of the event.")
    excerpt: str = Field(..., description="A short excerpt of the event.")
    location: Location = Field(..., description="The location of the event.")
    polities: list[Polity] = Field(..., description="The polities associated with the event")




