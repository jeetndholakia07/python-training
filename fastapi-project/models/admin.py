from ..config.base import Base
from sqlalchemy import Column, String, Integer, TIMESTAMP, func

class Admin(Base):
    __tablename__ = "admin"
    id = Column("id", Integer, primary_key=True, index=True)
    username = Column("username", String(30), nullable=False)
    guid = Column("guid", String(36), nullable=False)
    email = Column("email", String(100), nullable=False, unique=True)
    password_hash = Column("password_hash", String(100), nullable=False)
    createdAt = Column("createdAt", TIMESTAMP, server_default=func.now(), nullable=False)
    updatedAt = Column("updatedAt", TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)