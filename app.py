import os
import logging
from flask import Flask
import plotly.express as px
import pandas as pd
import dotenv
from twitter_topic_modeling.models.model_topic import get_raw_data, clean_tweet

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

    if return_type == 'json':
        return {i._json['id_str']: i._json for i in raw_data}

    tweet_text_list = [clean_tweet(i._json['text']) for i in raw_data if not i.retweeted]

    if return_type == 'list':
        return {'data': tweet_text_list}

    if return_type == 'text':
        return {'data': " ".join(tweet_text_list)}

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
