NEW_USER = "NEW_USER"
ADD_WORD = "ADD_WORD"
ADD_TRANSLATION = "ADD_TRANSLATION"
CHECK_TRANSLATION = "CHECK_TRANSLATION"
STATE_IDLE = "STATE_IDLE"
QUIZ_STATE = "STATE_QUIZ"
DELETE_TRANSLATION_STATE = "DELETE_TRANSLATION_STATE"
DELETE_TRANSLATION_STATE_V2 = "DELETE_TRANSLATION_STATE_V2"
GET_DEFINITION_STATE = "GET_DEFINITION_STATE"
SEARCH_URBAN_DICTIONARY_STATE = "SEARCH_URBAN_DICTIONARY_STATE"
CONNECT_DICTIONARY_STATE = "CONNECT_DICTIONARY_STATE"
DISCONNECT_DICTIONARY_STATE = "DISCONNECT_DICTIONARY_STATE"

ALL_STATES_STRING = f"""'{
"','".join(
    (
        NEW_USER,
        ADD_WORD,
        ADD_TRANSLATION,
        CHECK_TRANSLATION,
        STATE_IDLE,
        QUIZ_STATE,
        DELETE_TRANSLATION_STATE,
        DELETE_TRANSLATION_STATE_V2,
        GET_DEFINITION_STATE,
        SEARCH_URBAN_DICTIONARY_STATE,
        CONNECT_DICTIONARY_STATE,
        DISCONNECT_DICTIONARY_STATE
    )
)
}'"""