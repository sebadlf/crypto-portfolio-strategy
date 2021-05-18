import logging, re, requests
import pandas as pd
from datetime import datetime as dt
import model_service
from sqlalchemy import create_engine
import keys
import traceback


logging.basicConfig(filename="binance.log",
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class Binance_new():
    _URL = 'https://api.binance.com/api/v3/'

    def __init__(self):
        self.currencies_list = []

    def getSymbols(self, quote_currency):

        symbols_list = []

        try:
            logger.info(f'Bajando lista de symbols en {quote_currency}')
            endpoint = self._URL + 'ticker/price'
            r = requests.get(endpoint).json()
            symbols = [dic['symbol'] for dic in r if re.search(quote_currency, dic['symbol'])]

            for symbol in symbols:
                search = r'\D*DOWN|UP|BULL|BEAR|^DAI|^BUSD|^TUSD|^USDC|^PAX|^USDT|^USDSB|^AUD|^EUR|^GBP|^SUSD'
                if re.search(search, symbol) is None:
                    base_currency = symbol.split(quote_currency)[0]
                    lst = [symbol, base_currency, quote_currency]
                    symbols_list.append(lst)
            # print(symbols_list)

        except:
            logger.exception(f'Error al bajar la lista de symbols')

        return symbols_list

    # def download_info(self, symbol, startTime, endTime = None, interval='4h', limit=1000):


    def download_info_while(self, symbol, startTime, interval='4h', limit=1000):

        startTime = int(dt.strptime(startTime, '%Y-%m-%d %H:%M:%S').timestamp() * 1000)

        last_previous_date = False

        endpoint = self._URL + 'klines'

        md_acumulated = []


        while True:

            try:
                # print(startTime)
                # print(endTime)

                if not md_acumulated == []:
                    startTime = md_acumulated[-1][0] #busco ultima fecha
                    md_acumulated = md_acumulated[0:-1] #borro ultimo valor

                params = {'symbol': symbol, 'interval': interval,
                          'limit': limit,
                          'startTime': startTime,
                          # 'endTime': endTime
                          }

                r = requests.get(endpoint, params=params).json()

                if r == {'code': -1121, 'msg': 'Invalid symbol.'}:
                    print(f'Invalid symbol {symbol}. No pudo bajar la md')
                    break


                md_acumulated += r

                if r == []:
                    print(f'fechas no validas ticker {symbol}')
                    break

                if startTime == last_previous_date:
                    break

                last_previous_date = startTime

            except:
                traceback.print_exc()


        return md_acumulated



    def getHistorical(self, symbol, startTime, endTime = None, quote_currency='USDT', interval='4h', limit=1000):
        """
        Interval: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
        Limit: 500, max: 1000
        startTime: %Y-%m-%d
        endTime: %Y-%m-%d OR "hoy"
        """
        symbol += quote_currency

        r = Binance_new().download_info_while(symbol, startTime, interval=interval, limit=limit)

        return r

    # YYYY-MM-DD
    def saveHistorical(self, quote_currency, since = '2021-01-01 00:00:00'):

        db_connection = create_engine(keys.DB_CONNECTION)

        if not since:
            since = dt.fromisoformat('2021-01-01')

        model_service.sync_coins_binance(self.getSymbols(quote_currency))

        model_service.sync_currencies()

        currenciesList = list(set(model_service.get_currencies_by_quote(quote_currency)) - set(self.currencies_list))
        print(f'{len(currenciesList)} Coins\n{currenciesList}')
        self.currencies_list += currenciesList
        
        for currency in currenciesList:
            print(currency, end=', ')

            try:
                last_date = model_service.last_date(currency, db_connection)

                if last_date:
                    model_service.del_row(last_date, db_connection)
                    since = last_date[1]

                historical_data = Binance_new().getHistorical(currency, startTime= since, quote_currency= quote_currency)
                if historical_data != []:
                    model_service.save_historical_data_binance(currency, historical_data, quote_currency)
            except:
                traceback.print_exc()
                pass
    
    
    def saveMarketData(self):
        quote_currencies = ['USDT', 'BTC', 'ETH', 'DAI', 'BUSD', 'USDC', 'EOS', 'ETC']
        for quote_currency in quote_currencies:
            print(f'Quote Currency: {quote_currency}')
            self.saveHistorical(quote_currency = quote_currency)        




# class Binance():
#
#     _URL = 'https://api.binance.com/api/v3/'
#
#     def getSymbols(self, quote_currency):
#         try:
#             logger.info(f'Bajando lista de symbols en USDT')
#             endpoint = self._URL+'ticker/price'
#             r = requests.get(endpoint).json()
#             symbols = [dic['symbol'] for dic in r if re.search(quote_currency, dic['symbol'])]
#
#             symbols_list = []
#             for symbol in symbols:
#                 search = r'\D*DOWN|UP|BULL|BEAR|^DAI|^BUSD|^TUSD|^USDC|^PAX|^USDT|^USDSB|^AUD|^EUR|^GBP|^SUSD'
#                 if re.search(search, symbol) is None:
#                     base_currency = symbol.split(quote_currency)[0]
#                     lst = [symbol, base_currency, quote_currency]
#                     symbols_list.append(lst)
#             # print(symbols_list)
#
#         except:
#             logger.exception(f'Error al bajar la lista de symbols')
#
#         return symbols_list
#
#
#     def getHistorical(self, symbol, quote_currency = 'USDT', interval = '4h', limit = 1000, startTime = '2021-03-16', endTime = '2021-04-19'):
#         """
#         Interval: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
#         Limit: 500, max: 1000
#         startTime: %Y-%m-%d
#         endTime: %Y-%m-%d OR "hoy"
#         """
#         symbol += quote_currency
#         startTime = int(dt.strptime(startTime, '%Y-%m-%d').timestamp() * 1000)
#         if endTime == 'hoy':
#             endTime = int(dt.now().timestamp() * 1000)
#         else:
#             endTime = int(dt.strptime(endTime, '%Y-%m-%d').timestamp() * 1000)
#
#         endpoint = self._URL+'klines'
#         params =  {'symbol': symbol, 'interval': interval, 'limit': limit, 'startTime': startTime, 'endTime': endTime}
#
#         try:
#             r = requests.get(endpoint, params=params).json()
#         except (ValueError, ConnectionError) as e:
#             logger.exception(f'Problemas con bajar la coin: {symbol}, puede que no se hayan bajado los datos por este error:\n{e}')
#             return r
#
#         return r
#
#     def saveHistorical(self, quote_currency):
#
#         model_service.sync_coins_binance(self.getSymbols(quote_currency))
#         currencies = model_service.get_currencies_list()
#
#         model_service.sync_currencies()
#
#         for currency in model_service.get_currencies_list():
#             print(currency, end=', ')
#
#             try:
#                 historical_data = Binance().getHistorical(currency)
#                 model_service.save_historical_data_binance(currency, historical_data)
#             except:
#                 pass

if __name__ == '__main__':
    # Binance_new().saveHistorical('USDT')
    
    Binance_new().saveMarketData()
    # print(prueba)

    # hoy = dt.now()
    # print(hoy)
    #
    # hoy = hoy.strftime('%Y-%m-%d %H:%M')
    # print(hoy)

    pass