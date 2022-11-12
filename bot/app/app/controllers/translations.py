import logging
from typing import Tuple, Optional, List

from telebot.types import Message

from app.exceptions.database import WordTooLong, TranslationTooLong
from app.sql_queries import SELECT_RANDOM_WORD_PAIR

from app.controllers.base import BaseController
from app.models.translations import UserTranslation


logger = logging.getLogger(__name__)


class TranslationController(BaseController):
    __base_model__ = UserTranslation

    def get_correct_translation_list(self, message: Message, word: str):
        word_translations = self.get_translations(user_id=message.chat.id, word=word)
        translation_words = self.get_words(user_id=message.chat.id, translation=word)

        if word_translations:
            return [
                translation.translation_representation
                for translation in word_translations
            ]

        return [word.word_representation for word in translation_words]

    def get_correct_translations(
        self,
        message: Message,
        word: str,
        additional_translations: Optional[List[str]] = None,
    ):
        correct_translations = self.get_correct_translation_list(message, word)

        if additional_translations:
            correct_translations.extend(additional_translations)

        return ", ".join(set(correct_translations))

    def get_translation(self, *, user_id: int, word: str, translation: str):
        word = self.prepare_string(word)

        return (
            self._connection.query(self.__base_model__)
            .filter(
                self.__base_model__.user_id == user_id,
                self.__base_model__.word == word,
                self.__base_model__.translation == translation,
            )
            .first()
        )

    def get_translations(self, *, user_id: int, word: str):
        word = self.prepare_string(word)

        return (
            self._connection.query(self.__base_model__)
            .filter(
                self.__base_model__.user_id == user_id, self.__base_model__.word == word
            )
            .all()
        )

    def get_words(self, *, user_id: int, translation: str):
        translation = self.prepare_string(translation)

        return (
            self._connection.query(self.__base_model__)
            .filter(
                self.__base_model__.user_id == user_id,
                self.__base_model__.translation == translation,
            )
            .all()
        )

    def insert_translation(self, *, user_id: int, word, translation):
        casefold_word = self.prepare_string(word)
        casefold_translation = self.prepare_string(translation)
        if len(casefold_word) > 300:
            raise WordTooLong(word)
        if len(translation) > 300:
            raise TranslationTooLong(translation)
        return self.create(
            user_id=user_id,
            word_representation=word,
            word=casefold_word,
            translation_representation=translation,
            translation=casefold_translation,
        )

    def check_translation(self, *, user_id: int, word: str, translation: str) -> bool:

        word = self.prepare_string(word)
        translation = self.prepare_string(translation)

        var_1 = self.get_translations(user_id=user_id, word=word)
        var_1 = any(filter(lambda x: x.translation == translation, var_1))

        var_2 = self.get_translations(user_id=user_id, word=translation)
        var_2 = any(filter(lambda x: x.translation == word, var_2))

        return var_1 or var_2

    def delete_translation(self, *, translation: str, user_id: int, word: str):

        word = self.prepare_string(word)
        translation = self.prepare_string(translation)

        translation_model = self.get_translation(
            user_id=user_id, word=word, translation=translation
        )
        if not translation_model:
            return False

        self.remove(id_=translation_model.id)
        return True

    def get_random_pair(
        self, user_id: int
    ) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
        cursor = self._connection.execute(SELECT_RANDOM_WORD_PAIR, {"user_id": user_id})
        row = cursor.first()

        if not row:
            return None, None, None, None
        return row
