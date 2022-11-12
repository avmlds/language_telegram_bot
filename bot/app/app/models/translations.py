from sqlalchemy import (
    Column,
    String,
    BigInteger,
    ForeignKey,
    UniqueConstraint,
    DateTime,
    func,
)

from app.database.base_class import Base


class UserTranslation(Base):
    __tablename__ = "user_translation"
    __tableargs__ = (
        UniqueConstraint(
            "word_representation",
            "word",
            "translation",
            "translation_representation",
            "user_id",
        ),
    )

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("bot_user.id"))
    # representation is an actual word that were typed by a user
    word_representation = Column(String(300))
    # and word is a casefolded word
    word = Column(String(300), nullable=False)
    translation_representation = Column(String(300))
    translation = Column(String(300), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
