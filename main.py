import binance
import markowitz_sortino
import marcopolo


binance.Binance_new().saveHistorical('USDT')
markowitz_sortino.build_retornos()
marcopolo.run_montecarlo()









# if name == 'main':
#     import cryptocompare
#     print(cryptocompare.get_historical_price_hour('1INCH', "USDT", limit=2000, exchange="binance")[0])
