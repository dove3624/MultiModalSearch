from rdflib import Graph, plugin
from rdflib.serializer import Serializer
i=0
testrdf=""
with open("/Users/mukundverma/IR_Dataset/long-abstracts_en.nt", "r") as f,open("/Users/mukundverma/IR_Dataset/long_new.json", "w") as of:
	for line in f:
		if i%400==0:
			testrdf=line
			g = Graph().parse(data=testrdf, format='n3')
			#print g.serialize(format='json-ld', indent=4)
 			of.write(g.serialize(format='json-ld', indent=4))
 			of.write("\n")
 		i=i+1

