#uses custom template for dashboard. This dashboard displays the cpu and memory usage, updates every 500ms
import psutil
import panel as pn
import pandas as pd
import holoviews as hv
from holoviews import dim, opts
from jinja2 import Environment, FileSystemLoader

hv.extension("bokeh")

#load custom template
env = Environment(loader=FileSystemLoader('.'))
jinja_template = env.get_template('HRV_draft/templates/bootstrap.html')
tmpl = pn.Template(jinja_template)

# Define functions to get memory  usage
def get_mem_data():
    vmem = psutil.virtual_memory()
    df = pd.DataFrame(dict(free=vmem.free/vmem.total,
                           used=vmem.used/vmem.total),
                      index=[pd.Timestamp.now()])
    return df*100

# Define functions to get CPU usage
def get_cpu_data():
    cpu_percent = psutil.cpu_percent(percpu=True)
    df = pd.DataFrame(list(enumerate(cpu_percent)),
                      columns=['CPU', 'Utilization'])
    df['time'] = pd.Timestamp.now()
    return df

# Define DynamicMap callbacks returning Elements for memory
def mem_stack(data):
    data = pd.melt(data, 'index', var_name='Type', value_name='Usage')
    areas = hv.Dataset(data).to(hv.Area, 'index', 'Usage')
    return hv.Area.stack(areas.overlay()).relabel('Memory')

# Define DynamicMap callbacks returning Elements for cpu
def cpu_box(data):
    return hv.BoxWhisker(data, 'CPU', 'Utilization', label='CPU Usage')

# Set up StreamingDataFrame and add async callback
cpu_stream = hv.streams.Buffer(get_cpu_data(), 800, index=False)
mem_stream = hv.streams.Buffer(get_mem_data())

# Define DynamicMaps and display plot
cpu_dmap = hv.DynamicMap(cpu_box, streams=[cpu_stream]).opts(
    opts.BoxWhisker(box_fill_color=dim('CPU').str(), cmap='Category20',
                    width=500, height=400, ylim=(0, 100))
)
mem_dmap = hv.DynamicMap(mem_stack, streams=[mem_stream]).opts(
    opts.Area(height=400, width=400, ylim=(0, 100), framewise=True)
)


# Create PeriodicCallback which run every 500 milliseconds
def cb():
    cpu_stream.send(get_cpu_data())
    mem_stream.send(get_mem_data())

callback = pn.io.PeriodicCallback(callback=cb, period=500)
callback.start()

#serve dashboard
tmpl.add_panel('A', cpu_dmap)
tmpl.add_panel('B', mem_dmap)
tmpl.servable()