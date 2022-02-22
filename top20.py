import requests
import pandas as pd
import matplotlib.pyplot as plt


def geckoHistorical(ticker, vs_currency='usd', days='max'):
    url = f"https://api.coingecko.com/api/v3/coins/{ticker}/market_chart"
    params = {"vs_currency":{vs_currency}, "days":days}
    r = requests.get(url, params).json()
    prices = pd.DataFrame(r['prices'])
    market_caps = pd.DataFrame(r['market_caps'])
    total_volumes = pd.DataFrame(r['total_volumes'])
    df = pd.concat([prices, market_caps[1], total_volumes[1]], axis=1)
    df[0] = pd.to_datetime(df[0], unit='ms')
    df.columns = ['date','price','market_caps','total_volumes']
    df.set_index('date', inplace=True)
    return df

top_2021 = ['bitcoin','ethereum','litecoin','ripple','polkadot', 'bitcoin-cash','cardano',
              'binancecoin','chainlink','bitcoin-cash-sv','stellar','eos','monero','theta-token',
             'tron','nem','vechain','tezos','celsius-degree-token','uniswap']

data = []
for coin in top_2021:
     data.append(geckoHistorical(coin, days=414)['price'].resample('1D').last())
        
df = pd.DataFrame(data).T
df.columns = top_2021

df.dropna(inplace=True)
pd.options.display.max_columns=14
rendimientos_usd = (df/df.iloc[0]).iloc[-1]
rendimientos_btc = rendimientos_usd/rendimientos_usd['bitcoin']
df

plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(15,8))
ax.set_title('\nRendimiento en USD desde Enero de 2021, monedas top mktCap en ese momento\n', fontsize=15)

colors = []
for i in range(len(top_2021)):
    value = (rendimientos_usd-1).iloc[i]
    if value > 0 :
        colors.append('white')
    else:
        colors.append('red')
    ax.annotate(f"{value:.0%}", xy = (df.columns[i], max(0,value*100)+40), rotation=90, fontsize=12, color=colors[i])

ax.bar(rendimientos_usd.index, (rendimientos_usd-1)*100, color=colors, width=0.5)
ax.grid(alpha=0.3)
plt.xticks(rotation = 90, fontsize=14)

ax.set_ylim(-100,1050)
plt.show()