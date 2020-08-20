import dotenv
import os
import tweepy
import spacy
from sklearn.decomposition import LatentDirichletAllocation, NMF
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from spacymoji import Emoji


dotenv.load_dotenv(dotenv.find_dotenv())

nlp = spacy.load("en_core_web_sm")
emoji = Emoji(nlp)
nlp.add_pipe(emoji)

def get_raw_data(username, n_tweets):
    auth = tweepy.OAuthHandler(os.getenv('TWITTER_API_KEY'), os.getenv('TWITTER_API_SECRET_KEY'))
    auth.set_access_token(os.getenv('TWITTER_ACCESS_TOKEN'), os.getenv('TWITTER_ACCESS_SECRET'))
    api = tweepy.API(auth)
    return api.user_timeline(username, count=n_tweets)


def clean_tweet(text):
    doc = nlp(text)
    token_list = [token for token in doc if (not token.like_url) and (not token.is_punct) and (not token.is_stop) and (not token._.is_emoji)]
    filtered_sentence = [token.lemma_.replace('\n','').replace('RT','').replace('@','').replace(u"\u2018", "").replace(u"\u2019", "") for token in token_list]
    return(" ".join(filtered_sentence))


def return_data_type(raw_data, return_type):
    if return_type == 'raw':
        return {i._json['id_str']: i._json for i in raw_data}
    tweet_text_list = [clean_tweet(i._json['text']) for i in raw_data if not i.retweeted]
    if return_type == 'clean_list':
        return {'data': tweet_text_list}
    if return_type == 'clean_text':
        return {'data': " ".join(tweet_text_list)}


def model_data(tweet_text_list, no_topics=5, no_features=100, no_top_words=10):

    # NMF is able to use tf-idf
    tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words='english')
    tfidf = tfidf_vectorizer.fit_transform(tweet_text_list)
    nmf = NMF(n_components=no_topics, random_state=1, alpha=.1, l1_ratio=.5, init='nndsvd').fit(tfidf)
    tfidf_feature_names = tfidf_vectorizer.get_feature_names()

    # # LDA can only use raw term counts for LDA because it is a probabilistic graphical model
    # tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words='english')
    # tf = tf_vectorizer.fit_transform(tweet_text_list)
    # tf_feature_names = tf_vectorizer.get_feature_names()
    # lda = LatentDirichletAllocation(n_components=no_topics, max_iter=5, learning_method='online', learning_offset=50.,
    #                                 random_state=0).fit(tf)

    return {'model': nmf, 'feature_names': tfidf, 'no_top_words': no_top_words}

    # return {
    #     'nmf': nmf,
    #     'nmf_feature_names': tfidf_feature_names,
    #     'lda': lda,
    #     'lda_feature_names': tf_feature_names
    # }

def display_topics(model):
    return {
        f"{topic_idx}": " ".join(
            [
                model['feature_names'][i]
                for i in topic.argsort()[: -model['no_top_words'] - 1 : -1]
            ]
        )
        for topic_idx, topic in enumerate(model['model'].components_)
    }






