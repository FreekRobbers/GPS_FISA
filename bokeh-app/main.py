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
from bokeh.models import DatetimeTickFormatter, FileInput
from bokeh.layouts import column
from bokeh.plotting import figure
from bokeh.palettes import Colorblind8

# World Records
def worldRecord(file):
    if 'PR1' in file: # PR = Para-rowing
        if 'ROWMSCULL1' in file:
            WR = datetime.timedelta(minutes=9,seconds=12.99) # PR1 M1x
        elif 'ROWWSCULL1' in file:
            WR = datetime.timedelta(minutes=10,seconds=13.63) # PR1 W1x
        else:
            WR = None
    elif 'PR2' in file:
        if 'ROWMSCULL1' in file:
            WR = datetime.timedelta(minutes=8,seconds=28.4) # PR2 M1x
        elif 'ROWWSCULL1' in file:
            WR = datetime.timedelta(minutes=9,seconds=24.99) # PR2 W1x
        elif 'ROWXSCULL2' in file:
            WR = datetime.timedelta(minutes=8,seconds=6.21) # PR2 MIX2x
        else:
            WR = None
    elif 'PR3' in file:
        if 'ROWWNOCOX2' in file:
            WR= datetime.timedelta(minutes=7,seconds=39.3) # PR3 W2-
        elif 'ROWXSCULL2' in file:
            WR = datetime.timedelta(minutes=7,seconds=28.95) # PR3 MIX2x
        elif 'ROWXCOXED4' in file:
            WR = datetime.timedelta(minutes=6,seconds=49.24) # PR3 MIX4+
        else:
            WR = None
    elif 'ROWWSCULL1-L' in file:
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
    elif 'ROWMSCULL2' in file:
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
    # function that converts speed to average 2k time:
    # speed: each sample represents real time speed (m/s)
    # to
    # avg2kTime: each sample represents average speed so far (2k time)
    avg2kTime = []
    try:
        avg2kTime.append(datetime.timedelta(seconds=2000/speed[0]))
    except:
        avg2kTime.append(float('nan'))
        print('Error at first sample')
    for i in range(len(speed)-1):
        try:
            avg2kTime.append(datetime.timedelta(seconds=2000/(speed[0:i+1]).mean()))
        except:
            avg2kTime.append(float('nan'))
            print('Error at sample ' + str(i+1))
    return avg2kTime

def timeToAvgTime(time,distance):
    # function that converts speed to average 2k time:
    # speed: each sample represents real time speed (m/s)
    # to
    # avg2kTime: each sample represents average speed so far (2k time)
    avg2kTime = []
    for i in range(len(time)):
        try:
            t = datetime.datetime.strptime(time[i],"%M:%S.%f")
            dt = datetime.timedelta(minutes=t.minute,seconds=t.second,milliseconds=t.microsecond/1000)
            avg2kTime.append((dt/distance[i])*2000)
        except:
            avg2kTime.append(float('nan'))
            print('Error at sample ' + str(i+1))
    return avg2kTime

def update_figure(fileName):
    # decode fileName
    decoded = base64.b64decode(fileName)
    file = io.BytesIO(decoded)
    # read excelfile
    data = pd.read_csv(file, delimiter=';')
    # reset figure
    p = figure(plot_height=600, plot_width=1200, y_axis_type='datetime', background_fill_color='#fafafa')
    nanstring = ''
    for column_name in data.columns:
        for i in range(7):
            if str(i) in column_name:
                if 'Name' in column_name:
                    country = data[column_name][1]
                elif 'Time' in column_name:
                    time2k = data[column_name].iloc[-1]
                    time = data[column_name]
                    t = datetime.datetime.strptime(time[0],"%M:%S.%f")
                    avg2kTime2 = timeToAvgTime(time,data.Distance.values)
                elif 'Speed' in column_name:
                    speed = data[column_name]
                    if pd.isna(speed).any():
                        speed = speed.fillna(method='ffill')
                        nanstring = ' - NaN detected'
                    avg2kTime = speedToAvgTime(speed)
                    try:
                        # draw circles
                        p.circle(x=data.Distance.values, y=avg2kTime2, legend_label=(str(time2k)[0:7] + ' ' + country), color=Colorblind8[i])
                    except:
                        print('Draw figure failed')

    # add world best time
    WR = worldRecord(file_input.filename)
    if WR is not None:
        p.y_range.end = (WR + datetime.timedelta(minutes=1))
        p.line(x=[0,2000], y=[WR,WR], line_color='black', line_alpha=0.7, line_dash='dashed', line_width=2, legend_label= str(WR)[2:9] + ' WR')
    else:
        print('No WR found')

    fig = figure_layout(p, nanstring)
    return fig

def figure_layout(p, nanstring):
    p.title.text = file_input.filename + nanstring
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
