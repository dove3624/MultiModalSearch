#http://flask-restful-cn.readthedocs.org/en/0.3.4/quickstart.html
"""
    This is server program
"""
from flask import Flask, request, jsonify, render_template, url_for, redirect
from flask_restful import Resource, Api
import json, urllib, urllib2, unirest, re
from urllib2 import URLError

app = Flask(__name__)



@app.route('/search', methods=['POST'])
def search():
    query = request.form['text']

   	
    return jsonify({'result':[]})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=8080)
    app.run(debug=True)