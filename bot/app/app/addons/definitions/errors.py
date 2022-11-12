class DefinitionException(Exception):
    def __init__(self):
        super().__init__("Definition API is unavailable now. Please, try again later.")
