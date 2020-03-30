import re
from textblob import TextBlob
import pandas as pd
import numpy as np
import tweepy
from IPython.display import display
import matplotlib.pyplot as plt


from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret)


def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


def analize_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1


class TwitterStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)
        print(status.user.profile_image_url_https)
        print(analize_sentiment(status.text))


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True,
                 retry_count=10, retry_delay=5, retry_errors=5)
streamListener = TwitterStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=streamListener)

myStream.filter(track=["trump"])
