from sqlalchemy import distinct
from sqlalchemy.orm import Session
from datetime import datetime
import traceback

import model, model_binance


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

def sync_coins_binance(binance_symbols):
    with Session(model_binance.engine) as session, session.begin():

        for pair in binance_symbols:
            symbol = pair[0]

            db_coin = session.query(model.Coin).filter_by(symbol=symbol).first()

            if not db_coin:
                db_coin = model.Coin(symbol=symbol)
                session.add(db_coin)

            db_coin.base_currency = pair[1]
            db_coin.quote_currency = pair[2]

def export_historical_data(table = 'market_data_binance'):
    import pandas as pd
    import model

    r = pd.read_sql(table, con=model.engine)

    return r



def save_historical_data_binance(symbol, historical_data):
    with Session(model_binance.engine) as session, session.begin():
        for hour_data in historical_data:

            market_data = model_binance.MarketData(symbol=symbol)
            session.add(market_data)

            market_data.open_time = datetime.fromtimestamp(hour_data[0]/1000)
            market_data.open = hour_data[1]
            market_data.high = hour_data[2]
            market_data.low = hour_data[3]
            market_data.close = hour_data[4]
            market_data.volume = hour_data[5]
            market_data.close_time = datetime.fromtimestamp(hour_data[6]/1000)
            market_data.quote_asset_volume = hour_data[7]
            market_data.trades = hour_data[8]
            market_data.taker_buy_base = hour_data[9]
            market_data.taker_buy_quote = hour_data[10]
            market_data.ignore = hour_data[11]

def last_date(symbol, conn,tabla = 'market_data_binance'):
    from sqlalchemy import create_engine
    import keys

    res = False

    try:
        query = f'SELECT `id`,`open_time` FROM {tabla} WHERE `symbol` = "{symbol}" ORDER BY `open_time` DESC limit 0,1'
        res = conn.execute(query).fetchone()
        fecha = res[1].strftime('%Y-%m-%d %H:%M:%S')
        res = (res[0], fecha)
    except:
        print(f'no hay ultima fecha de {symbol}, bajando historico')

    return res

def del_row(last_date, conn, tabla = 'market_data_binance'):

    id = last_date[0]
    query = f'DELETE FROM {tabla} WHERE `id`={id}'
    conn.execute(query)



if __name__ == '__main__':
    # from sqlalchemy import create_engine
    # import keys
    # db_connection = create_engine(keys.DB_CONNECTION)
    #
    # print(last_date('BTC', db_connection))

    lista1 = [0,1,2,3]
    lista2 = [4,5,6]

    lista = lista1 + lista2
    print(lista)

    pass


