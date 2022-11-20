from sqlalchemy import (
    Column,
    String,
    Text,
    Boolean,
    Numeric,
    BigInteger,
    ForeignKey,
    UniqueConstraint,
    func,
    DateTime,
    Integer,
)

from app.database.base_class import Base


class UserDictionaryKnowledge(Base):
    """Table to store user knowledge of dictionary words."""
    __tablename__ = "user_dictionary_knowledge"
    __tableargs__ = UniqueConstraint("user_id", "dictionary_content_id")

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("bot_user.id"), nullable=False)
    dictionary_content_id = Column(BigInteger, ForeignKey("dictionary_content.id"), nullable=False)
    word_knowledge = Column(Integer, server_default="0", default=0)


class DictionaryContent(Base):
    """Table to store translations."""

    __tablename__ = "dictionary_content"
    __tableargs__ = UniqueConstraint("dictionary_id", "word", "translation")

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    dictionary_id = Column(BigInteger, ForeignKey("dictionary.id"), nullable=False)
    word = Column(String, nullable=False)
    translation = Column(String, nullable=False)
    word_meaning = Column(String)
    translation_meaning = Column(String)


class Dictionary(Base):
    """Dictionary table for any language."""

    __tablename__ = "dictionary"

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    description = Column(Text)
    is_paid = Column(Boolean, nullable=False, default=True)
    price = Column(Numeric(precision=18, scale=2), nullable=False, default=0)
    created_at = Column(DateTime, server_default=func.now())


class UsersDictionaries(Base):
    """Many2Many table for bot users and dictionaries."""

    __tablename__ = "users_dictionaries"
    __tableargs__ = (UniqueConstraint("user_id", "dictionary_id"),)

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("bot_user.id"), nullable=False)
    dictionary_id = Column(BigInteger, ForeignKey("dictionary.id"), nullable=False)
