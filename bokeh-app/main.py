# -*- coding: utf-8 -*-
"""
Created on Sun Oct  25 13:35:13 2020

@author: freek
"""
import pandas as pd

import datetime
import base64
import io

from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, Range1d, Span, FileInput
from bokeh.plotting import figure
from bokeh.palettes import Colorblind8

# World Records
def worldRecord(file):
    if 'ROWWSCULL1-L' in file:
        WR = datetime.timedelta(minutes=7,seconds=24.46) # LW1x
    elif 'ROWWSCULL1' in file:
        WR = datetime.timedelta(minutes=7,seconds=7.71) # W1x
    elif 'ROWMSCULL1-L' in file:
        WR = datetime.timedelta(minutes=6,seconds=41.03) # LM1x
    elif 'ROWMSCULL1' in file:
        WR = datetime.timedelta(minutes=6,seconds=30.74) # M1x
    elif 'ROWWNOCOX2-L' in file:
        WR = datetime.timedelta(minutes=7,seconds=18.32) # LW2-
    elif 'ROWWNOCOX2' in file:
        WR = datetime.timedelta(minutes=6,seconds=49.08) # W2-
    elif 'ROWMNOCOX2-L' in file:
        WR = datetime.timedelta(minutes=6,seconds=22.91) # LM2-
    elif 'ROWMNOCOX2' in file:
        WR = datetime.timedelta(minutes=6,seconds=8.5) # M2-
    elif 'ROWMCOXED2' in file:
        WR = datetime.timedelta(minutes=6,seconds=33.26) # M2+
    elif 'ROWWSCULL2-L' in file:
        WR = datetime.timedelta(minutes=6,seconds=47.69) # LW2x
    elif 'ROWWSCULL2' in file:
        WR = datetime.timedelta(minutes=6,seconds=37.31) # W2x
    elif 'ROWMSCULL2-L' in file:
        WR = datetime.timedelta(minutes=6,seconds=5.36) # LM2x
    elif 'ROWMSCULL-2' in file:
        WR = datetime.timedelta(minutes=5,seconds=59.72) # M2x
    elif 'ROWWNOCOX4-L' in file:
        WR = datetime.timedelta(minutes=6,seconds=36.4) # LW4-
    elif 'ROWWNOCOX4' in file:
        WR = datetime.timedelta(minutes=6,seconds=14.36) # W4-
    elif 'ROWMNOCOX4-L' in file:
        WR = datetime.timedelta(minutes=5,seconds=43.16) # LM4-
    elif 'ROWMNOCOX4' in file:
        WR = datetime.timedelta(minutes=5,seconds=37.86) # M4-
    elif 'ROWMCOXED4' in file:
        WR = datetime.timedelta(minutes=5,seconds=58.96) # M4+
    elif 'ROWWCOXED4' in file:
        WR = datetime.timedelta(minutes=6,seconds=43.86) # W4+
    elif 'ROWMSCULL4-L' in file:
        WR = datetime.timedelta(minutes=5,seconds=42.75) # LM4x
    elif 'ROWMSCULL4' in file:
        WR = datetime.timedelta(minutes=5,seconds=32.26) # M4x
    elif 'ROWWSCULL4-L' in file:
        WR = datetime.timedelta(minutes=6,seconds=15.95) # LW4x
    elif 'ROWWSCULL4' in file:
        WR = datetime.timedelta(minutes=6,seconds=6.84) # W4x
    elif 'ROWMCOXED8-L' in file:
        WR = datetime.timedelta(minutes=5,seconds=30.24) # LM8+
    elif 'ROWMCOXED8' in file:
        WR = datetime.timedelta(minutes=5,seconds=18.68) # M8+
    elif 'ROWWCOXED8' in file:
        WR = datetime.timedelta(minutes=5,seconds=54.16) # W8+
    else:
        WR = None

    return WR

def speedToAvgTime(speed):
    avg2kTime = []
    try:
        avg2kTime.append(datetime.timedelta(seconds=2000/speed[0]))
    except:
        avg2kTime.append(0)
    for i in range(len(speed)-1):
        try:
            avg2kTime.append(datetime.timedelta(seconds=2000/speed[0:i+1].mean()))
        except:
            avg2kTime.append(0)
    return avg2kTime

def update_figure(fileName):
    decoded = base64.b64decode(fileName)
    file = io.BytesIO(decoded)
    # read excelfile
    data = pd.read_csv(file, delimiter=';')
    # draw figure
    p = figure(plot_height=600, plot_width=1200, y_axis_type='datetime', background_fill_color='#fafafa')
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

layout = column(file_input, figure(plot_height=600, plot_width=1200))
curdoc().add_root(layout)
curdoc().title = "GPS FISA"
