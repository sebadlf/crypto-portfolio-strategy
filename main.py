import model_service
import cryptocompare

from keys import CRYPTOCOMPARE_APIKEY

cryptocompare.cryptocompare._set_api_key_parameter(CRYPTOCOMPARE_APIKEY)

cryptocompare_pairs = cryptocompare.get_pairs("binance")
model_service.sync_coins(cryptocompare_pairs)

model_service.sync_currencies()

for currency in model_service.get_currencies_list():
    print(currency)

    try:
        historical_data = cryptocompare.get_historical_price_hour(currency, "USDT", limit=2000)
        model_service.save_historical_data(currency, historical_data)
    except:
        pass




# if name == 'main':
#     import cryptocompare
#     print(cryptocompare.get_historical_price_hour('1INCH', "USDT", limit=2000, exchange="binance")[0])
