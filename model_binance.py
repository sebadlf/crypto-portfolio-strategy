from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, create_engine, Index
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

import keys

Base = declarative_base()

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
    __tablename__ = 'market_data_binance'

    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), ForeignKey('currency.symbol'))
    open_time = Column(DATETIME)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)
    close_time = Column(DATETIME)
    quote_asset_volume = Column(Float)
    trades = Column(Integer)
    taker_buy_base = Column(Float)
    taker_buy_quote = Column(Float)
    ignore = Column(Float)
    quote_currency = Column(String(10))
    close_adj = Column(Float)

    __table_args__ = (
        Index('symbol', symbol, open_time),
    )


engine = create_engine(keys.DB_CONNECTION)

Base.metadata.create_all(engine)