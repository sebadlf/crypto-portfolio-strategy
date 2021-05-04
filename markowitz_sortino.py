import numpy as np
import pandas as pd

import model_service

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




if __name__ == '__main__':
    from sqlalchemy import create_engine
    activos = {'1INCH': 0.5, 'AAVE': 0.3, 'ACM': 0.2}


    df = model_service.export_historical_data()

    df.drop(['id', 'open', 'high', 'low', 'volume', 'close_time', 'quote_asset_volume', 'trades',
             'taker_buy_base', 'taker_buy_quote', 'ignore'], axis= 1, inplace= True)

    df = df.pivot(index='open_time', columns='symbol', values='close')

    # borro up and down
    columnas = df.columns
    for i in columnas:
        if i.endswith(('DOWN','UP')):
            df = df.drop([i], axis=1)

    columnas = df.columns
    df_copy = df.copy()
    for i in range(len(df.iloc[0])):
        if not df.iloc[0, i] > 0:
            columna_borrar = columnas[i]
            df_copy.drop([columna_borrar], axis=1, inplace= True)
            # print(columna_borrar)

    # df_copy.to_excel('pturbs.xlsx')

    retornos = df_copy.pct_change()
    retornos = retornos.dropna()
    # print(retornos)

    retornos = retornos.filter(list(activos.keys())).dropna()

    df_ajustado = filter_return_2(df = retornos, coins_dict=activos)
    print(df_ajustado)

    print(markowitz(df = df_ajustado, coins_dict= activos))


