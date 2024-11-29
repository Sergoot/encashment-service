from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import BigInteger
from src.database import Base


class Atm(Base):
    __tablename__ = "atms"

    id = Column(BigInteger, autoincrement=True, primary_key=True, index=True)
    osm_id = Column(BigInteger)
    long = Column(Float)
    lat = Column(Float)
    money_current = Column(Float)
    money_max = Column(Float)
