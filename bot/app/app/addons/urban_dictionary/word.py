class Word:
    """A data class representing a word from the UrbanDictionary API

    .. table:: Available operations
        :widths: auto

        ==========  =========================================
        Operation   Result
        ==========  =========================================
        ``x == y``      Checks if two Words are equal
        ``x != y``      Checks if two Words are not equal
        ``str(x)``      Returns the string representation of a Word
        ==========  =========================================

    Attributes:
        author (str): The author of the definition contained in the object.

        current_vote (str): An inexplicably empty string as far as I can tell, but included in the API response nonetheless.
        defid (int): The UrbanDictionary definition ID.

        definition (str): The definition of the word.

        example (str): User created examples of the word. Typically used in a sentence (or a few).

        permalink (str): The link to the definition of the word.

        votes (Dict[str, int]): A dict containing both the upvotes and downvotes for this word and definition pair.

            .. code:: python3

                # Example structure
                {
                    'up': 400,
                    'down': 20
                }

        word (str): The actual word.

    """

    def __init__(self, urban_dict: dict):
        self.defid = urban_dict["defid"]
        self.word = urban_dict["word"]
        self.author = urban_dict["author"]
        self.permalink = urban_dict["permalink"]
        self.definition = urban_dict["definition"]
        self.example = urban_dict["example"]
        self.votes = {"up": urban_dict["thumbs_up"], "down": urban_dict["thumbs_down"]}
        self.current_vote = urban_dict[
            "current_vote"
        ]  # This seems to always be an empty string

    @property
    def message(self):
        return f"*Expression:* {self.word}\n\n*Definition:* {self.definition}\n\n*Example*: {self.example}"

    def __str__(self) -> str:
        return self.word

    def __repr__(self) -> str:
        return "<Word word={0.word!r} defid={0.defid!r}>".format(self)

    def __eq__(self, other) -> bool:
        return isinstance(other, Word) and other.defid == self.defid
