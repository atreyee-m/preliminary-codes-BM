
#!/usr/bin/env python 
# -*- coding: utf-8 -*- 


import sys 
from py2neo import Node, Relationship
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

#check!!
graph_db = Graph("bolt://neo4j:Gr@phdb_+r1pl35+0r3@156.56.14.247:7687/data")

class Person(object): 
    
    _root = graph_db.get_or_create_index("reference", 
         "contacts", "root") 
    
    @classmethod 
    def create(cls, name, *companys): 
        person_node, _ = graph_db.create(node(name=name), 
              rel(cls._root, "PERSON", 0)) 
        for company in companys: 
            graph_db.create(node(company=company), rel(cls._root, "company", 0), rel(person_node, "company", 0)) 
        return Person(person_node) 
    
    @classmethod 
    def get_all(cls): 
        return [Person(person.end_node) for person in 
              cls._root.match("PERSON")] 
    
    def __init__(self, node): 
        self._node = node 
    
    def __str__(self): 
        return self.name + "\n" + "\n".join("  <{0}>"
             .format(company) for company in self.companys) 
    
    @property 
    def name(self): 
        return self._node["name"] 
    
    @property 
    def companys(self): 
        return [rel.end_node["company"] for rel in 
             self._node.match("company")] 

if __name__ == "__main__": 
    if len(sys.argv) < 2: 
        app = sys.argv[0] 
        print("Usage: {0} add <name> <company>[<company>...]".format(app)) 
        print("       {0} list".format(app)) 
        sys.exit() 
    method = sys.argv[1] 
    if method == "add": 
        print(Person.create(*sys.argv[2:])) 
    elif method == "list": 
        for person in Person.get_all(): 
            print(person) 
    else: 
        print("Unknown command")