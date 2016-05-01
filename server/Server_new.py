import tensorflow.python.platform
import numpy as np
import tensorflow as tf
from tensorflow.python.platform import gfile
import csv
import socket

def create_graph():
    f = gfile.FastGFile('../dataset/classify_image_graph_def.pb', 'rb')
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')

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
		
def run_inference_on_image(image):
    image_data = gfile.FastGFile(image, 'rb').read()
 
    class_map, label_map = get_classes()

    res = ''
    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')
        predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
        predictions = np.squeeze(predictions)
        top_k = predictions.argsort()[-10:][::-1]
        print predictions.argsort()
        print top_k
        for k in top_k:
            res += label_map[class_map[k]] + ","

    return res

def main(_):
    create_graph()
    s = socket.socket()        
    host = socket.gethostname() 
    port = 9999                
    s.bind((host, port))        
    s.listen(5)                 
    while True:
        c, addr = s.accept()    
        prediction=run_inference_on_image("uploads/images/"+c.recv(1024))
        c.send(prediction)
        c.close()

if __name__ == '__main__':
    tf.app.run()

