from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Integer
from src.database import Base


class Atm(Base):
    __tablename__ = "atms"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    long = Column(Float)
    lat = Column(Float)
    money_in_current = Column(Float)
    money_in_max = Column(Float)
    money_out_current = Column(Float)
    money_out_max = Column(Float)

