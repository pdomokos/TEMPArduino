#!flask/bin/python
from flask import Flask, jsonify, url_for, make_response, render_template, request, abort
import json
import datetime
import random
import plotly
import chart_studio.plotly as py
import plotly.graph_objs as go
import subprocess

import numpy as np
from collections import deque

app = Flask(__name__)

class RollingAverage:
    def __init__(self, max_size=60):
        self.queue = deque(maxlen=max_size)
    
    def add_number(self, num):
        self.queue.append(num)
        return self.calculate_average()
    
    def calculate_average(self):
        return sum(self.queue) / len(self.queue)
    
rolling_avg = RollingAverage()
rolling_avg2 = RollingAverage()

@app.route('/showMultiChart')
def multiLine():
    #count = 288
    #base = datetime.datetime.today()
    #xScale = [base - datetime.timedelta(minutes=x) for x in range(0,1440,5)]
    #y0_scale = getRandList(24.1,27.9,288)
    #y1_scale = getRandList(16.2,23.9,288)
    #y2_scale = getRandList(8.1,15.9,288)
    lists = getLastDay()
    xScale = lists[0]
    y0_scale = lists[1]
    y1_scale = lists[2]
    y2_scale = lists[3]
    y3_scale = lists[4]
    y4_scale = lists[5]
    y5_scale = lists[6]
    y6_scale = lists[7]
    y7_scale = lists[8] 	
    # Create traces
    trace1 = go.Scatter(
        x = xScale,
        y = y0_scale,
        name = 'sensor1'
    )
    trace2 = go.Scatter(
        x = xScale,
        y = y1_scale,
        name = 'sensor2'
    )
    trace3 = go.Scatter(
        x = xScale,
        y = y2_scale,
        name = 'sensor3'
    )
    trace4 = go.Scatter(
        x = xScale,
        y = y3_scale,
        name = 'sensor1'
    )
    trace5 = go.Scatter(
        x = xScale,
        y = y4_scale,
        name = 'sensor2'
    )
    trace6 = go.Scatter(
        x = xScale,
        y = y5_scale,
        name = 'sensor3'
    )
    trace7 = go.Scatter(
        x = xScale,
        y = y6_scale,
        name = 'term1'
    )
    trace8 = go.Scatter(
        x = xScale,
        y = y7_scale,
        name = 'term2'
    )
    data = [trace1, trace2, trace3]
    data2 = [trace4, trace5, trace6]
    data3 = [trace7, trace8]
    #data = [trace1, trace3]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(data2, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON3 = json.dumps(data3, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html',
                           graphJSON=graphJSON,graphJSON2=graphJSON2,graphJSON3=graphJSON3)

def getLastDay():
    #f = open("../temp_logger/temp_data.csv","r")
    f = '../temp_data.txt'
    #lines = tail(f, 288)
    lines = tail(f, 8640)
    #f.close()
    dates = []
    sensor1 = []
    sensor2 = []
    sensor3 = []
    sensor1T = []
    sensor2T = []
    sensor3T = []
    term1 = []
    term2 = []
    for line in lines:
        data = line.rstrip().decode("utf-8").split('#')
        dates.append(datetime.datetime.strptime(data[0], "%Y-%m-%d %H:%M:%S"))
        sensor1.append(data[2].split(':')[1])
        sensor2.append(data[4].split(':')[1])
        sensor3.append(data[6].split(':')[1])
        sensor1T.append(data[1].split(':')[1])
        sensor2T.append(data[3].split(':')[1])
        sensor3T.append(data[5].split(':')[1])
        term1.append(rolling_avg.add_number(float(data[7].split(':')[1])))
        term2.append(rolling_avg2.add_number(float(data[8].split(':')[1])))
    return [dates,sensor1,sensor2,sensor3,sensor1T,sensor2T,sensor3T,term1,term2]
    
def tail(f, n, offset=0):
    proc = subprocess.Popen(['tail', '-n', str(n + offset), f], stdout=subprocess.PIPE)
    lines = proc.stdout.readlines()
    #return lines[:, -offset]
    return lines

def getRandList(f,t,s):
	randomFloatList = []
	for i in range(0, s):
		x = round(random.uniform(f, t), 1)
		randomFloatList.append(x)
	return randomFloatList
	
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(host= '192.168.0.143', port=9081, debug=True)
