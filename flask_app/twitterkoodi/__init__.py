import json
import urllib.request
import os
from flask import Flask, request, jsonify, render_template
import requests
from flask_restful import Resource, Api
from twython import Twython
from dotenv import load_dotenv
load_dotenv()
import tweepy as tw
import pandas as pd

app = Flask(__name__)
api = Api(app)


class bitcoin(Resource):
    def get(self):
        json_url = urllib.request.urlopen(
    "https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=BTC,USD,EUR&api_key=os.getenv('cryptocompare_api_key')")
        data = json.loads(json_url.read())
        return {'kurssit': data}


#testing
class Testi(Resource):
    def get(self):
        return {'about':'Testi'}

    def post(self):
        some_json = request.get_json()
        return {'you sent': some_json}, 201

class Tweets(Resource):
    def get(self):
        # Tunnistusobjektin luominen
        auth = tw.OAuthHandler(os.getenv('twitter_consumer_key'),
                       os.getenv('twitter_consumer_secret'))
        # Access tokenien asettaminen
        auth.set_access_token(os.getenv('twitter_access_token'),
                      os.getenv('twitter_access_token_secret'))
        # API-objektin luominen ja auth informaation puskeminen
        api = tw.API(auth)

        user = api.get_user('realdonaldtrump')
        return {'userscreenname': user.screen_name}      
        




api.add_resource(bitcoin, '/bitcoin')
api.add_resource(Testi, '/testi')
api.add_resource(Tweets, '/tweets')