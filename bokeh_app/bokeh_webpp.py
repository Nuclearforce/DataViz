from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.layouts import row, column, gridplot

import pandas as pd
import numpy as np
import math

from bokeh.io import curdoc

x = np.arange(0, math.pi*2, 0.05)

df = pd.DataFrame(dict(
    x = x,
    sin = np.sin(x),
    cos = np.cos(x),
    tan = np.tan(x)
))

source = ColumnDataSource(data=df)

#-------------------------------
#   Sine Wave
#-------------------------------
p1 = figure(title = "Sine wave",
            x_axis_label = 'x',
            y_axis_label = 'y',
            plot_width=300,
            plot_height=300
)
p1.line('x', 'sin',
        source=source,
        legend_label = "sine",
        line_width = 2)

#-------------------------------
#   Cosine Wave
#-------------------------------
p2 = figure(title = "Cosine wave",
            x_axis_label = 'x',
            y_axis_label = 'y',
            plot_width=300,
            plot_height=300
)
p2.line('x', 'cos',
        source=source,
        legend_label = "cos",
        line_width = 2)

#-------------------------------
#   Tangent Wave
#-------------------------------
p3 = figure(title = "Tangent wave",
            x_axis_label = 'x',
            y_axis_label = 'y',
            plot_width=300,
            plot_height=300
)
p3.line('x', 'tan',
        source=source,
        legend_label = "tan",
        line_width = 2)

#-------------------------------
#   Laying out in gridplot
#-------------------------------
plot = gridplot([p1, p2, p3], ncols=2, sizing_mode='stretch_both')

# output_file("sine_cosine_tangent.html")
# show(plot)

curdoc().add_root(plot)
curdoc().title = "Using the Bokeh Server"
