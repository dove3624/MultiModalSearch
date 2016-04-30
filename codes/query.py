from subprocess import call
from elasticsearch import Elasticsearch
import json
import requests
import enchant

d = enchant.Dict("en_US")
es = Elasticsearch()

uri_search = 'http://localhost:9200/test/images/_search'
image = ""
query = "robert f kennedy"
query = image + result

#print json.dumps(es.search(index = 'dbpedia', q = query), indent=1)
print "Suggestions"
print d.suggest(query)
resrc = es.search(index = 'dbpedia', q = query)

for hit in resrc['hits']['hits']:
    res =  hit["_source"]["resource"]
    print res
    print hit["_source"]["text"]
    rest = es.search(index="test", body={"query": {"match_phrase": {"resource": res}}})
    print "image"
    print rest