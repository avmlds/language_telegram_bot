import logging
import math
import random

from telebot.types import Message

from app.constants import states
from app.exceptions.database import DbEmptyException
from app.templates import TRANSLATION_QUIZ_STARTED


logger = logging.getLogger(__name__)


class QuizController:
    def __init__(self, user_controller, translation_controller):
        self.user_controller = user_controller
        self.translation_controller = translation_controller

    def quiz(self, message: Message):

        logger.info("State updated to QUIZ_STATE for user %s", message.chat.id)

        self.user_controller.update_user_state(
            user_state=states.QUIZ_STATE, message=message
        )

        pairs = self.translation_controller.get_random_pair(user_id=message.chat.id)
        (
            word,
            word_representation,
            word_translation,
            word_translation_representation,
        ) = pairs
        if not word:
            self.user_controller.update_user_state(
                user_state=states.STATE_IDLE, message=message
            )
            raise DbEmptyException

        quiz_word = random.choice(
            (word_representation, word_translation_representation)
        )

        translation = word_representation
        if quiz_word == translation:
            translation = word_translation_representation

        logger.info(
            "User %s state data updated to %s, metadata updated to %s",
            message.chat.id,
            quiz_word,
            translation,
        )

        self.user_controller.update_user_state_data(
            data=quiz_word, meta=translation, message=message
        )
        return TRANSLATION_QUIZ_STARTED.format(quiz_word)

    @staticmethod
    def get_hint_string(translation: str):
        str_len = len(translation)
        hint_len = math.ceil(str_len / 4)
        return f"{translation[:hint_len]}" + " %" * (str_len - hint_len)
