from flask import Flask, request, jsonify, render_template
import requests
app = Flask(__name__)

@app.route('/json', methods=['GET', 'POST'])
def json():
    testi = "testi"
    return jsonify({"key" : testi})


@app.route('/user', methods=['POST'])
def user():
    user = request.form['userform']
    return jsonify({"key" : user})

@app.route('/')
def index():
    return render_template('index.html')