
# testaus pelkka flask
from flask import Flask, request, jsonify, render_template
from fetch_tweets_v2 import search_user
import requests
import cgi
app = Flask(__name__)
form = cgi.FieldStorage()

# json testi
@app.route('/json', methods=['GET', 'POST'])
def json():
    name = request.form.get("searchform")

    return jsonify(search_user(name, 50))

# user jsonina
@app.route('/user', methods=['POST'])
def user():
    user = request.form['userform']
    return jsonify({"key": user})


# @app.route('/search', methods=['POST'])
# def search():

#     # user_search = request.form['searchform']
#     # user_search = user
#     return sentiment_analysis()

# index
@app.route('/')
def index():
    return render_template('index.html')
