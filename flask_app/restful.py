#testaus flaskrestfulin kanssa
from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

#testing
class Testi(Resource):
    def get(self):
        return {'about':'Testi'}

    def post(self):
        some_json = request.get_json()
        return {'you sent': some_json}, 201
    


api.add_resource(Testi, '/testi')
