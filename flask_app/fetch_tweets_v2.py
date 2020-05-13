import tweepy as tw
import pandas as pd
import os
import json
from twython import Twython
import re
import pathlib
import argparse
import warnings
from pathlib import Path
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize, word_tokenize, TweetTokenizer

# auth.py import
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret)

# Tweeter port
twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret)

# Read json-file & remove link functions


def read_json(json_file):
    with open(json_file) as file:
        list = json.load(file)
    file.close()
    print(type(list))
    return list


def remove_links(text):
    urls = re.finditer('http\S+', text)
    for i in urls:
        try:
            text = re.sub(i.group().strip(), '', text)
        except:
            pass
    return (text)

# text normalization


class NormalizeText():
    def remove_special(s):
        SPECIAL_CHARS = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ü': 'u',
                         'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U'}
        for char in SPECIAL_CHARS:
            s = s.replace(char, SPECIAL_CHARS[char])
        return s

    def to_lowercase(s):
        s = s.casefold()
        return s

    def remove_flags(s):
        FLAGS = {'RT': ''}
        for flag in FLAGS:
            s = s.replace(flag, FLAGS[flag])
        return s

    def remove_nonascii(s):
        s = re.sub(r'[^\x00-\x7f]', r'', s)
        return s


# # Search words
# user = "selenagomez"
# # date_since = "2020-04-06"
# count = "20"

# print("datatypes")
# print(type(count))


# try:
#     search_details = twitter.search(q=search_words)
# except:
#     print('Nothing found!')
#     exit()

# if len(search_details) == 0:
#     print('Nothing found!')
#     exit(0)

# print('Downloading {} tweet(s) of:'.format(count))
# print('id: {} | name: {} | screen name: {} | Tweets: {} | Followers: {}'.format(
#     search_details[0]['id'],
#     search_details[0]['name'],
#     search_details[0]['screen_name'],
#     search_details[0]['statuses_count'],
#     search_details[0]['followers_count']))
# print('\n')

#############################################################################

# Fetch tweets with parameters
def search_user(user, count):

    try:
        user_timeline = twitter.get_user_timeline(screen_name=user,
                                                  count=count,
                                                  tweet_mode='extended')
        print('Tweets succesfully retrieved!')
    except:
        raise ValueError('Tweets could not be retrived!')

    ################################################################################
    # tweets = tw.Cursor(api.search,
    #                    q=search_words,
    #                    lang="en",
    #                    since=date_since).items(50)

    # Create JSON-file from tweets
    print('Creating JSON file...')
    filename = user+'.json'

    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(user_timeline, file, sort_keys=True, indent=4)

    print('{} created'.format(filename))

    print(type(filename))
    tweet_file = filename

    # Read JSON-file
    print("Reading the file...")
    tweets_2 = read_json(tweet_file)
    print(type(tweets_2))
    # tweets_2.items()
    print(type(tweets_2))

    # initialize tweeter tokenizer
    tTokenizer = TweetTokenizer()

    # initialize NLTK sentiment analyzer
    sid = SentimentIntensityAnalyzer()

    # initialize cumulator for avg.
    tss1 = 0.0
    tss2 = 0.0

    # Sentiment analysis
    print("Analyzing...")

    print("""--------------------------------------------------------------------------------------------------------------------------------
    TextBlob | NLTK  |                                    Tweet text                            | Sentences | Words  | Unique Words
    --------------------------------------------------------------------------------------------------------------------------------""")

    for tweet in tweets_2:
        # get text from tweets
        if tweet['truncated']:
            line = tweet['extended_tweet']['full_text']
        elif 'text' in tweet:
            line = tweet['text']
        else:
            line = tweet['full_text']

        # delete Leading & trailing characters
        line = line.strip()
        # Remove links
        line = remove_links(line)

        # Remove new line
        line = line.replace('\n', ' ')

        # Remove Non-ascii
        line = NormalizeText.remove_nonascii(line)

        # Tokenize text
        tweet_sent = sent_tokenize(line)   # Tokenize sentences
        tweet_word = tTokenizer.tokenize(line)
        tweet_unique = list(set(tweet_word))  # Eliminate duplicated words

        # Analyse sentiment
        ss1 = TextBlob(line)
        ss2 = sid.polarity_scores(line)

        # Update Cumulators
        tss1 += ss1.sentiment.polarity
        tss2 += ss2['compound']

        # Add updates to the JSON-file
        tweet.update(
            {'sentiment': {'textblob': ss1.sentiment.polarity, 'nltk': ss2['compound']}})

        # Show results
        print('{:8.2f} | {:5.2f} | {:72.72} | {:9d} | {:6d} | {:12d}'.format(
            ss1.sentiment.polarity,
            ss2['compound'],
            line,
            len(tweet_sent),
            len(tweet_word),
            len(tweet_unique)
        ))

    print('\n-------------------------')
    print('Sentiment analysis summary:')
    print('TextBlob Average {:.2f}'.format(tss1/len(tweets_2)))
    print('NLTK Average {:.2f}'.format(tss2/len(tweets_2)))

    # Update JSON file
    print('\n')
    print('*****************')
    print('Updating JSON file...')
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(tweets_2, file, sort_keys=True, indent=4)
    print('File {} updated. Process complete!'.format(filename))
    return tweets_2
    file.close()
    # for tweet in tweets:
    #     print(tweet.text)
