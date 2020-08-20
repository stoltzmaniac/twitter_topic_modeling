import os
import logging
from flask import Flask
import plotly.express as px
import pandas as pd
import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())


# Instantiate an app
app = Flask(__name__)


logger = logging.getLogger(__name__)
logger.info('Starting to gather Twitter data.')
logger.info("Authenticating Twitter:")


@app.route('/')
def home():
    return 'This is the start of something great!'



if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
