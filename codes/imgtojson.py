from rdflib import Graph, plugin
from rdflib.serializer import Serializer
i=0
testrdf=""
with open("../dataset/images_en.nt", "r") as f,open("../dataset/img_new.json", "w") as of:
	for line in f:
		
		testrdf=line
		g = Graph().parse(data=testrdf, format='n3')
 		of.write(g.serialize(format='json-ld', indent=4))
 		of.write("\n")
 		i=i+1

