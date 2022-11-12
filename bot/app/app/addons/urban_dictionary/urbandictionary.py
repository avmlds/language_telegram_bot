from typing import List

import requests

import app.addons.urban_dictionary

from app.addons.urban_dictionary.errors import *
from app.addons.urban_dictionary.word import Word


class UrbanDictionary:
    """A client which fetches word info from the UrbanDictionary API.

    Attributes:
        API_URL (str): The base URL for all search requests.
        RANDOM_URL (str): The base URL for random word requests.

    Args:
        loop (:class:`o.AbstractEventLoop`, optional): The event loop in which the client runs.
            If one isn't provided, a loop is created.
        session (:class:`aiohttp.ClientSession`, optional): The session which makes all calls to the API.
            If one isn't provided, a session is created.
    """

    API_URL = "http://api.urbandictionary.com/v0/define"
    RANDOM_URL = "http://api.urbandictionary.com/v0/random"

    def __init__(self, session: requests.Session = None):
        self._autoclose_session = False

        if session is None:
            self.session = requests.Session()
            self._autoclose_session = True
        else:
            self.session = session

    def _get(self, term: str = None, random: bool = False) -> dict:
        """Helper method to reduce some boilerplate with :module:`aiohttp`.

        Args:
            term: The term to search for. Optional if doing a random search.
            random: Whether the search should return a random word.

        Returns:
            The JSON response from the API.

        Raises:
            UrbanConnectionError: If the response status isn't ``200``.
            WordNotFoundError: If the response doesn't contain data (i.e. no word found).
        """
        params = None
        if random:
            url = self.RANDOM_URL
        else:
            params = {"term": term}
            url = self.API_URL

        with self.session.get(url, params=params) as response:
            if response.status_code == 200:
                response = response.json()
            else:
                raise UrbanConnectionError(response.status_code)

        if not response["list"]:
            raise WordNotFoundError(term)

        return response

    def get_word(self, term: str) -> "app.addons.urban_dictionary.word.Word":
        """Gets the first matching word available.

        Args:
            term: The word to be defined.

        Returns:
            The closest matching :class:`Word` from UrbanDictionary.

        Raises:
            UrbanConnectionError: If the response status isn't ``200``.
            WordNotFoundError: If the response doesn't contain data (i.e. no word found).
        """
        resp = self._get(term=term)
        return Word(resp["list"][0])

    def search(self, term: str, limit: int = 3) -> "List[Word]":
        """Performs a search for a term and returns a list of possible matching :class:`Word`
        objects.

        Args:
            term: The term to be defined.

            limit (optional): Max amount of results returned.
                Defaults to 3.

        Note:
            The API will relay a fixed number of words and definitions, so ``limit`` can be
            arbitrarily high if needed or wanted.

        Returns:
            A list of :class:`Word` objects of up to the specified length.

        Raises:
            UrbanConnectionError: If the response status isn't ``200``.
            WordNotFoundError: If the response doesn't contain data (i.e. no word found).
        """
        resp = self._get(term=term)
        words = resp["list"]
        return [Word(x) for x in words[:limit]]

    def get_random(self) -> Word:
        """Gets a random word.

        Returns:
            A random :class:`Word`\.

        Raises:
            UrbanConnectionError: If the response status isn't ``200``.
        """
        resp = self._get(random=True)
        return Word(resp["list"][0])

    def get_word_raw(self, term: str) -> dict:
        """Gets the raw json response for a word.

        Args:
            term: The word to be defined.

        Returns:
            The JSON response from the UrbanDictionary API for ``term``.

        Raises:
            UrbanConnectionError: If the response status isn't ``200``.
            WordNotFoundError: If the response doesn't contain data (i.e. no word found).
        """
        return self._get(term=term)["list"][0]

    def search_raw(self, term: str, limit: int = 3) -> List[dict]:
        """Performs a search for a term and returns the raw response.

        Args:
            term: The term to be defined.

            limit: The maximum amount of results you'd like.
                Defaults to 3.

        Returns:
            A list of :class:`dict`\s which contain word information.
        """
        return self._get(term=term)["list"][:limit]

    def get_random_raw(self) -> dict:
        """Gets a random word in raw json format.

        Returns:
            The json representation of a random word as a :class:`dict`.

        Raises:
            UrbanConnectionError: If the response status isn't ``200``.
        """
        res = self._get(random=True)
        return res["list"][0]

    def close(self) -> None:
        """Closes the :class:`UrbanDictionary` client."""
        if self._autoclose_session:
            self.session.close()
