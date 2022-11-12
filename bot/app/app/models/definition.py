from sqlalchemy import (
    Column,
    BigInteger,
    String,
    JSON,
    DateTime,
    func,
    ForeignKey,
)

from app.database.base_class import Base


class Definition(Base):
    __tablename__ = "definition"

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    word = Column(String, nullable=False, unique=True)
    phonetic = Column(String)
    phonetics = Column(JSON)
    origin = Column(String)
    meanings = Column(JSON)
    license = Column(JSON)
    source_url = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())
    requested_by = Column(BigInteger, ForeignKey("bot_user.id"))
