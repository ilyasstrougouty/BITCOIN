import pandas as pd
import plotly.graph_objects as go
import plotly
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

bitcoin_price = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days=30)
df = pd.DataFrame(bitcoin_price['prices'], columns=['timestamp', 'price'])
df["date"] = pd.to_datetime(df['timestamp'], unit='ms')

candlestick_data = df.groupby(df.date.dt.date).agg({'price': ['min', 'max', 'first', 'last']})
fig = go.Figure(data=[go.Candlestick(x=candlestick_data.index,
                open=candlestick_data['price']['first'],
                high=candlestick_data['price']['max'],
                low=candlestick_data['price']['min'],
                close=candlestick_data['price']['last'])])

fig.update_layout(xaxis_rangeslider_visible=False,xaxis_title="Date",yaxis_title="Price (USD)",title="Bitcoin Price Over Past 30 Days")
plotly.offline.plot(fig, filename='bitcoin_price.html')