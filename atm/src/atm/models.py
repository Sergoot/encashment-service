from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import BigInteger, Integer, ForeignKey
from src.database import Base


class Atm(Base):
    __tablename__ = "atms"

    id = Column(BigInteger, autoincrement=True, primary_key=True, index=True)
    osm_id = Column(BigInteger)
    long = Column(Float)
    lat = Column(Float)
    money_in_current = Column(Float)
    money_in_max = Column(Float)
    money_out_current = Column(Float)
    money_out_max = Column(Float)


class AtmsDistances(Base):
    __tablename__ = "atms_distances"

    id = Column(BigInteger, autoincrement=True, primary_key=True, index=True)
    atm1_id = Column(ForeignKey(Atm.id), unique=True)
    atm2_id = Column(ForeignKey(Atm.id))
    distance = Column(Integer)