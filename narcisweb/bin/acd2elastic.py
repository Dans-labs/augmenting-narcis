from elasticsearch import helpers, Elasticsearch
import csv

es = Elasticsearch(
    ['elasticsnarcis'],
    http_auth=('elastic', 'changeme'),
    port=9200
    )

with open('/exchange/acd.csv') as acd:
    reader = csv.DictReader(acd)
    helpers.bulk(es, reader, index='acd', doc_type='metadata')
