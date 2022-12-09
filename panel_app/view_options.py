import dask.dataframe as dd
import holoviews as hv
from holoviews.operation.datashader import rasterize
from holoviews.operation.datashader import dynspread
import panel as pn
import datetime as dt
pn.extension()
hv.extension('bokeh')
#load data
ddf = dd.read_parquet('../data/crypto_dataset/2015_flights.parquet').persist()

#create graph
points=hv.Points(ddf[["SCHEDULED_DEPARTURE","DEPARTURE_DELAY"]])

#different plots
pts1 = rasterize(points).opts(tools=["hover"], width=600,cmap='inferno', colorbar=True, cnorm='log',title='resize points and colourbar on zoom')
pts2 = rasterize(points).opts(tools=["hover"], width=600, cmap='PuOr', colorbar=True, axiswise=True, cnorm='log',title='only resize axis, axis not linked',clim=(0, 10000))
pts3 = rasterize(points).opts(cnorm='eq_hist', width=600,cmap='YlOrRd', colorbar=True,title='points on zoom',tools=["hover"])
pts4 = rasterize(points).opts(cnorm='eq_hist', width=600,cmap='viridis', colorbar=True,title='points on zoom resize',tools=["hover"])

#layout

rolling_window = pn.widgets.IntSlider(name='Rolling Window', value=10, start=1, end=365)
select = pn.widgets.Select(name='Select', options=['Biology', 'Chemistry', 'Physics'])
multi_choice = pn.widgets.MultiChoice(name='MultiSelect', value=['Apple', 'Pear'],
    options=['Apple', 'Banana', 'Pear', 'Strawberry'])
date_picker = pn.widgets.DatePicker(name='Date Picker',value=dt.date.today())
first_app = pn.Row(
    pn.Column(rolling_window, select, multi_choice, date_picker),
    pn.Column(pts3, dynspread(pts4)),
    pn.Column(dynspread(pts1), pts2))
first_app.servable()

#panel serve --warm --autoreload --show .\main.py