import tweepy as tw
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

# Creating the authentication object
auth = tw.OAuthHandler(os.getenv('twitter_consumer_key'), os.getenv('twitter_consumer_secret'))
# Setting your access token and secret
auth.set_access_token(os.getenv('twitter_access_token'), os.getenv('twitter_access_token_secret'))
# Creating the API object while passing in auth information
api = tw.API(auth)

search_words = "#bitcoin"
date_since = "2020-02-06"

tweets = tw.Cursor(api.search,
              q=search_words,
              lang="en",
              since=date_since).items(50)

for tweet in tweets:
    print(tweet.text)




