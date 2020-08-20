import os
import logging
from flask import Flask
import plotly.express as px
import pandas as pd
import dotenv
from twitter_topic_modeling.models.model_topic import gather_and_model_data, display_topics

dotenv.load_dotenv(dotenv.find_dotenv())


# Instantiate an app
app = Flask(__name__)


logger = logging.getLogger(__name__)
logger.info('Starting to gather Twitter data.')
logger.info("Authenticating Twitter:")


@app.route('/')
def home():
    return 'This is the start of something great!'


@app.route('/<username>/<model_type>/<no_top_words>')
def user_tweet_topics(username='realDonaldTrump', model_type="nmf", no_top_words=5):
    model = gather_and_model_data(username)
    return display_topics(model[model_type], f"{model_type}_feature_names", no_top_words)



if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
