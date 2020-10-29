# -*- coding: utf-8 -*-
"""
Created on Sun Oct  25 13:35:13 2020

@author: freek
"""
import pandas as pd

import statistics
import datetime
import base64
import io

from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, Range1d, Span, FileInput
from bokeh.plotting import figure
from bokeh.palettes import Colorblind8

from functions import speedToAvgTime
from worldRecords import worldRecord

def update_figure(fileName):
    decoded = base64.b64decode(fileName)
    file = io.BytesIO(decoded)
    # read excelfile
    data = pd.read_csv(file, delimiter=';')
    # draw figure
    p = figure(plot_height=800, plot_width=1400, y_axis_type='datetime', background_fill_color='#fafafa')
    for column_name in data.columns:
        for i in range(7):
            if str(i) in column_name:
                if 'Name' in column_name:
                    country = data[column_name][1]
                elif 'Time' in column_name:
                    time2k = data[column_name].iloc[-1]
                elif 'Speed' in column_name:
                    speed = data[column_name].values
                    avg2kTime = speedToAvgTime(speed)
                    time = str(time2k)
                    p.circle(x=data.Distance.values, y=avg2kTime, legend_label=(str(time2k)[0:7] + ' ' + country), color=Colorblind8[i])

    # add world best time
    WR = worldRecord(file_input.filename)
    try:
        p.y_range.end = (WR + datetime.timedelta(minutes=1))
        p.line(x=[0,2000], y=[WR,WR], line_color='black', line_alpha=0.7, line_dash='dashed', line_width=2, legend_label= str(WR)[2:9] + ' WR')
    except:
        print('No WR found')

    fig = figure_layout(p)
    return fig

def figure_layout(p):
    p.title.text = file_input.filename
    p.legend.click_policy = 'hide'
    p.xaxis.axis_label = 'Afstand (m)'
    p.yaxis.axis_label = 'Gemiddelde snelheid (2k tijd)'
    p.yaxis.formatter = DatetimeTickFormatter(seconds=['%M:%S'], minutes=['%M:%S'])
    return p

def update(attr, old, new):
    layout.children[1] = update_figure(new)

# file button
file_input = FileInput(accept='.csv', multiple=False, margin=[5,5,5,65])
file_input.on_change('value', update)

layout = column(file_input, figure(plot_height=800, plot_width=1400))
curdoc().add_root(layout)
curdoc().title = "GPS FISA"
