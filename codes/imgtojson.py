from rdflib import Graph, plugin
from rdflib.serializer import Serializer
i=0
testrdf=""
with open("/Users/mukundverma/IR_Dataset/images_en.nt", "r") as f,open("/Users/mukundverma/IR_Dataset/img_new.json", "w") as of:
	for line in f:
		
		testrdf=line
		g = Graph().parse(data=testrdf, format='n3')
 		of.write(g.serialize(format='json-ld', indent=4))
 		of.write("\n")
 		i=i+1

