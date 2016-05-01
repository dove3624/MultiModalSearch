from rdflib import Graph, plugin
from rdflib.serializer import Serializer

testrdf=""
with open("../dataset/long-abstracts_en.nt", "r") as f,open("../dataset/long_new.json", "w") as of:
	for line in f:
		testrdf=line
		g = Graph().parse(data=testrdf, format='n3')
		#print g.serialize(format='json-ld', indent=4)
 		of.write(g.serialize(format='json-ld', indent=4))
 		of.write("\n")

