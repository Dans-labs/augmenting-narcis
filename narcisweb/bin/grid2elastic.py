from elasticsearch import helpers, Elasticsearch
import csv

es = Elasticsearch(
    ['elasticsnarcis'],
    http_auth=('elastic', 'changeme'),
    port=9200
    )

with open('/exchange/grid/grid.csv') as grid:
    reader = csv.DictReader(grid)
    helpers.bulk(es, reader, index='grid', doc_type='metadata')
