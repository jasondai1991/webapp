from flask import Flask, render_template, request
import os, json, datetime
from threading import Thread, Event
from datetime import datetime
import requests
from .loadRegister import LoadRegister

# Create application, and point static path (where static resources like images, css, and js files are stored) to the
# "static folder"
app = Flask(__name__,static_url_path="/static")


TIME_INTERVAL=10
TIME_DISPLAYED = 60*10
ERROR_INTERVAL = 60*2

lg = LoadRegister(TIME_INTERVAL, TIME_DISPLAYED, ERROR_INTERVAL)

# defining a class which runs in the background the gather datapoints
class MyThread(Thread):
    def __init__(self, interval_seconds, event):
        super().__init__()
        self.stop_event = Event()
        self.interval_seconds = interval_seconds
        self.callback = event

    def run(self):
        while not self.stop_event.wait(self.interval_seconds):
            self.callback()

    def stop(self):
        self.stop_event.set()

event = lg.add_datapoint
thread = MyThread(10, event)
thread.start()


@app.route('/', methods = ['GET'])
def main():
    error_messages = lg.get_messages()
    key_metrics = lg.key_metrics()
    return render_template("index.html", error_messages = error_messages, metrics = key_metrics)

@app.route('/stats')
def get_stats():
    stats_data = lg.get_stats()
    return json.dumps(stats_data)



