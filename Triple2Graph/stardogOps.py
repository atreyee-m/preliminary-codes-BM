#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""

"""


__author__ = 'atreyee'

from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF, SKOS
from rdflib.plugins.stores import sparqlstore
import urllib3

def main():

    s = stardog()
    s.conn()

class stardog:

    def __init__(self):

        pass

    def conn(self):
        """
        
        connects to the sparqlstore(points to stardog at port 5820)
        :return: 
        """
        endpoint = 'http://156.56.14.247:5820'
        store = sparqlstore.SPARQLUpdateStore()
        store.open((endpoint, endpoint))
        print(store)

    def inputfromNLP(self):
        """
        gets the text triples as input and sends it to appropriate function
        :return: 
        """

        return

    def createDB(self):

        """
        
        :return: 
        """



        return

    def createURI(self):
        """
        
        
        :return: 
        """

        return

    def createSparqlQuery(self):
        """
        
        :return: 
        """

        return

    def modifyDB(self):
        """
        
        :return: 
        """


        pass

if __name__ == '__main__':
    main()

