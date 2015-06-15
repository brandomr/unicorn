
# coding: utf-8


from elasticsearch import Elasticsearch
import requests
import ast
import json
import os


es = Elasticsearch('http://localhost:9200/')


es.indices.delete('dossiers')
es.indices.create('dossiers')

#es.put_mapping(index='dossiers', doc_type=map, mapping=mapping)

folder = os.listdir('reuters')
file_paths = folder[1:len(folder)-1]




count = 0

for file in file_paths:
    filename = 'reuters/' + file
    with open(filename) as f:
        text = f.read()
        
        out = requests.post('http://54.84.21.94:8080/extractor', data=json.dumps({"text":text})).text
        out = ast.literal_eval(out)
        print out

        try:
            people = out['people']
        except:
            people = []

        try:
            organizations = out['organizations']
        except:
            organizations = []

        try: 
            locations = out['locations']
        except:
            locations = []

        es_dict = {
                'file': text,
                'title': text[:50],
                'people': people,
                'organizations': organizations,
                'locations': locations,
                'owner': 'unicorn'
                }
        
        es.index(index='dossiers', doc_type='attachment', body=es_dict)
        
        f.close()
        
        count += 1
        print
        print count
        print
        print
        print
        print

