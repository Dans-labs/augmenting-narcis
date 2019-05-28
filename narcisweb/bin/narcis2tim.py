# -*- coding: utf-8 -*-
import itertools
import re
import os
import rdflib
import re
from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader

#EASY_OAI = 'http://easy.dans.knaw.nl/oai/'
EASY_OAI = "https://dataverse.nl/oai?verb=ListRecords&set=tilburg_oai&metadataPrefix=oai_dc"
EASY_OAI = "http://zandbak11.dans.knaw.nl/dataexplore/oai"
EASY_SPARQL = 'http://localhost:8890/sparql'
EASY_TARGET_GRAPH = 'https://dataverse.nl'
OAI_URL = "http://oai.narcis.nl/oai"

dc11 = rdflib.Namespace('http://purl.org/dc/elements/1.1/')
geo = rdflib.Namespace('http://www.w3.org/2003/01/geo/wgs84_pos#')
virtrdf = rdflib.Namespace('http://www.openlinksw.com/schemas/virtrdf#')
easy_id = rdflib.Namespace('https://dataverse.nl/dataset.xhtml?persistentId=')
rds = rdflib.Namespace('http://rdfs.org/ns/void#')
w3rds = rdflib.Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
oains = "http://oai.narcis.nl/oai?verb=GetRecord&metadataPrefix=oai_dc&identifier="

def easy_url(oai_id):
    namespace, dataset = oai_id.rsplit(':', 1)
    ns = rdflib.Namespace("%s%s:" % (oains, namespace))
    return ns[dataset]

def make_graphs(oai_records):
    for header, metadata, _ in oai_records:
        if metadata is None:
            continue
        graph = rdflib.Graph()
        s = easy_url(header.identifier())
	#d = easy_url(header.datestamp())
        metadata_fields = metadata.getMap().iteritems()
	graph.add((s, w3rds['type'], rdflib.Literal('Publication')))
        for p, vv in metadata_fields:
            for v in vv:
		print "Graph %s %s" % (p, v)
                graph.add((s, dc11[p], rdflib.Literal(v)))
        yield graph

def oai_metadata(oai_endpoint):
    registry = MetadataRegistry()
    registry.registerReader('oai_dc', oai_dc_reader)
    client = Client(oai_endpoint, registry)
    print client.listRecords(metadataPrefix='oai_dc')
    return make_graphs(client.listRecords(metadataPrefix='oai_dc'))

def add_geo(graph):
    return 

def easy_rdf(max_records=None):
    easy_records = itertools.islice(oai_metadata(OAI_URL), max_records)
    print easy_records
    return itertools.imap(easy_records)

def update_query(graph, graph_name):
    ntriples = graph.serialize(format='turtle')
    return '''INSERT DATA {{ GRAPH <{0}> {{ {1} }} }}'''.format(graph_name, ntriples)

def update_triplestore(records, sparql_endpoint_uri=EASY_SPARQL, graph_name=EASY_TARGET_GRAPH):
    """
    Save records to triplestore

    :param records: iterable of rdflib.Graph objects
    :param sparql_endpoint_uri: SPARQL Update endpoint
    :type sparql_endpoint_uri: str
    :param graph_name: target graph name
    :type graph_name: str
    """
    target_graph = rdflib.Graph(store='SPARQLUpdateStore', identifier=graph_name)
    target_graph.open((sparql_endpoint_uri, sparql_endpoint_uri), create=False)
    for record in records:
        target_graph.update(update_query(record, graph_name))

def dump_nt(records, filename, mode='w'):
    """
    Save records to disk in N-Triples format

    :param records: iterable of rdflib.Graph objects
    :param filename: output file name
    :param mode: file open mode
    """
    fout = open(filename, mode)
    newrecord = []
    g = rdflib.Graph()
    for record in records:
	if filename:
	    print "REC"
	    print record
	    #g.add((term[0], term[1], term[2]))
            record.serialize(fout, format='nt')

if __name__ == '__main__':
    dfile = 'narcis.100.nt'
    dump_nt(easy_rdf(10), dfile)
    newrdf = open("narcis100.nt","w")
    newrdf.write("@prefix dc: <http://purl.org/dc/elements/1.1/> .\n")
    newrdf.write("@prefix tim: <http://timbuctoo.huygens.knaw.nl/properties/> .\n")
    newrdf.write("@prefix w3rds: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n")
    newrdf.write("@prefix rds: <http://rdfs.org/ns/void#> .\n")
    newrdf.write("@prefix hdl: <http://hdl.handle.net/> .\n\n")

    with open(dfile) as f:
	for line in f:
	    line = line.replace('https://dataverse.nl/dataset.xhtml?persistentId=', 'hdl:')
	    line = line.replace('hdl://hdl.handle.net/', 'hdl:')
	    line = line.replace('http://purl.org/dc/elements/1.1/', 'dc:')
	    line = line.replace('http://www.w3.org/1999/02/22-rdf-syntax-ns#', 'w3rds:')
	    line = line.replace('http://rdfs.org/ns/void#', 'rds:')
	    line = re.sub(r'<(easy:\d+)>', '\\1', line) 
	    line = re.sub(r'<(dc\:\w+)>', '\\1', line)
	    line = re.sub(r'<w3rds:type>', 'w3rds:type', line)
	    line = re.sub(r'"Dataset"', 'rds:Dataset', line)
	    line = re.sub(r'"Publication"', 'rds:Publication', line)
	    newrdf.write(line)
