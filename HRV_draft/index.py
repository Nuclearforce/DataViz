#this is the home page for the dashboard multi page app. 
from jinja2 import Environment, FileSystemLoader
import panel as pn

#loads custom bootstrap template
env = Environment(loader=FileSystemLoader('.'))
jinja_template = env.get_template('/templates/index.html')

tmpl = pn.Template(jinja_template)

tmpl.servable()