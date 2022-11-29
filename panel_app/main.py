import pandas as pd
import numpy as np
import dask.dataframe as dd
import holoviews as hv
from holoviews.operation.datashader import rasterize
from holoviews.operation.datashader import dynspread

# ddf = dd.read_parquet('../data/crypto_dataset/2015_flights.parquet').persist()

num=600000
np.random.seed(1)

dists = {cat: pd.DataFrame(dict([('x',np.random.normal(x,s,num)), 
                                 ('y',np.random.normal(y,s,num)), 
                                 ('val',val), 
                                 ('cat',cat)]))      
         for x,  y,  s,  val, cat in 
         [(  2,  2, 0.03, 10, "d1"), 
          (  2, -2, 0.10, 20, "d2"), 
          ( -2, -2, 0.50, 30, "d3"), 
          ( -2,  2, 1.00, 40, "d4"), 
          (  0,  0, 3.00, 50, "d5")] }
points = hv.Points(np.random.multivariate_normal((0,0), [[0.1, 0.1], [0.1, 1.0]], (100000,)),label="Points")
df = pd.concat(dists,ignore_index=True)
df["cat"]=df["cat"].astype("category")

ropts = dict(tools=["hover"], height=380, width=330, colorbar=True, colorbar_position="bottom")
pts1 = rasterize(hv.Points(df)).opts(**ropts).opts(tools=[], cnorm='log', axiswise=True)
pts2 = rasterize(hv.Points(df)).opts(**ropts).opts(tools=[], cnorm='log', axiswise=True)
pts = rasterize(points).opts(cnorm='eq_hist')

# pts1 + pts2.opts(clim=(0, 10000))+pts + dynspread(pts)


import panel as pn
pn.extension()


# interactive = pn.bind(find_outliers, window=window, sigma=sigma)

first_app = pn.Column(pts, dynspread(pts), pts1, pts2.opts(clim=(0, 10000)))

first_app.servable();