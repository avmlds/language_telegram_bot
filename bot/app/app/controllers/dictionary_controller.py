import logging
from typing import List

from telebot.types import Message

from app.controllers import BaseController
from app.controllers.reward_controller import RewardController
from app.exceptions.dictionary import DictionaryNotFoundException
from app.models import UsersDictionaries, Dictionary, DictionaryContent


logger = logging.getLogger(__name__)


class DictionaryController(BaseController):
    # TODO: Refactor me, merge with user_translations

    __base_model__ = UsersDictionaries
    __support_model__ = Dictionary
    __sub_model__ = DictionaryContent

    def create_dictionary(self, title, description="", is_paid=True, price=0):
        return self.create_by_support_model(
            title=title, description=description, is_paid=is_paid, price=price
        )

    def all_dictionaries(self, offset=0, limit=100):
        return self.all_by_support_model(offset=offset, limit=limit)

    def all_dictionary_users(self, offset=0, limit=100):
        return self.all(offset, limit)

    def connect_dictionary(self, dictionary_name: str, user_id: int):
        dictionary = (
            self._connection.query(self.__support_model__)
            .filter(self.__support_model__.title == dictionary_name)
            .first()
        )

        if not dictionary:
            raise DictionaryNotFoundException(dictionary_name)
        return self.create(user_id=user_id, dictionary_id=dictionary.id)

    def disconnect_dictionary(self, dictionary_name, user_id):
        dictionary = (
            self._connection.query(self.__support_model__)
            .filter(self.__support_model__.title == dictionary_name)
            .first()
        )

        if not dictionary:
            raise DictionaryNotFoundException(dictionary_name)

        users_dictionaries = (
            self._connection.query(self.__base_model__)
            .filter(
                self.__base_model__.user_id == user_id,
                self.__base_model__.dictionary_id == dictionary.id,
            )
            .first()
        )

        if not users_dictionaries:
            raise DictionaryNotFoundException(dictionary_name)

        return self.remove(id_=users_dictionaries.id)

    def delete_dictionary_user(self, dictionary_user):
        if isinstance(dictionary_user, self.__base_model__):
            if dictionary_user is not None:
                self.remove_by_support_model(dictionary_user.id)
        else:
            print(dictionary_user)
            raise Exception("Provided model is not an instance of UsersDictionaries!")

    def delete_dictionary(self, id_):
        self.remove_by_support_model(id_=id_)

    def insert_dictionary_content(
        self,
        dictionary_id,
        word,
        translation,
        word_meaning=None,
        translation_meaning=None,
    ):
        self.create_by_sub_model(
            dictionary_id=dictionary_id,
            word=word,
            translation=translation,
            word_meaning=word_meaning,
            translation_meaning=translation_meaning,
        )

    def get_user_dictionaries(self, user_id: int):
        return (
            self._connection.query(self.__base_model__)
            .filter(self.__base_model__.user_id == user_id)
            .all()
        )

    def get_user_dictionaries_ids(self, user_id: int) -> List[int]:
        return [
            dictionary.dictionary_id
            for dictionary in self.get_user_dictionaries(user_id)
        ]

    def get_dictionary_translations(self, *, user_id: int, word: str):
        # FIXME: These are not translations, these are rows from the database
        word = self.prepare_string(word)
        dictionaries_ids = self.get_user_dictionaries_ids(user_id)

        if not dictionaries_ids:
            return []

        return (
            self._connection.query(self.__sub_model__)
            .filter(
                self.__sub_model__.dictionary_id.in_(dictionaries_ids),
                self.__sub_model__.word == word,
            )
            .all()
        )

    def modify_reward(self, user_id, word, reward_type):
        word_rows = self.get_dictionary_translations(user_id=user_id, word=word)
        translation_rows = self.get_dictionary_words(user_id=user_id, translation=word)
        RewardController.modify_knowledge(word_rows, reward_type)
        RewardController.modify_knowledge(translation_rows, reward_type)
        self._connection.commit()

    def get_dictionary_words(self, *, user_id: int, translation: str):
        translation = self.prepare_string(translation)

        dictionaries_ids = self.get_user_dictionaries_ids(user_id)

        if not dictionaries_ids:
            return []

        return (
            self._connection.query(self.__sub_model__)
            .filter(
                self.__sub_model__.dictionary_id.in_(dictionaries_ids),
                self.__sub_model__.translation == translation,
            )
            .all()
        )

    def get_correct_dictionary_translation_list(self, message: Message, word: str):
        word_translations = self.get_dictionary_translations(
            user_id=message.chat.id, word=word
        )
        translation_words = self.get_dictionary_words(
            user_id=message.chat.id, translation=word
        )

        if word_translations:
            return [translation.translation for translation in word_translations]

        return [word.word for word in translation_words]
