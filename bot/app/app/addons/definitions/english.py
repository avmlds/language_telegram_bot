import logging
from typing import List

import requests

from app.addons.definitions.english_model import EnglishDefinition
from app.addons.definitions.errors import DefinitionException


logger = logging.getLogger(__name__)


class DefinitionAddon:

    API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/{}"

    def __init__(self, session: requests.Session = None):
        self._autoclose_session = False

        if session is None:
            self.session = requests.Session()
            self._autoclose_session = True
        else:
            self.session = session

    def get_definition_from_api(self, word: str) -> List[EnglishDefinition]:
        url = self.API_URL.format(word)
        with self.session.get(url) as response:
            if response.status_code == 200:
                json_data = response.json()
                response = [
                    EnglishDefinition.parse_obj(element) for element in json_data
                ]
            else:
                raise DefinitionException
        return response
