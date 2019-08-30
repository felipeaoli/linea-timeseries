# app.py
#        bokeh serve --show timeseries.py
import numpy as np
from numpy.random import random

from bokeh.io import curdoc
from bokeh.layouts import row, column, widgetbox
from bokeh.models import ColumnDataSource, Spacer, HoverTool
from bokeh.models.widgets import Div, Select, Slider
from bokeh.plotting import Figure
from bokeh.io import output_notebook, show

# ====================
# Creating  fake data 

f = 1/13.
time = np.arange(0,100,1)
ndata = time.shape[0]
ptest = 1. # initial ptest
ph = ( time / ptest ) % 1
print (ph[:4],  "ph")

d1 = 0.5* np.sin( 2.0* np.pi* (f* time +0.25))\
        + .0*np.random.normal(0,0.1, ndata)
d2 = 0.5* np.sin( 2.0* np.pi* (f* time +0.25))\
        + .5*np.random.normal(0,0.1, ndata)
d3 = 0.5* np.sin( 2.0* np.pi* (f* time +0.25))\
        + 10.*np.random.normal(0,0.1, ndata)
d4 = 0.5* np.sin( 2.0* np.pi* (f* time +0.25))\
        + .2* np.sin( 2.0* np.pi* (f* time +0.33))

data_model=dict(
        time=time, 
        ph = ph, 
        noise1 = d1,
        noise2 = d2,
        noise3 = d3,
        noise4 = d4,)


# Column Data Source are the nice way to pass data to bokeh!
source = ColumnDataSource(data=dict(
        x=data_model['ph'],
        y=data_model['noise1'], 
        time=data_model['time']
        ))



# ===============
# Style session:

frame_title ="""<div><p align="center" style="font-size: 40px;"> 
                        Find Period</p></div>"""

def style(p):
    # Title 
    p.title.align = 'center'
    p.title.text_font_size = '20pt'
    p.title.text_font = 'serif'

    # Axis titles
    p.xaxis.axis_label_text_font_size = '14pt'
    p.xaxis.axis_label_text_font_style = 'bold'
    p.yaxis.axis_label_text_font_size = '14pt'
    p.yaxis.axis_label_text_font_style = 'bold'

    # Tick labels
    p.xaxis.major_label_text_font_size = '12pt'
    p.yaxis.major_label_text_font_size = '12pt'
    p.xaxis.ticker = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    return p

fiber_tooltip = """
            <div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">time (time_scale): </span>
                    <span style="font-size: 13px; color: #515151">@x</span>
                </div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">y: </span>
                    <span style="font-size: 13px; color: #515151;">@y</span>
                </div>
            </div>
        """

hover = HoverTool(tooltips=fiber_tooltip)



# ==================
# Bokeh plot itself:

plot = Figure(title='', 
            plot_width=900, 
            plot_height=300,
            toolbar_location='above',
            x_axis_label='Ph (some scale)',
            y_axis_label='Data (1)',
            tools=[hover,'pan,wheel_zoom,box_select,reset'],
            x_range=(-0.05,1.05))

q = plot.circle('x', 'y', source=source, size= 8,
             fill_alpha=0.2,
             color='red', 
             hover_fill_color='blue', line_color='black')

qa_options =  ["noise%s"%i for i in list(range(1,5)) ] 

label_dict =  dict( zip( qa_options[:],
            ["Data (%s)"%i for i in list(range(1,5)) ]
            ))



# =================
# Callback session:

select_y = Select(title="", value="noise1", options= qa_options) 

plot = style(plot)

def update_y(attrname, old, new):
    source.data['y'] = data_model[select_y.value]
    plot.yaxis.axis_label = label_dict[select_y.value]

select_y.on_change('value', update_y)


range_select = Slider(  start = 1,  # bar range
                        end   = 20, # bar range
                        value = 1., # values of the bar
                        step  = 0.2, 
                        title = 'ph_test (some scale)')

# Update function that accounts for all 3 controls
def update(attr, old, new):   
    ph_test = float(range_select.value)
    ph = (time/float(ph_test))%1

    # Update the data on the plot
    source.data['x'] = ph
    source.data['y'] = np.array(data_model[select_y.value])
        


# Update the plot with new value
range_select.on_change('value', update)


# ==============================
# Creating the exhibition layout
layout =  column( row(  widgetbox(Div(text=frame_title), width=300, height=100), 
                        column( widgetbox(select_y), widgetbox(range_select)) ),
                 plot )

curdoc().add_root(layout)
