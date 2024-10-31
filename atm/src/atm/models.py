from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Integer
from src.database import Base


class Atm(Base):
    __tablename__ = "atms"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    long = Column(Float)
    lat = Column(Float)
    priem_current = Column(Float)
    priem_max = Column(Float)
    vidacha_current = Column(Float)
    vidacha_max = Column(Float)

