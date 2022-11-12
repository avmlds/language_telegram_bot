from typing import List, Optional

from pydantic import BaseModel, Field


class License(BaseModel):
    name: str
    url: str

    class Config:
        orm_mode = True


class Phonetics(BaseModel):
    text: Optional[str] = "No text available"
    audio: Optional[str] = None
    source_url: str = Field(None, alias="sourceUrl")
    license: Optional[License] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    @property
    def extract_audio(self):
        if self.audio:
            name = self.audio.rsplit("/", maxsplit=1)[-1]
            name = name.rsplit(".", maxsplit=1)[0]
            name = name.split("-")[-1].upper()
            return f"[{name}]({self.audio})"
        return "Audio is not available"


class WordDefinition(BaseModel):
    definition: Optional[str]
    example: Optional[str] = None
    synonyms: Optional[List[str]] = []
    antonyms: Optional[List[str]] = []

    class Config:
        orm_mode = True


class Meaning(BaseModel):
    part_of_speech: str = Field(alias="partOfSpeech")
    definitions: List[WordDefinition]
    synonyms: Optional[List[str]] = []
    antonyms: Optional[List[str]] = []

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        allow_population_by_field_name = True


class EnglishDefinition(BaseModel):
    word: str
    phonetic: Optional[str]
    phonetics: Optional[List[Phonetics]] = None
    origin: Optional[str]
    meanings: Optional[List[Meaning]] = []
    license: Optional[License] = None
    source_url: Optional[List[str]] = Field(None, alias="sourceUrl")

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        allow_population_by_field_name = True


class DefinitionWithError(BaseModel):
    """
    {
        "title":"No Definitions Found",
        "message":"Sorry pal, we couldn't find definitions for the word you were looking for.",
        "resolution":"You can try the search again at later time or head to the web instead."
    }"""

    title: str
    message: str
    resolution: str
