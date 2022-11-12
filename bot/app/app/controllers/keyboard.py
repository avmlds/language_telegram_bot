from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class Keyboard:

    ADD = "ADD"
    STOP_ADD = "STOP_ADD"
    LIST = "LIST"
    DELETE = "DELETE"
    START_QUIZ = "START_QUIZ"
    NEXT_QUIZ = "NEXT_QUIZ"
    STOP_QUIZ = "STOP_QUIZ"
    URBAN_RANDOM = "URBAN_RANDOM"
    URBAN_SEARCH = "URBAN_SEARCH"
    URBAN_ADD = "URBAN_ADD"
    HINT = "HINT"
    GIVE_TRANSLATION = "GIVE_TRANSLATION"
    GET_DEFINITION = "GET_DEFINITION"

    OPERATE_DICTIONARIES = "OPERATE_DICTIONARIES"
    CONNECT_DICTIONARY = "CONNECT_DICTIONARY"
    DISCONNECT_DICTIONARY = "DISCONNECT_DICTIONARY"

    EN_RU_DICTIONARY_3K = "EN-RU 3k words"

    @property
    def _en_ru_dictionary_3k(self):
        return InlineKeyboardButton(
            "EN-RU 3k words", callback_data=self.EN_RU_DICTIONARY_3K
        )

    @property
    def _hint(self):
        return InlineKeyboardButton("Give me a clue!", callback_data=self.HINT)

    @property
    def _full_translation(self):
        return InlineKeyboardButton("Show translation", callback_data=self.GIVE_TRANSLATION)

    @property
    def _add(self):
        return InlineKeyboardButton("Add words", callback_data=self.ADD)

    @property
    def _stop_adding(self):
        return InlineKeyboardButton("Go back", callback_data=self.STOP_ADD)

    @property
    def _list_words(self):
        return InlineKeyboardButton("List your words", callback_data=self.LIST)

    @property
    def _delete(self):
        return InlineKeyboardButton("Delete words", callback_data=self.DELETE)

    @property
    def _start_quiz(self):
        return InlineKeyboardButton("Quiz", callback_data=self.START_QUIZ)

    @property
    def _next_quiz(self):
        return InlineKeyboardButton("Next word", callback_data=self.NEXT_QUIZ)

    @property
    def _stop_quiz(self):
        return InlineKeyboardButton("Main Menu", callback_data=self.STOP_QUIZ)

    @property
    def _urban_random(self):
        return InlineKeyboardButton("UrbanDict Random", callback_data=self.URBAN_RANDOM)

    @property
    def _urban_search(self):
        return InlineKeyboardButton("UrbanDict Search", callback_data=self.URBAN_SEARCH)

    @property
    def _urban_add(self):
        return InlineKeyboardButton("UrbanDict Add", callback_data=self.URBAN_ADD)

    @property
    def _get_word_definition(self):
        return InlineKeyboardButton("Get definition", callback_data=self.GET_DEFINITION)

    @property
    def _get_operate_dictionary(self):
        return InlineKeyboardButton(
            "Manage dictionaries", callback_data=self.OPERATE_DICTIONARIES
        )

    @property
    def _get_connect_dictionary(self):
        return InlineKeyboardButton(
            "Connect dictionary", callback_data=self.CONNECT_DICTIONARY
        )

    @property
    def _get_disconnect_dictionary(self):
        return InlineKeyboardButton(
            "Disconnect dictionary", callback_data=self.DISCONNECT_DICTIONARY
        )

    @property
    def default_keyboard(self):
        keyboard = InlineKeyboardMarkup()
        keyboard.row_width = 2
        keyboard.add(
            self._add,
            self._delete,
            self._start_quiz,
            self._get_word_definition,
            self._get_connect_dictionary,
            self._get_disconnect_dictionary,
            self._urban_search,
            self._urban_random,
        )
        return keyboard

    @property
    def dictionaries_keyboard(self):
        keyboard = InlineKeyboardMarkup()
        keyboard.row_width = 1
        keyboard.add(self._en_ru_dictionary_3k)
        return keyboard

    @property
    def quiz_keyboard_with_hint(self):
        keyboard = InlineKeyboardMarkup()
        keyboard.row_width = 2
        keyboard.add(
            self._next_quiz, self._stop_quiz, self._hint, self._full_translation
        )
        return keyboard

    @property
    def quiz_keyboard_with_full_translation(self):
        keyboard = InlineKeyboardMarkup()
        keyboard.row_width = 2
        keyboard.add(self._next_quiz, self._stop_quiz, self._full_translation)
        return keyboard

    @property
    def quiz_keyboard(self):
        keyboard = InlineKeyboardMarkup()
        keyboard.row_width = 2
        keyboard.add(self._next_quiz, self._stop_quiz)
        return keyboard

    @property
    def add_word_keyboard(self):
        keyboard = InlineKeyboardMarkup()
        keyboard.row_width = 1
        keyboard.add(self._stop_adding)
        return keyboard
