import tweepy as tw
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

# Tunnistusobjektin luominen
auth = tw.OAuthHandler(os.getenv('twitter_consumer_key'),
                       os.getenv('twitter_consumer_secret'))
# Access tokenien asettaminen
auth.set_access_token(os.getenv('twitter_access_token'),
                      os.getenv('twitter_access_token_secret'))
# API-objektin luominen ja auth informaation puskeminen
api = tw.API(auth)

# Hakusanat
search_words = "#bitcoin"
date_since = "2020-02-06"

tweets = tw.Cursor(api.search,
                   q=search_words,
                   lang="en",
                   since=date_since).items(50)

for tweet in tweets:
    print(tweet.text)
