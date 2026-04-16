from app.core.config import Base
from sqlalchemy import Column, String, Integer, Enum, TIMESTAMP, Numeric, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Employee(Base):
    __tablename__ = "employee"
    id = Column("id", Integer, primary_key=True, autoincrement="auto", index=True)
    guid = Column("guid", String(36), nullable=False)
    employeeName = Column("employeeName", String(50), nullable=False)
    designation = Column("designation", String(30))
    salary = Column("salary", Numeric(5,2))
    status = Column("status", Enum("A", "D"), default='A')
    createdAt = Column("createdAt", TIMESTAMP, server_default=func.now(), nullable=False)
    updatedAt = Column("updatedAt", TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
    companyId = Column("companyId", Integer, ForeignKey("company.id"))
    company = relationship("Company", back_populates="employees", lazy="selectin")