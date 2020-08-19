import os
import time
import logging

import dotenv
import pandas as pd
import tweepy


class MyStreamListener(tweepy.StreamListener):

    def setup(self):
        self.iteration = 1
        self.batch = 1
        self.stored_data = []


    def on_status(self, status):

        data = status._json

        id_str = data['id_str']
        created_at = data['created_at']
        retweets = data['retweet_count']
        description = data['user']['description']
        text = data['text']
        screen_name = data['user']['screen_name']
        user_created = data['user']['created_at']
        followers = data['user']['followers_count']

        df = pd.DataFrame({
            'id_str': [id_str],
            'created_at': created_at,
            'retweets': retweets,
            'description': description,
            'text': text,
            'screen_name': screen_name,
            'user_created_at': user_created,
            'followers': followers
        })

        self.stored_data.append(df)
        self.batch += 1

        if self.batch % 50 == 0:
            print(f"Iteration: {self.iteration}")
            to_write = pd.concat(self.stored_data)
            to_write.to_csv(f"twitter_topic_modeling/data/raw/demconvention/{self.iteration}.csv")
            self.stored_data = []
            self.batch = 1
            self.iteration += 1
            time.sleep(1)




def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('Starting to gather Twitter data.')

    logger.info("Authenticating Twitter:")
    auth = tweepy.OAuthHandler(os.getenv('TWITTER_API_KEY'), os.getenv('TWITTER_API_SECRET_KEY'))
    auth.set_access_token(os.getenv('TWITTER_ACCESS_TOKEN'), os.getenv('TWITTER_ACCESS_SECRET'))
    api = tweepy.API(auth)

    myStreamListener = MyStreamListener()
    myStreamListener.setup()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

    #myStream.sample()
    myStream.filter(track=['demconvention'])




if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    dotenv.load_dotenv(dotenv.find_dotenv())
    main()
