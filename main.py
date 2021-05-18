import binance
import markowitz_sortino
import marcopolo
import telegram_bot as tb

binance.Binance_new().saveMarketData()
markowitz_sortino.build_retornos()
best_portfolio = marcopolo.run_montecarlo()

print("best_portfolio", best_portfolio)
tb.send_telegram_message(str(best_portfolio))


# if name == 'main':
#     import cryptocompare
#     print(cryptocompare.get_historical_price_hour('1INCH', "USDT", limit=2000, exchange="binance")[0])
