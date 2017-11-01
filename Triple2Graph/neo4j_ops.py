#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
neoSomethingj_ops.py

(C) 2017 by Atreyee Mukherjee, Damir Cavar

Functionalities:
 - connects to the parser, gets the triples and inserts into the neo4j
 - creates nodes, relationships, labels
 - If a label is not available, it assigns a default label to the node
 - For relationships, a check is in place for the nodes, if the associated nodes arent present, they are created.
 - Similarly for attributes, an attribute is attached to an existing node and if the node isnt present, it is created before the attribute is attached to it.
"""

import sys, getopt, os
import time
import py2neo
from CoreNLPXMLParser import *


# from LingData import SentenceData, Document, labels


def main():
    Decision().neoFunctions()


#     #graph.addAttribute("OSU", "level", "high")
#     #graph.addLabel("apple", "company")
#     graph.addRelation("VW", "apple", "bought")
#     defaultLabel = "Test"
#     #graph.replaceDefaultLabel("Sony")


class Decision(CoreNLPXMLParser, Document):
    """
    - This class calls the function which extracts the triples
    - Calls appropriate neo4j function for to insert an label/relationship/attribute
    
    """

    DATABASE_URL = 'bolt://neo4j:Gr@phdb_+r1pl35+0r3@156.56.14.247:7687'

    def __init__(self):
        pass

    def getCoreNLPTriples(self):
        annotator_list = ["tokenize", "cleanxml", "ssplit", "pos", "lemma", "ner", "parse", "depparse", "dcoref"]
        myParser = CoreNLPXMLParser()
        myParser.connect('http://156.56.14.247:9000', annotator_list)
        myParser.getParseFromConnection("Jeffrey P. Bezos loves Google.")
        result = myParser.getConcepts()
        return result

    def neoFunctions(self):
        neoGraph = BMGraph(self.DATABASE_URL)
        triples = []
        triples.append(self.getCoreNLPTriples())
        print(triples)
        for tple in triples:
            for i in tple:
                if (i[1] == 'isA'):
                    neoGraph.addLabel(i[0], i[2])
                # elif(i[1] == 'hasA'): #attributes?
                #     neoGraph.addAttribute(i[0],i[1],i[2])
                else:
                    neoGraph.addRelation(i[0], i[2], i[1])


class BMGraph(py2neo.Graph):
    """BMGraph adds"""

    # index = graph_db.get_or_create_index(Node, "index_name")
    defaultLabel = "Test"

    def addLabel(self, nodeName, label):
        """Adds an isA relation to the Graph"""
        try:
            # get the node
            nodeIDs = self.findNode(nodeName)
            # print(nodeIDs)
            # add to node add_label(label)
            if len(nodeIDs) > 1:
                # print("we got more nodes with that name")
                raise MultipleNodeFoundError("Multiple nodes with this name")
                # return
            if len(nodeIDs) == 1:
                print("Adding new label", label, "to node", nodeName)
                myNode = self.node(nodeIDs[0])
                myNode.add_label(label)
                # replacing default label
                if len(myNode.labels()) > 1 and self.defaultLabel in myNode.labels():
                    myNode.remove_label(self.defaultLabel)
                    # finally pushing the node """
                myNode.push()
            else:
                print("Adding new node", nodeName, "with label", label)
                tx = self.begin(autocommit=False)
                newNode = py2neo.Node(label, name=nodeName)
                tx.create(newNode)
                tx.commit()
        except MultipleNodeFoundError as problem:
            print("Multiple nodes found problem: {0}".format(problem))

    def addAttribute(self, nodeName, attribute, attrvalue):
        """ Adds new attributes (or properties, in neo4j terms) to the graph"""
        # get the node
        try:
            nodeIDs = self.findNode(nodeName)
            # add to node add_label(label)
            if len(nodeIDs) > 1:
                # print("we got more nodes with that name")
                # return
                raise MultipleNodeFoundError("Multiple nodes with this name")
            if len(nodeIDs) == 1:
                print("Adding new attribute", attribute, "with value", attrvalue, "to node", nodeName)
                myNode = self.node(nodeIDs[0])
                myNode[attribute] = attrvalue
                myNode.push()
            else:
                print("Adding new attribute", attribute, "with value", attrvalue, "to new node", nodeName)
                tx = self.begin(autocommit=False)
                newNode = py2neo.Node(self.defaultLabel, name=nodeName)
                newNode[attribute] = attrvalue
                tx.create(newNode)
                tx.commit()
        except MultipleNodeFoundError as problem:
            print("Multiple nodes found problem: {0}".format(problem))

    def createNewNode(self, nodeName):
        """ Creates new node with the default label if the label is not mentioned. """
        return self.createNewNodeWithLabel(nodeName, self.defaultLabel)

    def createNewNodeWithLabel(self, nodeName, label):
        """Creates a new node with the given label """
        tx = self.begin(autocommit=False)
        newNode = py2neo.Node(label, name=nodeName)
        tx.create(newNode)
        tx.commit()
        return py2neo.remote(newNode)._id

    def addRelation(self, fromNode, toNode, relation):
        """Adds a new relationship between nodes with label."""
        try:
            nodeIDs = self.findNode(fromNode)
            # add to node add_label(label)
            if len(nodeIDs) > 1:
                # print("we got more source nodes with that name")
                # return
                raise MultipleNodeFoundError("Multiple source nodes with this name")
            if len(nodeIDs) == 1:  # one node exists
                fromNodeID = nodeIDs[0]
            else:  # no node exists, create new node
                fromNodeID = self.createNewNode(fromNode)
            nodeIDs = self.findNode(toNode)
            # add to node add_label(label)
            if len(nodeIDs) > 1:
                # print("we got more target nodes with that name")
                # return
                raise MultipleNodeFoundError("Multiple target nodes with this name")
            if len(nodeIDs) == 1:  # one node exists
                toNodeID = nodeIDs[0]
            else:  # no node exists, create new node
                toNodeID = self.createNewNode(toNode)
            tx = self.begin(autocommit=False)
            newRelationship = py2neo.Relationship(self.node(fromNodeID), relation, self.node(toNodeID))
            tx.create(newRelationship)
            tx.commit()
        except MultipleNodeFoundError as problem:
            print("Multiple nodes found problem: {0}".format(problem))

    def findNode(self, nodeName):
        """ Returns the id of a node which is assigned by neo4j """
        return ([i['ID(n)'] for i in self.run("MATCH (n) where n.name = '" + nodeName + "' return ID(n)")])

    # nope
    def replaceDefaultLabel(self, nodeName):
        """ Deletes the default label if any other label exists """

        nodeID = self.findNode(nodeName)
        # print(self.defaultLabel)
        # print nodeID
        if len(nodeID) > 1:
            print("Multiple nodes with same name")
        else:
            print("removing default label..")
            myNode = self.node(nodeID[0])
            if len(myNode.labels()) > 1 and self.defaultLabel in myNode.labels():
                print(myNode.labels())
                myNode.remove_label(self.defaultLabel)
                myNode.push()
                print("removed default node label")

    def connect(self, url):
        pass


class MultipleNodeFoundError(Exception):
    def __init__(self, mismatch):
        Exception.__init__(self, mismatch)


if __name__ == "__main__":
    main()
    # if len(sys.argv) < 3:
    #    app = sys.argv[0]
    #    print("Usage: {0} <node_type> <attr_file>".format(app))
    #    #print("       {0} list".format(app))
    #    sys.exit()
    # node_type = sys.argv[1]
    # attr_file = sys.argv[2]
    # ccg = createCompanyGraph()
    # ccg.createIndividualNodes(node_type,attr_file)
    # new_rel = createRelation()
    # to_node = 'apple'
    # from_node = 'John'
    # new_rel.createRelations(from_node, to_node)
