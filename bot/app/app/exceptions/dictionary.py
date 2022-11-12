class DictionaryNotFoundException(Exception):
    def __init__(self, dictionary_name):
        super().__init__(f"Dictionary with name {dictionary_name} is not found.")
