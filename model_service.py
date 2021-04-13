from sqlalchemy import distinct
from sqlalchemy.orm import Session
from datetime import datetime

import model


def sync_coins(cryptocompare_pairs):
    with Session(model.engine) as session, session.begin():

        for pair in cryptocompare_pairs:
            symbol = pair['exchange_fsym'] + pair['exchange_tsym']

            db_coin = session.query(model.Coin).filter_by(symbol=symbol).first()

            if not db_coin:
                db_coin = model.Coin(symbol=symbol)
                session.add(db_coin)

            db_coin.base_currency = pair['exchange_fsym']
            db_coin.quote_currency = pair['exchange_tsym']

def get_currencies_list():
    with Session(model.engine) as session:
        results = session.query(distinct(model.Coin.base_currency)).all()
        currencies = [r[0] for r in results]

        return currencies


def sync_currencies():
    with Session(model.engine) as session, session.begin():
        currencies = get_currencies_list()

        for currency in currencies:

            db_currency = session.query(model.Currency).filter_by(symbol=currency).first()

            print(currency)

            if not db_currency:
                db_currency = model.Currency(symbol=currency)
                session.add(db_currency)

def save_historical_data(symbol, historical_data):
    with Session(model.engine) as session, session.begin():
        for hour_data in historical_data:

            market_data = model.MarketData(symbol=symbol)
            session.add(market_data)

            market_data.timestamp = datetime.fromtimestamp(hour_data['time'])
            market_data.high = hour_data['high']
            market_data.low = hour_data['low']
            market_data.open = hour_data['open']
            market_data.close = hour_data['close']
            market_data.volume_from = hour_data['volumefrom']
            market_data.volume_to = hour_data['volumeto']
            market_data.conversion_type = hour_data['conversionType']
            market_data.conversion_symbol = hour_data['conversionSymbol']


