from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, create_engine, Index
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

import keys

# declarative base class
Base = declarative_base()

# an example mapping using the base
class Coin(Base):
    __tablename__ = 'coin'

    symbol = Column(String(20), primary_key=True)
    base_currency = Column(String(10))
    quote_currency = Column(String(10))

    __table_args__ = (
        Index('symbol', symbol),
    )

class Currency(Base):
    __tablename__ = 'currency'

    symbol = Column(String(10), primary_key=True)

    __table_args__ = (
        Index('symbol', symbol),
    )

class MarketData(Base):
    __tablename__ = 'market_data'

    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), ForeignKey('currency.symbol'))
    timestamp = Column(DATETIME)
    open = Column(Float)
    close = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume_from = Column(Float)
    volume_to = Column(Float)
    conversion_type = Column(String(20))
    conversion_symbol = Column(String(10))

    __table_args__ = (
        Index('symbol', symbol, timestamp),
    )

engine = create_engine(keys.DB_CONNECTION)

Base.metadata.create_all(engine)