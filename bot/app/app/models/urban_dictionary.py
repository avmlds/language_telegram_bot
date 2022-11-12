from sqlalchemy import (
    Column,
    BigInteger,
    String,
    UniqueConstraint,
    JSON,
    ForeignKey,
    DateTime,
    func,
)

from app.database.base_class import Base


class UrbanDictionaryModel(Base):
    __tablename__ = "urban_dictionary"
    __tableargs__ = (UniqueConstraint("defid", "word"),)

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    defid = Column(String, nullable=False, unique=True)
    word = Column(String, nullable=False, unique=True)
    author = Column(String)
    permalink = Column(String, nullable=False)
    definition = Column(String)
    example = Column(String)
    votes = Column(JSON)
    current_vote = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    requested_by = Column(BigInteger, ForeignKey("bot_user.id"))
