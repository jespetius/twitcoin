
# testaus pelkka flask
from flask import Flask, request, jsonify, render_template
from tweets_get import sentiment_analysis
import requests
app = Flask(__name__)

# json testi
@app.route('/json', methods=['GET', 'POST'])
def json():
    testi = "testi"
    return jsonify({"key": testi})

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
