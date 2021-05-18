import numpy as np
import pandas as pd

pd.options.display.max_rows = 10000

import model_service
import config

def filter_return_1(df, vol_neg_accepted = 0):

    df_adjust = df.copy()
    df_adjust[df_adjust > vol_neg_accepted] = 0

    return df_adjust

def filter_return_2(df, coins_dict, vol_neg_accepted = 0):

    df_adjust = df.copy()
    coins_list = list(coins_dict.keys())
    coins_pond = [coins_dict[x] for x in coins_list]

    for i in range(len(coins_list)):
        if i == 0:
            df_adjust['roi'] = df_adjust[coins_list[i]] * coins_pond[i]
        else:
            df_adjust['roi'] = df_adjust['roi'] + df_adjust[coins_list[i]] * coins_pond[i]

    df_adjust[df_adjust['roi'] > 0] = 0
    df_adjust.drop(['roi'], axis = 1, inplace = True)

    return df_adjust



def markowitz(df, coins_dict, vol_neg_accepted = 0):
    r = {}
    r['coins'] = list(coins_dict.keys())
    r['pond'] = [coins_dict[x] for x in r['coins']]
    r['roi'] = np.sum((df.mean() * r['pond'] * 365))

    df_adjust = filter_return_1(df = df, vol_neg_accepted = vol_neg_accepted)
    r['volatility_1'] = np.sqrt(np.dot(r['pond'], np.dot(df_adjust.cov() * 365, r['pond'])))
    r['sortino_1'] = r['roi'] / r['volatility_1']

    df_adjust = filter_return_2(df = df, coins_dict = coins_dict, vol_neg_accepted = vol_neg_accepted)
    r['volatility_2'] = np.sqrt(np.dot(r['pond'], np.dot(df_adjust.cov() * 365, r['pond'])))
    r['sortino_2'] = r['roi'] / r['volatility_2']

    sharpe = {}
    sharpe['volatility'] = np.sqrt(np.dot(r['pond'], np.dot(df.cov() * 365, r['pond'])))
    sharpe['sharpe'] = r['roi'] / sharpe['volatility']

    return r, sharpe



retornos = None

def build_retornos():
    global retornos

    df = model_service.export_historical_data()

    df.drop(['id', 'open', 'high', 'low', 'volume', 'close_time', 'quote_asset_volume', 'trades',
             'taker_buy_base', 'taker_buy_quote', 'ignore', 'close', 'quote_currency'], axis=1, inplace=True)

    df = df.pivot(index='open_time', columns='symbol', values='close_adj')

    # borro up and down y las que no sean selected coins
    coins = df.columns
    selected_coins = []
    del_coins = [*config.stable_coins, *config.disallowed_coins]

    for symbol in coins:
        if symbol not in del_coins:
            selected_coins.append(symbol)

    columnas = df.columns
    for i in columnas:
        if i.endswith(('DOWN', 'UP')) or i not in selected_coins:
            df = df.drop([i], axis=1)

    # borro tickers que en algun momento no tengan datos (Nan)
    df_copy = df.dropna(axis=1)


    retornos = np.log((df_copy / df_copy.shift()).dropna())

    columnas = retornos.columns
    columnas_borrar = []
    # borro ticker si tiene mov mayor al 50%
    for fila in range(len(retornos)):
        for columna in range(len(retornos.iloc[fila])):
            retorno = retornos.iloc[fila, columna]
            if retorno > 0.5 or retorno < -0.5:
                columnas_borrar.append(columnas[columna])
    retornos.drop(columnas_borrar, axis=1, inplace= True)


def sortino_2(retornos, df_adjust, coins_dict, vol_neg_accepted = 0):
    r = {}
    r['coins'] = list(coins_dict.keys())
    r['pond'] = [coins_dict[x] for x in r['coins']]
    r['roi'] = np.sum((retornos.mean() * r['pond'] * 365))

    r['volatility_2'] = np.sqrt(np.dot(r['pond'], np.dot(df_adjust.cov() * 365, r['pond'])))
    r['sortino_2'] = r['roi'] / r['volatility_2']

    return {'roi': r['roi'], 'volatility': r['volatility_2'] , 'ratio': r['sortino_2']}

def calc_ratio(distribution):
    global retornos

    retornos_select = retornos.filter(list(distribution.keys())).dropna()
    df_adjust = filter_return_2(df=retornos_select, coins_dict=distribution)
    res = sortino_2(retornos=retornos_select, df_adjust = df_adjust, coins_dict=distribution)

    return res


def get_coins():

    coins = retornos.columns

    selected_coins = []
    del_coins = [*config.stable_coins, *config.disallowed_coins]

    for symbol in coins:
        if symbol not in del_coins:
            selected_coins.append(symbol)

    return selected_coins

if __name__ == '__main__':


    pass


