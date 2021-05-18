import defi.defi_tools as dft
import pandas as pd

# import matplotlib.pyplot as plt
#
# df = dft.getProtocols()
# fig, ax = plt.subplots(figsize=(12,6))
# top_20 = df.sort_values('tvl', ascending=False).head(20)
#
# chains = top_20.groupby('chain').size().index.values.tolist()
# for chain in chains:
#     filtro = top_20.loc[top_20.chain==chain]
#     ax.bar(filtro.index, filtro.tvl, label=chain)
#
# ax.set_title('Top 20 dApp TVL, groupBy dApp main Chain', fontsize=14)
# plt.legend()
# plt.xticks(rotation=90)
# plt.show()

pd.options.display.max_columns = 250
#
data = dft.geckoList(page=2, per_page=1000)
print(data)
print(data.columns)

# df = dft.geckoMarkets('ltc')
# print(df)
# print(df.info())

diccionario = {'base': 'ADA', 'quote': 'BTC', 'value_quote': 10, 'value_usdt': 100}





