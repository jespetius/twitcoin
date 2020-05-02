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

# JSON luku ja Linkkien poisto funktiot


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

# Tekstin normalisointi


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


# Hakusanat
search_words = "football"
# date_since = "2020-04-06"
count = "10"

print("datatypes")
print(type(count))
print(type(search_words))

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

# Haetaan twiittejä parametreillä
try:
    tweets = twitter.search(
        q=search_words,
        count=count,
        # since=date_since,
        tweet_mode='extended'
    )
    print("Tweets succesfully retrieved!")
except:
    raise ValueError('Tweets could not be retrieved!')


# tweets = tw.Cursor(api.search,
#                    q=search_words,
#                    lang="en",
#                    since=date_since).items(50)

# Luodaan twiiteistä JSON-tiedosto
print('Creating JSON file...')
filename = search_words+'.json'

with open(filename, 'w', encoding='utf-8') as file:
    json.dump(tweets, file, sort_keys=True, indent=4)

print('{} created'.format(filename))


print(type(filename))
tweet_file = filename

# Luetaan JSON-tiedosto
print("Reading the file...")
tweets_2 = read_json(tweet_file)
print(type(tweets_2))
tweets_2.items()
print(type(tweets_2))

# Alustetaan tweeter tokenizer
tTokenizer = TweetTokenizer()

# Alustetaan NLTK sentiment analyzer
sid = SentimentIntensityAnalyzer()

# Alustetaan kumulaattorit keskiarvon laskemiseen
tss1 = 0.0
tss2 = 0.0

# Sentiment analysis
print("Analyzing...")

print("""--------------------------------------------------------------------------------------------------------------------------------
TextBlob | NLTK  |                                    Tweet text                            | Sentences | Words  | Unique Words
--------------------------------------------------------------------------------------------------------------------------------""")


for tweet in tweets_2:
    # haetaan texti twiiteistä
    if tweet['truncated']:
        line = tweet['extended_tweet']['full_text']
    elif 'text' in tweet:
        line = tweet['text']
    else:
        line = tweet['full_text']

    # Leading ja trailing kirjaimien poisto
    line = line.strip()
    # Linkkien poisto
    line = remove_links(line)

    # New line poisto
    line = line.replace('\n', ' ')

    # Non-ascii poisto
    line = NormalizeText.remove_nonascii(line)

    # Tokenize text
    tweet_sent = sent_tokenize(line)   # Tokenize sentences
    tweet_word = tTokenizer.tokenize(line)
    tweet_unique = list(set(tweet_word))  # Eliminate duplicated words

    # Analyse sentiment
    ss1 = TextBlob(line)
    ss2 = sid.polarity_scores(line)

    # Kumulaattorien päivitys
    tss1 += ss1.sentiment.polarity
    tss2 += ss2['compound']

    # lisätään tulokset JSON-tiedostoon
    tweet.update(
        {'sentiment': {'textblob': ss1.sentiment.polarity, 'nltk': ss2['compound']}})

    # Näytetään tulokset
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

# Päivitetään JSON file
print('\n')
print('*****************')
print('Updating JSON file...')
with open(filename, 'w', encoding='utf-8') as file:
    json.dump(tweets_2, file, sort_keys=True, indent=4)
print('File {} updated. Process complete!'.format(filename))
file.close()
# for tweet in tweets:
#     print(tweet.text)
