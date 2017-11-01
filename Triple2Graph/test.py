#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
major comment that describes the code and project

"""


from collections import defaultdict
import xml.sax
from lxml import objectify
import xml.etree.ElementTree as ET
from collections import namedtuple


MyStruct = namedtuple("token", "ID lemma PoS NER")




def  main():
    #print()
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    # override the default ContextHandler
    parser.setContentHandler(corenlpHandler())
    parser.parse("100.txt.xml")


class corenlpHandler(xml.sax.ContentHandler):
    """some comment..."""

    data = {}

    
    def __init__(self):
        """some comment..."""
        self.CurrentData = ""
        self.token = ""
        self.word = ""
        self.lemma = ""
        self.pos = ""
        self.NER = ""
        self.dep_type = ""
        self.governor = ""
        self.dependent =  ""
    
    def startElement(self, tag, attributes):
        self.CurrentData = tag   
        if(tag == "token"):
           token_id = attributes["id"]
           print(token_id)     
        elif(tag == "dep"):
            dep_type = attributes["type"]
            print("Dependency Type ... "+dep_type)
            print(dep_type)
#             for (k,v) in attributes.items():
#                 print(k+ " " + v)
        
        
    def endElement(self, tag):
        if(self.CurrentData == "token"):
            print(self.token)
        if(self.CurrentData == "word"):
            print(self.word)
        if(self.CurrentData == "governor"):
            print(self.governor)
        elif(self.CurrentData == "dependent"):
            print(self.dependent)
     
    def characters(self, content):
        if(self.CurrentData == "token"):
            self.token = content
        if(self.CurrentData == "word"):
            self.word = content
        if(self.CurrentData == "governor"):
            self.governor = content
        elif(self.CurrentData == "dependent"):
            self.dependent = content   
        
        
        
if __name__ == "__main__":
    main()     