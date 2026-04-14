from config.base import Base
from sqlalchemy import Column, String, Integer, Enum, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Company(Base):
    __tablename__ = "company"
    id = Column("id", Integer, primary_key=True, autoincrement="auto", index=True)
    guid = Column("guid", String(36), nullable=False)
    companyName = Column("companyName", String(30), nullable=False)
    description = Column("description", String(50))
    status = Column("status", Enum("A", "D"), default='A')
    createdAt = Column("createdAt", TIMESTAMP, server_default=func.now(), nullable=False)
    updatedAt = Column("updatedAt", TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
    employees = relationship("Employee", back_populates="company", lazy="selectin")