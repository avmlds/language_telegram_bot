from app.addons.urban_dictionary import Word, UrbanDictionary
from app.addons.urban_dictionary.errors import WordNotFoundError, UrbanConnectionError

from app.controllers.base import BaseController
from app.models.urban_dictionary import UrbanDictionaryModel


class UrbanDictionaryController(BaseController):
    __base_model__ = UrbanDictionaryModel

    def get_word(self, word: str):
        word = self.prepare_string(word)
        return (
            self._connection.query(self.__base_model__)
            .filter(self.__base_model__.word == word)
            .first()
        )

    def search(self, term: str, user_id: int):
        try:
            urban = UrbanDictionary()
            words = urban.search(term=term, limit=3)
            reply_messages = []
            for word in words:
                self.insert(word, user_id)
                reply_messages.append(word.message)

            reply_message = "\n\n".join(reply_messages)

        except (WordNotFoundError, UrbanConnectionError) as e:
            reply_message = e.message
        return reply_message

    def insert(self, word: Word, user_id: int):
        return self.create(
            defid=word.defid,
            word=self.prepare_string(word.word),
            author=word.author,
            permalink=word.permalink,
            definition=word.definition,
            example=word.example,
            votes=word.votes,
            current_vote=word.current_vote,
            requested_by=user_id,
        )

    def get_random(self, user_id: int):
        try:
            # TODO: Merge UrbanDictionary addon into UrbanDictionaryController
            urban = UrbanDictionary()
            word = urban.get_random()
            self.insert(word, user_id)
            reply_message = word.message

        except (WordNotFoundError, UrbanConnectionError) as e:
            reply_message = e.message
        return reply_message
