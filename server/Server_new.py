import socket              
import tensorflow as tf
from tensorflow.python.platform import gfile
import csv

def create_graph():
	f = gfile.FastGFile('../dataset/classify_image_graph_def.pb', 'rb')
	graph_def = tf.GraphDef()
	graph_def.ParseFromString(f.read())
	_ = tf.import_graph_def(graph_def, name='')

create_graph()

def get_classes():
	r1 = csv.reader(open("../dataset/class_id_to_node_id.txt","rb"))
	r2 = csv.reader(open("../dataset/node_id_to_class.txt","rb"), delimiter="\t")

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

s = socket.socket()        
host = socket.gethostname() 
port = 12345                
s.bind((host, port))        
s.listen(5)                 
while True:
   c, addr = s.accept()    
   prediction=get_predictions(c.recv(1024))
   c.send(prediction)
   c.close()