from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    testi = "testi"
    return jsonify({"key" : testi})
