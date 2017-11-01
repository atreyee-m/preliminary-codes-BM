#!/usr/bin/python
# -*- coding: utf-8 -*- 
from __future__ import print_function 
import sys,getopt
import rdflib
from py2neo import *
from py2neo import Graph
from py2neo import cypher
from py2neo import Node, Relationship
import socket
import csv
from neo4j.v1 import GraphDatabase, basic_auth
from py2neo import Graph
from py2neo import authenticate, Graph

#from py2neo.ext.ogm import Store
graph = Graph("bolt://neo4j:Gr@phdb_+r1pl35+0r3@156.56.14.247:7687/data")
labels = ['Person', 'Country', 'Company']

# def create(node_name):

#     print "create"

# class Person(object):
#     @classmethod
#     def create(cls):
    
def create(name,concept):
    #check if the node exists
    person_node = graph.create(Node(concept, name=name))
    #rel(person_node, "company", 0)
    rel(person_node)
    #graph.create(node(company=company), rel(cls._root, "company", 0), rel(person_node, "company", 0)) 
    

    
def main():
    if len(sys.argv) < 3: 
        app = sys.argv[0] 
        print("Usage: {0} <add node/add relation/add concept> <name> <concept>".format(app)) 
        sys.exit() 
    add_stuff=sys.argv[1]
    if(add_stuff == "add node"):
        create(*sys.argv[2:])
    elif(add_stuff == "add relation"):
        create(*sys.argv[2:])
    else:
        print("unknown command")
 
# def main(argv):
# 
#     #print 'Number of arguments:', len(sys.argv), 'arguments.'
#     #print 'Argument List:', str(sys.argv)
# # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# # s.connect(("8.8.8.8", 80))
# # print(s.getsockname()[0])
# # connection_str = "bolt://"+s.getsockname()[0]+":7687/db/data"
# # print(connection_str)
#     
#     type = sys.argv[1]
#     
#     #driver = GraphDatabase.driver("bolt://156.56.14.247:7687", auth=basic_auth("neo4j", "Gr@phdb_+r1pl35+0r3"))
# #driver = GraphDatabase.driver("connection_str", auth=basic_auth("neo4j", "Gr@phdb_+r1pl35+0r3"))
#     #session = driver.session()
#     
#     #print concept
#     
#     if(type == "node"):
#         create_node(graph, concept, node_name)
#     else:
#         create_relation(graph, concept, )
#     
#     # set up authentication parameters
#     #authenticate("156.56.14.247:7687", "neo4j", "Gr@phdb_+r1pl35+0r3")
# 
# # connect to authenticated graph database
# #http://arthur:excalibur@camelot:1138/db/data/
#     
# #funcs
# 
#     
#     create_node(graph,concept,node_name)
#     #execute_queries()
#     create_relation(graph, relation_name)
# 
# 
# 
#     #session.close()
# 
#   
#     
#     
#     
# def create_node(graph,concept,node_name):
#     
#     
#     #session.run("CREATE (a:People {name: {name}, title: {title}})", {"name": "Arthur", "title": "King"})
#     graph.create(Node(concept, name=node_name))
# 
# 
# def create_relation(graph, relation_name):    
#     print "func"
#     
#     
# # def add_relations():
# # #trying py2neo
# #     session.run('''MERGE (arthur:People {name: "Arthur"})
# #    MERGE (mary:People {name: "Mary"})
# #    CREATE UNIQUE (arthur)-[:KNOWS]->(mary)''')
# # 
# # def execute_queries():
# #     result = session.run("MATCH (a:People) WHERE a.name = {name} "
# #                      "RETURN a.name AS name, a.title AS title",
# #                      {"name": "Arthur"})
# # 
# #     for record in result:
# #         print("%s %s" % (record["title"], record["name"]))
# 
# 
if __name__ == "__main__": main()