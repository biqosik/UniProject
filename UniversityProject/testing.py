import pandas as pd
import pandas_datareader as pdr
import datetime as dt
import plotly.graph_objects as go

def get_data():
    crypto_currency = "BTC"
    against_currency = "GBP"

    start = dt.datetime(2016, 1, 1)
    end = dt.datetime.now()

    data = pdr.DataReader(f'{crypto_currency}-{against_currency}', 'yahoo', start, end)

    trace1 = {
        'x': data.index,
        'open': data.Open,
        'close': data.Close,
        'high': data.High,
        'low': data.Low,
        'type': 'candlestick',
        'name': 'BBAS3',
        'showlegend': False
    }

    data = [trace1]
    # Config graph layout
    layout = go.Layout({
        'title': {
            'text': 'Bitcoin',
            'font': {
                'size': 15
            }
        }
    })

    fig = go.Figure(data=data, layout=layout)
    fig.show()
