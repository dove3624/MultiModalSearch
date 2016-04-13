from elasticsearch import Elasticsearch
es = Elasticsearch()

idd=""
text=""
para=""
count = 1
with open("/Users/mukundverma/IR_Dataset/long_new.json","r") as fi:
	for line in fi:
		if "\"@id" in line:
			idd=line[44:]
			idd=idd[:-3]
		elif "\"@value" in line:
			text=line[27:]
			text=text[:-2]
		if len(idd)>0 and len(text)>0:
			para="{\n\"resource\" : " + "\"" + idd + "\"" + ",\"text\" :" + "\"" + text + "\"\n"+ "}"
			res = es.index(index="dbpedia", doc_type='abstracts', id=count, body=para)
			idd=""
			text=""
			para=""
			count=count+1

'''
res = es.get(index="test-index", doc_type='tweet', id=1)
print(res['_source'])

es.indices.refresh(index="test-index")

res = es.search(index="test-index", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
'''
