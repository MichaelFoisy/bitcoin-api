# BITCOIN API Example
# Using pycoingecko
import pandas as pd
import plotly
from pycoingecko import CoinGeckoAPI

# Create client object
cg = CoinGeckoAPI()
# Request the data
bitcoin_data = cg.get_coin_market_chart_by_id(id = 'bitcoin', vs_currency = 'usd', days=30)
#print(bitcoin_data['prices'])

# Convert our nested list to a dataframe
data = pd.DataFrame(bitcoin_data['prices'], columns=['TimeStamp','Price'])
#print(data)

# Create readable time data
data['Date'] = pd.to_datetime(data['TimeStamp'], unit = 'ms')
#print(data)

# Create a candlestick plot. To get the data for the daily candlestick, group data to min, max, first, last price of each day
candlestick_data = data.groupby(data.Date.dt.date).agg({'Price': ['min', 'max', 'first', 'last']})
#print(candlestick_data)

# Use plotly to create the candlestick chart and plot it
import plotly.graph_objects as go
fig = go.Figure(data=[go.Candlestick(x = candlestick_data.index,
                                    open = candlestick_data['Price']['first'],
                                    high = candlestick_data['Price']['max'],
                                    low = candlestick_data['Price']['min'],
                                    close = candlestick_data['Price']['last'])])

fig.update_layout(xaxis_rangeslider_visible = False, xaxis_title = 'Date',
yaxis_title = 'Price (USD $)', title = 'Bitcoin Candlestick Chart Over Past 30 Days')

plotly.offline.plot(fig, filename = './bitcoin_candlestick_graph.html', auto_open=False)
