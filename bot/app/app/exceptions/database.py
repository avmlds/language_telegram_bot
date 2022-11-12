"""Module with custom database exceptions."""


class DbEmptyException(Exception):
    def __init__(self):
        super(DbEmptyException, self).__init__(
            "You should add words or connect dictionary before taking quiz!"
        )


class WordTooLong(Exception):
    def __init__(self, word):
        super(WordTooLong, self).__init__(
            f"Word {word[:300]} is too long (> 300 chars), sorry!"
        )


class TranslationTooLong(Exception):
    def __init__(self, translation):
        super(TranslationTooLong, self).__init__(
            f"Translation {translation[:300]} is too long (> 300 chars), sorry!"
        )
