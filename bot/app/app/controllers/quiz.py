import logging
import math
import random

from telebot.types import Message

from app.constants import states
from app.controllers.reward_controller import RewardController
from app.exceptions.database import DbEmptyException
from app.templates import TRANSLATION_QUIZ_STARTED, TRANSLATION_CORRECT

logger = logging.getLogger(__name__)


class QuizController:
    def __init__(self, user_controller, translation_controller, dictionary_controller):
        self.user_controller = user_controller
        self.translation_controller = translation_controller
        self.dictionary_controller = dictionary_controller

    def _pend_or_reward(self, user_id, word, dictionary, reward_type):
        controller = self.translation_controller
        if dictionary:
            controller = self.dictionary_controller
        controller.modify_reward(
            user_id=user_id,
            word=word,
            reward_type=reward_type,
        )

    def pend_for_hint(self, user_id, word, dictionary=False):
        self._pend_or_reward(user_id, word, dictionary, RewardController.HINT_PEND)

    def pend_for_translation(self, user_id, word, dictionary=False):
        self._pend_or_reward(user_id, word, dictionary, RewardController.TRANSLATION_PEND)

    def pend_for_incorrect_answer(self, user_id, word, dictionary=False):
        self._pend_or_reward(user_id, word, dictionary, RewardController.ANSWER_PEND)

    def reward_for_correct_answer(self, user_id, word, dictionary=False):
        self._pend_or_reward(user_id, word, dictionary, RewardController.ANSWER_REWARD)

    def pend_or_reward_at_quiz(self, user_id, word, correctness, dictionary=False):
        if correctness == TRANSLATION_CORRECT:
            return self.reward_for_correct_answer(user_id, word, dictionary=dictionary)
        return self.pend_for_incorrect_answer(user_id, word, dictionary=dictionary)

    def get_word_pairs(self, user_id):
        return self.translation_controller.get_ordered_word_pair(user_id=user_id)

    def quiz(self, message: Message):

        logger.info("State updated to QUIZ_STATE for user %s", message.chat.id)

        self.user_controller.update_user_state(
            user_state=states.QUIZ_STATE, message=message
        )

        pairs = self.get_word_pairs(user_id=message.chat.id)
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
