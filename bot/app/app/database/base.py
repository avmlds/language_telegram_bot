# Import all the models, so that Base has them before being
# imported by Alembic
from app.database.base_class import Base  # noqa
from app.models.dictionaries import Dictionary  # noqa
from app.models.dictionaries import Dictionary  # noqa
from app.models.dictionaries import DictionaryContent  # noqa
from app.models.dictionaries import UsersDictionaries  # noqa
from app.models.dictionaries import UserDictionaryKnowledge # noqa
from app.models.translations import UserTranslation  # noqa
from app.models.users import BotUser  # noqa
from app.models.users import UserState  # noqa
from app.models.urban_dictionary import UrbanDictionaryModel  # noqa
from app.models.definition import Definition  # noqa
