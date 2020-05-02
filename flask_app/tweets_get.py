from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret)
from twython import Twython
import re
import json
import argparse
import warnings
import argparse
import warnings
import json
import re
from pathlib import Path
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize, word_tokenize, TweetTokenizer


def sentiment_analysis():

    # Get Twitter authentication credentials

    #############
    # Functions
    #############

    #############
    # Constants
    #############
    # These constants control the behavior the this routine. Change them accordingly.
    MIN_TWEETS = 10         # Number of tweets to download in not specified in command line
    PRINT_OUT = False        # Display retrieved tweets?

    #############
    # Main Loop
    #############

    print('\n')
    print('***************************')
    print('*    Twitter Download     *')
    print('***************************')
    print('\n')

    # # construct the command line argument parser and parse the arguments
    # ap = argparse.ArgumentParser()
    # ap.add_argument('-u', '--user', required=True,
    #                 help='usage: python tweets_get.py --user <user> --count <tweet_count>')
    # ap.add_argument('-c', '--count', required=False)
    # args = vars(ap.parse_args())
    # warnings.filterwarnings("ignore")

    # # unpack command line arguments
    # user = args["user"].lower()
    # count = args['count']

    user = "realdonaldtrump"
    count = "10"

    print("datatypes")
    print(type(user))
    print(type(count))
    # Validate number of tweets to get
    if count == None:
        count = MIN_TWEETS
    elif not (count.isdigit()):
        count = MIN_TWEETS
    count = int(count)

    # Initialize tweeter port
    twitter = Twython(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret)

    # # Validate user name
    # user_details = []
    # try:
    #     user_details = twitter.lookup_user(screen_name=user)
    # except:
    #     print('[ERROR] User name not found in twitter!')
    #     exit()

    # if len(user_details) == 0:
    #     print('[ERROR] User name not found in twitter!')
    #     exit(0)

    # # Validate user has enough tweets to download
    # if count > 200:
    #     print('[WARNING] Tweet count cannot be greater that 200. Adjusting...')
    #     count = 200
    # if user_details[0]['statuses_count'] < count:
    #     print('[WARNING] User does not have enough tweets, Adjusting...')
    #     count = user_details[0]['statuses_count']

    # print('Downloading {} tweet(s) of:'.format(count))
    # print('id: {} | name: {} | screen name: {} | Tweets: {} | Followers: {}'.format(
    #     user_details[0]['id'],
    #     user_details[0]['name'],
    #     user_details[0]['screen_name'],
    #     user_details[0]['statuses_count'],
    #     user_details[0]['followers_count']))
    # print('\n')

    # Get user timeline
    try:
        user_timeline = twitter.get_user_timeline(screen_name=user,
                                                  count=count,
                                                  tweet_mode='extended')
        print('Tweets succesfully retrieved!')
    except:
        raise ValueError('Tweets could not be retrived!')

    # Display retrieved tweets
    # if PRINT_OUT:
    #     print('\n')
    #     for tweet in user_timeline:
    #         print('...{} | {}... |'.format(
    #             tweet['id_str'][-4:],
    #             tweet['full_text'][0:90].replace('\n', ' ')
    #         ))
    #     print('\n')

    # Save tweets to JSON file
    print('Creating JSON file...')
    filename = user+'.json'

    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(user_timeline, file, sort_keys=True, indent=4)

    print('File {} created. Process complete!'.format(filename))

    def read_json(json_file):
        with open(json_file) as file:
            list = json.load(file)
        file.close()
        return list

    def remove_links(text):
        urls = re.finditer('http\S+', text)
        for i in urls:
            try:
                text = re.sub(i.group().strip(), '', text)
            except:
                pass
        return (text)

    #############
    # Constants
    #############

    # These constants control the behavior the this routine. Change them accordingly.
    PRINT_OUT = True       # True if tweets should be display when processed
    UPDATE_FILE = True     # True if JSON file is updated with sentiment calculation
    FILE_ENCODING = 'utf-8'

    #############
    # Classes
    #############

    class NormalizeText():
        def remove_special(s):
            # Special characters dictionary
            SPECIAL_CHARS = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ü': 'u',
                             'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U'}
            for char in SPECIAL_CHARS:
                s = s.replace(char, SPECIAL_CHARS[char])
            return s

        def to_lowercase(s):
            # Convert text to lowercase
            s = s.casefold()
            return s

        def remove_flags(s):
            # Flags dictionary
            FLAGS = {'RT': ''}
            for flag in FLAGS:
                s = s.replace(flag, FLAGS[flag])
            return s

        def remove_nonascii(s):
            s = re.sub(r'[^\x00-\x7f]', r'', s)
            return s

    #############
    # Main Loop
    #############

    # # construct the command line argument parser and parse the arguments
    # ap = argparse.ArgumentParser()
    # ap.add_argument('-f', '--file', required=True,
    #                 help='usage: python tweets_sentiment.py --file <file>')
    # args = vars(ap.parse_args())
    # warnings.filterwarnings("ignore")

    # # unpack command line arguments
    # tweet_file = args['file']
    tweet_file = filename
    # Validate file exists
    file_check = Path(tweet_file)
    if not(file_check.is_file()):
        # file does not exist
        print('[Error] File does not exist.')
        exit()

    # Read the tweets file
    print('Reading tweets file...')
    print(type(tweet_file))
    tweets = read_json(tweet_file)
    print(type(tweets))
    # Initalize tweeter tokenizer
    tTokenizer = TweetTokenizer()

    # Initialize NLTK sentiment analyzer
    sid = SentimentIntensityAnalyzer()

    # Initialize cumulators for mean calculation
    tss1 = 0.0
    tss2 = 0.0

    # Analyze tweet sentiment
    print('Analyzing tweet sentiment...')
    print(type(tweets))

    if PRINT_OUT:
        print('--------------------------------------------------------------------------------------------------------------------------------')
        print('TextBlob | NLTK  |                                    Tweet text                            | Sentences | Words  | Unique Words')
        print('--------------------------------------------------------------------------------------------------------------------------------')

    for tweet in tweets:
        # get text from tweet
        print(type(tweets))
        if tweet['truncated']:
            line = tweet['extended_tweet']['full_text']
        elif 'text' in tweet:
            line = tweet['text']
        else:
            line = tweet['full_text']

        # Remove leading and trailing spaces
        line = line.strip()
        # Remove links
        line = remove_links(line)

        # Eliminate new lines
        line = line.replace('\n', ' ')

        # Remove non-ascii characters
        line = NormalizeText.remove_nonascii(line)

        # Tokenize text
        tweet_sent = sent_tokenize(line)   # Tokenize sentences
        tweet_word = tTokenizer.tokenize(line)
        tweet_unique = list(set(tweet_word))  # Eliminate duplicated words

        # Analyse sentiment
        ss1 = TextBlob(line)
        ss2 = sid.polarity_scores(line)

        # Update cumulators
        tss1 += ss1.sentiment.polarity
        tss2 += ss2['compound']

        # Add sentiment results to the JSON
        if UPDATE_FILE:
            tweet.update(
                {'sentiment': {'textblob': ss1.sentiment.polarity, 'nltk': ss2['compound']}})

        # Display results
        if PRINT_OUT:
            print('{:8.2f} | {:5.2f} | {:72.72} | {:9d} | {:6d} | {:12d}'.format(
                ss1.sentiment.polarity,
                ss2['compound'],
                line,
                len(tweet_sent),
                len(tweet_word),
                len(tweet_unique)
            ))
        return (print('\n-------------------------'),
                print('Sentiment analysis summary:'),
                print('TextBlob Average {:.2f}'.format(tss1/len(tweets))),
                print('NLTK Average {:.2f}'.format(tss2/len(tweets))),
                print(type(tweet)))
