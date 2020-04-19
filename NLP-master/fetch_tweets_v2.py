import tweepy as tw
import pandas as pd
import os
import json
from twython import Twython
import re
import argparse
import warnings


# auth.py import

from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret)


def remove_regex(input_text, regex_pattern):
    # Remove a regular expression (regex) from a string
    urls = re.finditer(regex_pattern, input_text)
    for i in urls:
        try:
            input_text = re.sub(i.group().strip(), '', input_text)
        except:
            print('Regex exception')

    return input_text


twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret)


# Hakusanat
search_words = "wrghwrhhhwhwrhhfhf"
date_since = "2020-04-06"
count = 10

try:
    search_details = twitter.search(q=search_words)
except:
    print('Nothing found!')
    exit()

if len(search_details) == 0:
    print('Nothing found!')
    exit(0)

print('Downloading {} tweet(s) of:'.format(count))
print('id: {} | name: {} | screen name: {} | Tweets: {} | Followers: {}'.format(
    search_details[0]['id'],
    search_details[0]['name'],
    search_details[0]['screen_name'],
    search_details[0]['statuses_count'],
    search_details[0]['followers_count']))
print('\n')

try:
    tweets = twitter.search(
        q=search_words,
        count=count,
        since=date_since,
        tweet_mode='extended'
    )
    print("Tweets succesfully retrieved!")
except:
    raise ValueError('Tweets could not be retrieved!')


# tweets = tw.Cursor(api.search,
#                    q=search_words,
#                    lang="en",
#                    since=date_since).items(50)


print('Creating JSON file...')
filename = search_words+'.json'

with open(filename, 'w', encoding='utf-8') as file:
    json.dump(tweets, file, sort_keys=True, indent=4)

print(f'{filename} created')

# for tweet in tweets:
#     print(tweet.text)
