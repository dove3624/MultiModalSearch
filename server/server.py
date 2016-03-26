#http://flask-restful-cn.readthedocs.org/en/0.3.4/quickstart.html
"""
    This is server program
"""
from flask import Flask, request, jsonify, render_template, url_for, redirect
from flask_restful import Resource, Api
import json, urllib, urllib2, unirest, re
from urllib2 import URLError
import numpy as np
import tensorflow as tf
from tensorflow.python.platform import gfile
import csv

app = Flask(__name__)
def create_graph():
	f = gfile.FastGFile('../codes/classify_image_graph_def.pb', 'rb')
	graph_def = tf.GraphDef()
	graph_def.ParseFromString(f.read())
	_ = tf.import_graph_def(graph_def, name='')

create_graph()

def get_classes():
	r1 = csv.reader(open("../codes/class_id_to_node_id.txt","rb"))
	r2 = csv.reader(open("../codes/node_id_to_class.txt","rb"), delimiter="\t")

	class_map = {}
	label_map = {}

	for row in r1:
		class_map[int(row[0])] = row[1]

	for row in r2:
		label_map[row[0]] = row[1]

	return class_map, label_map

class_map,label_map = get_classes()

sess = tf.Session()
		
def get_predictions(image):	
	image_data = gfile.FastGFile(image, 'rb').read()
	softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')	
	predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
	predictions = np.squeeze(predictions)
	top_k = predictions.argsort()[-5:][::-1]
	res = []
	for k in top_k:
		res.append(label_map[class_map[k]])
	return res

@app.route('/search', methods=['POST'])
def search():
    query = request.form['text']
    print get_predictions("../codes/cropped_panda.jpg")
   	
    return jsonify({'result':[]})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    #app.run(debug=True)