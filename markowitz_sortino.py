import numpy as np
import pandas as pd

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

    df_adjust = df_adjust[df_adjust['roi'] < vol_neg_accepted]
    df_adjust.drop(['roi'], axis = 1, inplace = True)

    print(df_adjust)

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
    activos = {'BTC': 0.5, 'ETH': 0.3, 'LTC': 0.2}

    # ---------------- PRUEBA EN MI PC CON UNA DB QUE TENIA ANTES -------------
    from sqlalchemy import create_engine

    DB_MARKOWITZ = 'mysql+pymysql://root:@localhost/markowitz'
    sql_engine = create_engine(DB_MARKOWITZ)
    sql_conn = sql_engine.connect()
    retornos = pd.read_sql("retornos", con=sql_conn)
    retornos = retornos.filter(list(activos.keys())).dropna()

    # print(retornos)
    # df_ajustado = filter_return(df = retornos)
    # print(df_ajustado)

    print(markowitz(df = retornos, coins_dict= activos))