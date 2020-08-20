import os
import logging
from flask import Flask
import plotly.express as px
import pandas as pd
import dotenv
from twitter_topic_modeling.models.model_topic import get_raw_data, return_data_type, model_data, display_topics

dotenv.load_dotenv(dotenv.find_dotenv())


# Instantiate an app
app = Flask(__name__)


logger = logging.getLogger(__name__)
logger.info('Starting to gather Twitter data.')
logger.info("Authenticating Twitter:")


@app.route('/')
def home():
    return 'This is the start of something great!'


@app.route('/<username>/<n_tweets>/<return_type>')
def user_tweets(username, n_tweets, return_type):
    raw_data = get_raw_data(username, int(n_tweets))
    return return_data_type(raw_data, return_type)


@app.route('/topics/<username>')
def topics(username):
    raw_data = get_raw_data(username, 20)
    clean_tweet_list = return_data_type(raw_data, 'list')
    logger.warning(clean_tweet_list['data'])
    model = model_data(clean_tweet_list['data'])
    return display_topics(model)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
