#testaus pelkka flask
from flask import Flask, request, jsonify, render_template
import requests
app = Flask(__name__)

#json testi
@app.route('/json', methods=['GET', 'POST'])
def json():
    testi = "testi"
    return jsonify({"key" : testi})

#user jsonina 
@app.route('/user', methods=['POST'])
def user():
    user = request.form['userform']
    return jsonify({"key" : user})

#index
@app.route('/')
def index():
    return render_template('index.html')

