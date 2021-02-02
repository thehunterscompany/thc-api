from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def welcome():
    return jsonify('The Hunters Company')

@app.errorhandler(404)
def page_not_found(error):
    return { 'result': 'not_found' }, 404
