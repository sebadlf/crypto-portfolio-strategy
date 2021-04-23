import logging, re, requests
import pandas as pd
from datetime import datetime as dt
import model_service


logging.basicConfig(filename="binance.log",
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class Binance():

    _URL = 'https://api.binance.com/api/v3/'

    def getSymbols(self, base_currency):
        try:
            logger.info(f'Bajando lista de symbols en USDT')    
            endpoint = self._URL+'ticker/price'
            r = requests.get(endpoint).json()
            symbols = [dic['symbol'] for dic in r if re.search(base_currency, dic['symbol'])]
            
            symbols_list = []
            for symbol in symbols:
                search = r'\D*DOWN|UP|BULL|BEAR|^DAI|^BUSD|^TUSD|^USDC|^PAX|^USDT'
                if re.search(search, symbol) is None:
                    quote_currency = symbol.split(base_currency)[0]
                    lst = [symbol, base_currency, quote_currency]
                    symbols_list.append(lst)
            print(symbols_list)
                
        except:
            logger.exception(f'Error al bajar la lista de symbols')

        return symbols_list

          
    def getHistorical(self, symbol, interval = '4h', limit = 1000, startTime = '2021-03-16', endTime = '2021-04-19'):
        """
        Interval: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
        Limit: 500, max: 1000
        startTime: %Y-%m-%d
        endTime: %Y-%m-%d OR "hoy"
        """
              
        startTime = int(dt.strptime(startTime, '%Y-%m-%d').timestamp() * 1000)
        if endTime == 'hoy':
            endTime = int(dt.now().timestamp() * 1000)
        else:    
            endTime = int(dt.strptime(endTime, '%Y-%m-%d').timestamp() * 1000)

        endpoint = self._URL+'klines'
        params =  {'symbol': symbol, 'interval': interval, 'limit': limit, 'startTime': startTime, 'endTime': endTime}
        
        try:
            r = requests.get(endpoint, params=params).json()            
        except (ValueError, ConnectionError) as e:
            logger.exception(f'Problemas con bajar la coin: {symbol}, puede que no se hayan bajado los datos por este error:\n{e}')
            return r

        return r

    def saveHistorical(self):
        model_service.sync_coins_binance(self.getSymbols('USDT'))
        currencies = model_service.get_currencies_list()

        for currency in currencies:
            print(currency)
            