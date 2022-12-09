import panel as pn
import holoviews as hv
import pandas as pd
import dask.dataframe as dd
from holoviews.operation.datashader import rasterize
from holoviews.operation.datashader import dynspread
from bokeh.sampledata import stocks
hv.extension('bokeh')
pn.extension()
#load data
ddf = dd.read_parquet('../data/crypto_dataset/2015_flights.parquet').persist()
def load_data(y_axis,x_axis, **kwargs):
    points=hv.Points(ddf[[x_axis, y_axis]])
    return points
    # return rasterize(points).opts(tools=["hover"], width=730,cmap='inferno', colorbar=True, cnorm='log',title='resize points and colourbar on zoom')
y_options=['DISTANCE','SCHEDULED_DEPARTURE']
x_options=['ARRIVAL_DELAY','DEPARTURE_DELAY']
dmap = hv.DynamicMap(load_data, kdims=['XOptions','YOptions']).redim.values(YOptions=y_options,XOptions=x_options)
def load_symbol(symbol, **kwargs):
    df = pd.DataFrame(getattr(stocks, symbol))
    df['date'] = df.date.astype('datetime64[ns]')
    return hv.Curve(df, ('date', 'Date'), ('adj_close', 'Adjusted Close'))

stock_symbols = ['AAPL', 'FB', 'GOOG', 'IBM', 'MSFT']
dmap2 = hv.DynamicMap(load_symbol, kdims='Symbol').redim.values(Symbol=stock_symbols)
second_app = pn.Row(
    pn.Column(dynspread(rasterize(dmap).opts(tools=["hover"], width=730,cmap='inferno', colorbar=True, cnorm='log',title='resize points and colourbar on zoom',axiswise=True))),
    pn.Column(dmap2)
    )
second_app.servable()
#panel serve --warm --autoreload --show .\main.py