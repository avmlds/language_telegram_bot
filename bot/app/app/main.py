import os
import logging

import telebot
from telebot.types import BotCommand, Message, CallbackQuery


from app.controllers import (
    Keyboard,
    TranslationController,
    UrbanDictionaryController,
    UserController,
    QuizController,
)

import app.constants.states as states
from app.controllers.base import get_session
from app.controllers.definition_controller import DefinitionController
from app.controllers.dictionary_controller import DictionaryController
from app.exceptions.database import WordTooLong, TranslationTooLong, DbEmptyException
from app.exceptions.dictionary import DictionaryNotFoundException

from templates import (
    START_TEMPLATE,
    ADD_TRANSLATION_TEMPLATE,
    ADD_WORD_TEMPLATE,
    TRANSLATION_ADDED_TEMPLATE,
    TRANSLATION_CORRECT,
    TRANSLATION_INCORRECT,
    TRANSLATION_DELETE_TEMPLATE,
    TRANSLATION_DELETE_FAIL,
    TRANSLATION_DELETE_STEP_2,
    TRANSLATION_DELETED,
    TRANSLATION_HINT,
    TRANSLATION_FULL,
    TRANSLATION_NO_HINT,
    GET_DEFINITION,
    TRANSLATION_TOO_LONG,
    SEARCH_URBAN_DICTIONARY_TEMPLATE,
)

logger = logging.getLogger()

formatter = logging.Formatter('%(asctime)s -- %(filename)s -- line_%(lineno)d : "%(message)s"')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
logger.addHandler(handler)

TOKEN = os.environ.get("TELEGRAM_TOKEN")

bot = telebot.TeleBot(token=TOKEN, parse_mode="Markdown", num_threads=10)
bot.set_my_commands(
    [
        BotCommand("start", description="Start using bot."),
        BotCommand("help", description="Ask for help."),
    ]
)


@bot.message_handler(commands=["start", "help"], content_types=["text"])
@get_session
def handle_start(message, session):
    logger.info(
        "User %s pressed start or help, state updated to STATE_IDLE", message.chat.id
    )
    UserController(connection=session).update_user_state(states.STATE_IDLE, message)
    return bot.send_message(
        message.chat.id, START_TEMPLATE, reply_markup=Keyboard().default_keyboard
    )


@bot.callback_query_handler(lambda query: query.data == Keyboard.ADD)
@get_session
def add_new_word(query: CallbackQuery, session):
    message = query.message
    logger.info("User %s pressed add, state updated to ADD_WORD", message.chat.id)
    UserController(connection=session).update_user_state(
        user_state=states.ADD_WORD, message=message
    )
    return bot.send_message(message.chat.id, ADD_WORD_TEMPLATE)


@bot.callback_query_handler(lambda query: query.data == Keyboard.STOP_ADD)
@get_session
def add_new_word(query: CallbackQuery, session):
    message = query.message

    logger.info(
        "User %s pressed stop add, state updated to STATE_IDLE", message.chat.id
    )
    UserController(connection=session).update_user_state(
        user_state=states.STATE_IDLE, message=message
    )
    return bot.send_message(
        message.chat.id, START_TEMPLATE, reply_markup=Keyboard().default_keyboard
    )


@bot.callback_query_handler(lambda query: query.data == Keyboard.DELETE)
@get_session
def delete_translation(query: CallbackQuery, session):
    message = query.message

    logger.info(
        "User %s pressed delete, state updated to STATE_DELETE", message.chat.id
    )
    UserController(connection=session).update_user_state(
        user_state=states.DELETE_TRANSLATION_STATE, message=message
    )
    return bot.send_message(message.chat.id, TRANSLATION_DELETE_TEMPLATE)


@bot.callback_query_handler(
    lambda query: query.data in (Keyboard.START_QUIZ, Keyboard.NEXT_QUIZ)
)
@get_session
def start_quiz(query: CallbackQuery, session):
    message = query.message
    chat_id = message.chat.id

    logger.info("User %s pressed START_QUIZ or NEXT_QUIZ", message.chat.id)
    try:
        quiz = QuizController(
            user_controller=UserController(connection=session),
            translation_controller=TranslationController(connection=session),
            dictionary_controller=DictionaryController(connection=session),
        )
        quiz_message = quiz.quiz(message)
    except DbEmptyException as e:
        logger.info("No words for user %s", message.chat.id)
        return bot.send_message(
            chat_id=chat_id,
            text=str(e),
            reply_markup=Keyboard().default_keyboard,
        )
    else:
        return bot.edit_message_text(
            chat_id=chat_id,
            message_id=message.id,
            text=quiz_message,
            reply_markup=Keyboard().quiz_keyboard_with_hint,
        )


@bot.callback_query_handler(lambda query: query.data == Keyboard.STOP_QUIZ)
@get_session
def stop_quiz(query: CallbackQuery, session):
    message = query.message

    logger.info("User %s pressed STOP_QUIZ", message.chat.id)

    UserController(connection=session).update_user_state(states.STATE_IDLE, message)

    return bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.id,
        text=START_TEMPLATE,
        reply_markup=Keyboard().default_keyboard,
    )


@bot.callback_query_handler(lambda query: query.data == Keyboard.URBAN_RANDOM)
@get_session
def get_random_from_urban_dictionary(query: CallbackQuery, session):
    message = query.message

    logger.info("User %s pressed URBAN_RANDOM", message.chat.id)

    UserController(connection=session).update_user_state(
        user_state=states.STATE_IDLE, message=message
    )
    word = UrbanDictionaryController(connection=session).get_random(message.chat.id)

    return bot.send_message(
        chat_id=query.message.chat.id,
        text=word,
        reply_markup=Keyboard().default_keyboard,
    )


@bot.callback_query_handler(lambda query: query.data == Keyboard.URBAN_SEARCH)
@get_session
def get_random_from_urban_dictionary(query: CallbackQuery, session):
    message = query.message

    logger.info("User %s pressed URBAN_SEARCH", message.chat.id)

    user_controller = UserController(connection=session)
    user_controller.update_user_state(
        user_state=states.SEARCH_URBAN_DICTIONARY_STATE, message=message
    )
    logger.info(
        "User %s state updated to SEARCH_URBAN_DICTIONARY_STATE", message.chat.id
    )
    return bot.send_message(
        chat_id=message.chat.id, text=SEARCH_URBAN_DICTIONARY_TEMPLATE
    )


@bot.callback_query_handler(lambda query: query.data == Keyboard.HINT)
@get_session
def get_quiz_hint(query: CallbackQuery, session):
    message = query.message

    user_controller = UserController(connection=session)
    dictionary_controller = DictionaryController(connection=session)
    translation_controller = TranslationController(connection=session)

    logger.info("User %s pressed HINT", message.chat.id)

    quiz_controller = QuizController(
        user_controller=user_controller,
        translation_controller=translation_controller,
        dictionary_controller=dictionary_controller,
    )

    user_state_data = user_controller.get_user_state_data(message)
    word = user_state_data["data"]

    list_translations = translation_controller.get_correct_translation_list(
        message, word
    )
    dictionary_translations = (
        dictionary_controller.get_correct_dictionary_translation_list(message, word)
    )

    if list_translations:
        hint_string = quiz_controller.get_hint_string(list_translations[0])
        quiz_controller.pend_for_hint(user_id=message.chat.id, word=word)
    elif dictionary_translations:
        hint_string = quiz_controller.get_hint_string(dictionary_translations[0])
        quiz_controller.pend_for_hint(user_id=message.chat.id, word=word, dictionary=True)
    else:
        logger.info("User %s no hint available for a word %s", message.chat.id, word)

        hint_string = TRANSLATION_NO_HINT

    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.id,
        text=TRANSLATION_HINT.format(word, hint_string),
        reply_markup=Keyboard().quiz_keyboard_with_full_translation,
    )


@bot.callback_query_handler(lambda query: query.data == Keyboard.GIVE_TRANSLATION)
@get_session
def get_quiz_full_translation(query: CallbackQuery, session):
    message = query.message

    user_controller = UserController(connection=session)
    dictionary_controller = DictionaryController(connection=session)
    translation_controller = TranslationController(connection=session)

    quiz_controller = QuizController(
        user_controller, translation_controller, dictionary_controller
    )

    user_state_data = user_controller.get_user_state_data(message)
    # TODO: refactor usage to property instead of direct access to data
    word = user_state_data["data"]

    logger.info("User %s pressed GIVE_TRANSLATION for a word %s", message.chat.id, word)

    dictionary_translations = (
        dictionary_controller.get_correct_dictionary_translation_list(message, word)
    )
    string_translations = translation_controller.get_correct_translations(
        message, word, dictionary_translations
    )
    quiz_controller.pend_for_translation(user_id=message.chat.id, word=word)
    quiz_controller.pend_for_translation(user_id=message.chat.id, word=word, dictionary=True)

    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.id,
        # TODO: move to controller?
        text=TRANSLATION_FULL.format(word, string_translations),
        reply_markup=Keyboard().quiz_keyboard,
    )


@bot.callback_query_handler(lambda query: query.data == Keyboard.GET_DEFINITION)
@get_session
def get_definition(query: CallbackQuery, session):
    message = query.message

    logger.info(
        "User %s pressed GIVE_DEFINITION, setting state to GET_DEFINITION_STATE",
        message.chat.id,
    )

    UserController(connection=session).update_user_state(
        user_state=states.GET_DEFINITION_STATE, message=message
    )
    # TODO: Add "go back" button
    bot.send_message(chat_id=message.chat.id, text=GET_DEFINITION)


@bot.callback_query_handler(
    lambda query: query.data
    in (Keyboard.CONNECT_DICTIONARY, Keyboard.DISCONNECT_DICTIONARY)
)
@get_session
def operate_dictionaries(query: CallbackQuery, session):
    message = query.message

    logger.info(
        "User %s pressed DISCONNECT_DICTIONARY, setting state to %s_STATE",
        message.chat.id,
        query.data,
    )

    # TODO: Refactor usage of constants
    UserController(connection=session).update_user_state(
        user_state=f"{query.data}_STATE", message=message
    )
    return bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.id,
        text="*Choose dictionary:*",
        reply_markup=Keyboard().dictionaries_keyboard,
    )


@bot.callback_query_handler(lambda query: query.data == Keyboard.EN_RU_DICTIONARY_3K)
@get_session
def connect_dictionary(query: CallbackQuery, session):
    message = query.message

    # TODO: Think how to use factory methods for dictionaries

    dictionary_controller = DictionaryController(connection=session)

    action = UserController(connection=session).get_user_state(message=message)

    if action == states.CONNECT_DICTIONARY_STATE:
        logger.info(
            "User %s pressed EN_RU_DICTIONARY_3K, action CONNECT_DICTIONARY_STATE",
            message.chat.id,
        )
        func = dictionary_controller.connect_dictionary
        # TODO: Move to templates
        message_text = f"*Dictionary connected successfully!*\n{START_TEMPLATE}"
    else:
        logger.info(
            "User %s pressed EN_RU_DICTIONARY_3K, action DISCONNECT_DICTIONARY_STATE",
            message.chat.id,
        )
        func = dictionary_controller.disconnect_dictionary
        # TODO: Move to templates
        message_text = f"*Dictionary disconnected successfully!*\n{START_TEMPLATE}"
    try:
        func(Keyboard.EN_RU_DICTIONARY_3K, user_id=message.chat.id)
    except DictionaryNotFoundException as e:
        message_text = e

    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.id,
        text=message_text,
        reply_markup=Keyboard().default_keyboard,
    )


@bot.message_handler()
@get_session
def operate_messages(message: Message, session):
    user_id = chat_id = message.chat.id

    user_controller = UserController(connection=session)
    dictionary_controller = DictionaryController(connection=session)
    translation_controller = TranslationController(connection=session)
    quiz_controller = QuizController(user_controller, translation_controller, dictionary_controller)
    user_state = user_controller.get_user_state(message)

    if user_state is None:

        logger.info("User %s sent message without state, new user", message.chat.id)

        return bot.send_message(
            chat_id, START_TEMPLATE, reply_markup=Keyboard().default_keyboard
        )

    elif user_state == states.STATE_IDLE:

        logger.info("User %s sent message in STATE_IDLE", message.chat.id)

        return bot.send_message(
            chat_id, START_TEMPLATE, reply_markup=Keyboard().default_keyboard
        )

    elif user_state == states.ADD_WORD:
        logger.info("User %s sent message in ADD_WORD", message.chat.id)

        user_controller.update_user_state_data(message=message, data=message.text)
        user_controller.update_user_state(states.ADD_TRANSLATION, message=message)
        return bot.send_message(chat_id, ADD_TRANSLATION_TEMPLATE)

    elif user_state == states.ADD_TRANSLATION:
        logger.info("User %s sent message in ADD_TRANSLATION", message.chat.id)

        word = user_controller.get_user_state_data(message)["data"]
        response_message = TRANSLATION_ADDED_TEMPLATE

        try:
            translation_controller.insert_translation(
                user_id=user_id, word=word, translation=message.text
            )
        except (WordTooLong, TranslationTooLong) as e:
            logger.info(
                "User %s sent message in ADD_TRANSLATION, message is too long",
                message.chat.id,
            )
            response_message = TRANSLATION_TOO_LONG.format(e)

        user_controller.update_user_state(states.ADD_WORD, message=message)
        return bot.send_message(
            chat_id, response_message, reply_markup=Keyboard().add_word_keyboard
        )

    elif user_state == states.QUIZ_STATE:
        logger.info("User %s sent message in QUIZ_STATE", message.chat.id)

        user_state_data = user_controller.get_user_state_data(message)
        word = user_state_data["data"]

        dictionary_translations = dictionary_controller.get_correct_dictionary_translation_list(
            message, word
        )

        correctness = TRANSLATION_INCORRECT
        if translation_controller.check_translation(
            user_id=user_id, word=word, translation=message.text
        ):
            correctness = TRANSLATION_CORRECT
        elif translation_controller.prepare_string(message.text) in dictionary_translations:
            correctness = TRANSLATION_CORRECT

        word_translations = translation_controller.get_correct_translations(
            message, word, dictionary_translations
        )
        # FIXME: That's a mess
        quiz_controller.pend_or_reward_at_quiz(user_id=user_id, word=word, correctness=correctness)
        quiz_controller.pend_or_reward_at_quiz(user_id=user_id, word=word, correctness=correctness, dictionary=True)
        try:
            next_quiz = quiz_controller.quiz(message)
        except DbEmptyException as e:
            return bot.send_message(
                chat_id=chat_id,
                text=str(e),
                reply_markup=Keyboard().default_keyboard,
            )

        return bot.send_message(
            chat_id=chat_id,
            text=f"{correctness.format(word, word_translations)}\n\n{next_quiz}",
            reply_markup=Keyboard().quiz_keyboard_with_hint,
        )

    elif user_state == states.DELETE_TRANSLATION_STATE:

        logger.info("User %s sent message in DELETE_TRANSLATION_STATE", message.chat.id)

        translations = translation_controller.get_translations(
            user_id=user_id, word=message.text
        )
        if not translations:
            return bot.send_message(
                chat_id,
                TRANSLATION_DELETE_FAIL,
                reply_markup=Keyboard().default_keyboard,
            )

        translations = [
            user_translation.translation for user_translation in translations
        ]
        user_controller.update_user_state(
            user_state=states.DELETE_TRANSLATION_STATE_V2, message=message
        )
        user_controller.update_user_state_data(message=message, data=message.text)
        return bot.send_message(
            chat_id, TRANSLATION_DELETE_STEP_2.format(", ".join(translations))
        )

    elif user_state == states.DELETE_TRANSLATION_STATE_V2:

        logger.info(
            "User %s sent message in DELETE_TRANSLATION_STATE_V2", message.chat.id
        )

        user_state_data = user_controller.get_user_state_data(message)
        word = user_state_data["data"]

        success = translation_controller.delete_translation(
            translation=message.text, user_id=user_id, word=word
        )

        if not success:
            return bot.send_message(
                chat_id,
                TRANSLATION_DELETE_FAIL,
                reply_markup=Keyboard().default_keyboard,
            )

        user_controller.update_user_state(user_state=states.STATE_IDLE, message=message)
        return bot.send_message(
            chat_id, TRANSLATION_DELETED, reply_markup=Keyboard().default_keyboard
        )

    elif user_state == states.GET_DEFINITION_STATE:

        logger.info("User %s sent message in GET_DEFINITION_STATE", message.chat.id)

        definition_controller = DefinitionController(connection=session)
        word = translation_controller.prepare_string(message.text)
        definition = definition_controller.get_definition(word, user_id)
        definition_strings = definition_controller.extract_meanings(definition)

        definitions_len = len(definition_strings)

        user_controller.update_user_state(user_state=states.STATE_IDLE, message=message)

        for definition_string in definition_strings:
            definitions_len -= 1

            if definitions_len == 0:
                bot.send_message(
                    chat_id, definition_string, reply_markup=Keyboard().default_keyboard
                )
            else:
                bot.send_message(chat_id, definition_string)
    elif user_state == states.SEARCH_URBAN_DICTIONARY_STATE:

        logger.info(
            "User %s sent message in SEARCH_URBAN_DICTIONARY_STATE", message.chat.id
        )

        urban_dictionary_controller = UrbanDictionaryController(connection=session)
        word = translation_controller.prepare_string(message.text)
        urban_dictionary_definition = urban_dictionary_controller.search(word, user_id)

        return bot.send_message(
            chat_id=message.chat.id,
            text=urban_dictionary_definition,
            reply_markup=Keyboard().default_keyboard,
        )
    else:

        logger.error("User %s sent message in UNKNOWN STATE", message.chat.id)

        return bot.send_message(
            message.chat.id, START_TEMPLATE, reply_markup=Keyboard().default_keyboard
        )


if __name__ == "__main__":
    bot.infinity_polling(
        skip_pending=True,
        long_polling_timeout=10,
        allowed_updates=["message", "callback_query"],
    )
