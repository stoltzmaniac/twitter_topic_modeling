import os
from flask import Flask
import plotly.express as px
import pandas as pd


# Instantiate an app
app = Flask(__name__)


@app.route('/')
def home():
    return 'This is the start of something great!'


@app.route('/data/<tickername>')
def data(tickername):
    data = fetch_data(tickername)
    return data.reset_index().to_html()

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
