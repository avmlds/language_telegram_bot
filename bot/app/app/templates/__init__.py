START_TEMPLATE = """
Hello!
I will help you to learn English!
Add new words to the bot. Then learn them by doing the quiz. 
Happy learning!"""

ADD_WORD_TEMPLATE = "Write down your word"

ADD_TRANSLATION_TEMPLATE = "Write down the translation"

TRANSLATION_ADDED_TEMPLATE = """Added successfully!
You can continue adding words or go back to the Main Menu"""
TRANSLATION_TOO_LONG = "{}\nContinue adding word and translation or stop addition process by pressing the button!"

TRANSLATION_DELETE_TEMPLATE = (
    """Type the word which you want to delete."""
)
TRANSLATION_DELETE_FAIL = """This word is not in the database, check the spelling."""
TRANSLATION_DELETE_STEP_2 = (
    """Write the translation to be deleted.\nPossible translations:\n*{}*"""
)
TRANSLATION_DELETED = """Translation successfully deleted!"""

TRANSLATION_QUIZ_STARTED = """Type the translation for:\n\n*{}*"""
TRANSLATION_CORRECT = """Correct!\n*{0}* - *{1}*"""
TRANSLATION_INCORRECT = """Incorrect!\n*{0}* - *{1}*"""
TRANSLATION_HINT = """Hint for a word *{0}*:\n*{1}*"""
TRANSLATION_FULL = """Correct translation:\n\n*{0}* - *{1}*"""
TRANSLATION_NO_HINT = """No hint available, sorry"""

GET_DEFINITION = "Write the word for which you want to get definition."
DEFINITION_TEMPLATE = "Word: *{0}*\n\nPhonetic: *{1}*\n\nMeaning: *{2}*"
SEARCH_URBAN_DICTIONARY_TEMPLATE = "Write down the word or phrase"
