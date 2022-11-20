class RewardController:
    """Controller for managing scores and rewards."""

    HINT_PEND = -1
    TRANSLATION_PEND = -2
    ANSWER_PEND = -2
    ANSWER_REWARD = 2

    ALLOWED_PENDS_REWARDS = [
        HINT_PEND,
        TRANSLATION_PEND,
        ANSWER_PEND,
        ANSWER_REWARD,
    ]

    @classmethod
    def modify_knowledge(cls, objects, reward_type):
        """Modify word_knowledge field in objects."""

        if reward_type not in cls.ALLOWED_PENDS_REWARDS:
            raise Exception("This reward type is not allowed")

        for word_object in objects:
            word_object.word_knowledge += reward_type
        return objects
