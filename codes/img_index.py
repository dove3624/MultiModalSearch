
from elasticsearch import Elasticsearch
es = Elasticsearch()

idd=""
text=""
para=""
img = ""
count = 1
with open("../dataset/img_new.json","r") as fi:
	for line in fi:
		line2 = fi.next()
		if "\"@id" in line:
			if "resource" in line:
				idd=line[43:]
				idd=idd[:-3]
			if "dbpedia.org/ontology/thumbnail" in line2:
				line3 = fi.next()
				line4 = fi.next()
				text=line4[20:]
				text=text[:-2]
			if len(idd)>0 and len(text)>0:
				print idd + " " + text
				para="{\n\"resource\" : " + "\"" + idd + "\"" + ",\"image\" :" + "\"" + text + "\"\n"+ "}"
				es.index(index="test", doc_type='images', id=count, body=para)
				idd=""
				text=""
				para=""
				count=count+1
				if(count % 100000 == 0):
					print count

