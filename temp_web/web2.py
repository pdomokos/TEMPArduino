#!flask/bin/python
from flask import Flask, jsonify, url_for, make_response, render_template, request, abort
import json
import datetime
import plotly
import plotly.graph_objs as go
import numpy as np
import subprocess
from collections import deque

app = Flask(__name__)

class RollingAverage:
    def __init__(self, max_size=60):
        self.queue = deque(maxlen=max_size)
    
    def add_number(self, num):
        self.queue.append(num)
        return self.calculate_average()
    
    def calculate_average(self):
        return sum(self.queue) / len(self.queue) if self.queue else 0

rolling_avg = RollingAverage()
rolling_avg2 = RollingAverage()
rolling_avg3 = RollingAverage()

@app.route('/showMultiChart')
def multiLine():
    # Extract data from file
    lists = getLastDay()
    xScale = lists[0]
    
    # Data for each graph
    dht_temp = lists[1]
    dht_hum = lists[2]
    t1 = lists[3]
    t2 = lists[4]
    pir1 = lists[5]

    # Create traces for each graph
    # Graph 1: DHT1_T and DHT1_H
    trace1 = go.Scatter(x=xScale, y=dht_temp, name='DHT1_T')
    trace2 = go.Scatter(x=xScale, y=dht_hum, name='DHT1_H')
    graph1_data = [trace1, trace2]
    graph1_json = json.dumps(graph1_data, cls=plotly.utils.PlotlyJSONEncoder)

    # Graph 2: T1 and T2
    trace3 = go.Scatter(x=xScale, y=t1, name='T1')
    trace4 = go.Scatter(x=xScale, y=t2, name='T2')
    graph2_data = [trace3, trace4]
    graph2_json = json.dumps(graph2_data, cls=plotly.utils.PlotlyJSONEncoder)

    # Graph 3: PIR1 Heatmap
    heatmap_data = go.Heatmap(
        z=[pir1],
        x=xScale,
        colorscale='Viridis',
        name='PIR1 Heatmap'
    )
    graph3_data = [heatmap_data]
    graph3_json = json.dumps(graph3_data, cls=plotly.utils.PlotlyJSONEncoder)

    # Render the template with all graphs
    return render_template('index.html', graphJSON=graph1_json, graphJSON2=graph2_json, graphJSON3=graph3_json)

def getLastDay():
    f = '../temp_data.txt'
    lines = tail(f, 8640)
    print(f"line size {len(lines)}")

    dates = []
    dht_temp = []
    dht_hum = []
    t1 = []
    t2 = []
    pir1 = []

    for line in lines:
        try:
            data = line.rstrip().decode("utf-8").split('#')
            dates.append(datetime.datetime.strptime(data[0], "%Y-%m-%d %H:%M:%S"))
            dht_temp.append(float(data[1].split(':')[1]))
            dht_hum.append(rolling_avg.add_number(float(data[2].split(':')[1])))
            t1.append(rolling_avg2.add_number(float(data[3].split(':')[1])))
            t2.append(rolling_avg3.add_number(float(data[4].split(':')[1])))
            pir1.append(float(data[5].split(':')[1]))
        except ValueError as e:
            print(f"Line: {line}")
            print(f"Error parsing line: {line.rstrip().decode('utf-8')}")
            print(f"Error details: {e}")
            continue

    return [dates, dht_temp, dht_hum, t1, t2, pir1]

def tail(f, n, offset=0):
    proc = subprocess.Popen(['tail', '-n', str(n + offset), f], stdout=subprocess.PIPE)
    lines = proc.stdout.readlines()
    #return lines[:, -offset]
    return lines

def tail2(f, n, offset=0):
    with open(f, 'rb') as file:
        file.seek(0, 2)  # Move to the end of the file
        file_size = file.tell()
        block_size = 1024
        blocks = []

        while file_size > 0 and len(blocks) < n + offset:
            file_size -= block_size
            file.seek(max(file_size, 0))
            blocks.extend(file.readlines())

        return blocks[-n:]

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(host= '192.168.0.143', port=9081, debug=True)


