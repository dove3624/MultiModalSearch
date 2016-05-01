from elasticsearch import Elasticsearch
es = Elasticsearch()

idd=""
text=""
count = 1
with open("../dataset/long_new.json","r") as fi:
	for line in fi:
		if "\"@id" in line:
			idd=line[44:]
			idd=idd[:-3]
		elif "\"@value" in line:
			text=line[27:]
			text=text[:-2]
		if len(idd)>0 and len(text)>0:
			para={"resource" : idd, "text1" : text}
			#print para
			es.index(index="dbpedia", doc_type='abstracts', id=count, body=para)
			idd=""
			text=""
			para=""
			count=count+1
			if(count % 100000 == 0):
				print count






'''
curl -XPUT 'http://localhost:9200/dbpedia/abstracts/1' -d '{
"resource" : "Calvin and Hobbes",
"text" : "Comics by Bill Waterson."
}'

curl -XPUT "http://localhost:9200/movies/movie/1" -d '{ "title": "The Godfather","director": "Francis Ford Coppola","year": 1972}'


curl -XPUT 'http://localhost:9200/dbpedia/abstracts/1' -d '{
"resource" : "Calvin and Hobbes",
"text" : "Comics by Bill Waterson."
}'
'''