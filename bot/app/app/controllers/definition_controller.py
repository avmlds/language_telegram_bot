import logging
from typing import Union, Optional, List

from app.addons.definitions.english import DefinitionAddon
from app.addons.definitions.english_model import EnglishDefinition
from app.addons.definitions.errors import DefinitionException
from app.controllers import BaseController
from app.models import Definition


logger = logging.getLogger(__name__)


class DefinitionController(BaseController):
    __base_model__ = Definition

    def insert(self, definition: EnglishDefinition, user_id: int):
        json_definition = definition.dict(by_alias=False)
        return self.create(
            word=definition.word,
            phonetic=definition.phonetic,
            phonetics=json_definition["phonetics"],
            origin=definition.origin,
            meanings=json_definition["meanings"],
            license=json_definition["license"],
            source_url=definition.source_url,
            requested_by=user_id,
            # created_at=datetime.datetime.now(), - already inserted by postgres
        )

    def one_by_word(self, word: str):
        return (
            self._connection.query(self.__base_model__)
            .filter(self.__base_model__.word == word)
            .first()
        )

    def get_definition(self, word: str, user_id: int) -> Union[EnglishDefinition, str]:
        definition = self.one_by_word(word)
        if definition:
            return self.definition_to_model(definition)

        api_definition = DefinitionAddon()
        try:
            # TODO: Think about the len of the definition
            definition_from_api = api_definition.get_definition_from_api(word)[0]
            definition = self.insert(definition_from_api, user_id)
        except DefinitionException as e:
            logger.error(e)
            definition = None

        return self.definition_to_model(definition)

    @staticmethod
    def definition_to_model(definition_object: Definition):
        if not definition_object:
            return None
        return EnglishDefinition.from_orm(definition_object)

    def extract_meanings(
        self, definition_object: Optional[EnglishDefinition]
    ) -> List[str]:
        if not definition_object or len(definition_object.meanings) == 0:
            return ["No valid meanings found"]

        meanings = definition_object.meanings

        phonetics = []
        for phonetic in definition_object.phonetics:
            phonetics.append(
                f"    Phonetic: {phonetic.text}\n"
                f"    Audio: {phonetic.extract_audio}\n"
            )
        phonetics = "\n".join(phonetics)

        results = [
            f"*Word:* {definition_object.word}\n" f"*Phonetics:*\n\n" f"{phonetics}"
        ]

        for meaning in meanings:
            result_object = (
                f"*Meaning:*\n*Part of speech:* {meaning.part_of_speech}\n\n"
            )

            if len(meaning.definitions) != 0:
                result_object = (
                    f"{result_object}"
                    f"*Definition:* {meaning.definitions[0].definition}\n"
                    f"*Example:* {meaning.definitions[0].example}\n"
                )
            results.append(result_object)

        return self.split("\n".join(results))

    @staticmethod
    def split(definition_string: str) -> List[str]:
        if len(definition_string) <= 4095:
            return [definition_string]
        messages = []
        chinks = definition_string.split("*Meaning:*\n")
        for chunk in chinks:
            messages.append(f"*Meaning:*\n{chunk}")
        return messages
