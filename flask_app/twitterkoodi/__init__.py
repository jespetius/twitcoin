import json
import urllib.request
import os
from flask import Flask, request, jsonify, render_template
import requests
from flask_restful import Resource, Api
from twython import Twython
#from dotenv import load_dotenv
#load_dotenv()
app = Flask(__name__)
api = Api(app)

#from auth import consumer_key, consumer_secret, access_token, access_token_secret

class bitcoin(Resource):
    def get(self):
        json_url = urllib.request.urlopen(
    "https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=BTC,USD,EUR&api_key=os.getenv('cryptocompare_api_key')")
        data = json.loads(json_url.read())
        return {'kurssit': data}

#class tweets(Resource):
#    def get(self):
#        twitter = Twython(
#        consumer_key,
#        consumer_secret,
#        access_token,
#        access_token_secret)
#
#        search_words = "bitcoin"
#        date_since = "2020-04-06"
#        count = 10#
#
#        tweets = twitter.search(
#            q=search_words,
#            count=count,
#            since=date_since,
#           tweet_mode='extended'
#        )
#
#        for tweet in tweets:
#              tweet = tweet.json
#        return {tweet}   


api.add_resource(bitcoin, '/bitcoin')
#api.add_resource(tweets, '/tweets')