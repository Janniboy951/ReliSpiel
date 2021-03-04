from sqlalchemy import Column, String
from database import Base


class ReliSpiel(Base):
    # Name of the Table
    __tablename__ = "ReliSpiel"
    # Use existing table if possible
    __table_args__ = {'extend_existing': True}

    # Column Declaration
    id = Column(String(64), primary_key=True)
    solution = Column(String(1024))
    result = Column(String(1024))


