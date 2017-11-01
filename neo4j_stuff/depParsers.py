#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import xml.etree.ElementTree as ET
from collections import defaultdict
from collections import namedtuple
from corenlp_pywrap import pywrap
import xmlrpclib
import pprint
import xml.sax
from enum import Enum



full_annotator_list = ["tokenize", "cleanxml", "ssplit", "pos", "lemma", "ner", "parse", "depparse"]

triple_dict = {}


def main():
    
    
    data = readFile("sent3.txt")
    #cn = pywrap.CoreNLP(url='http://149.161.139.120:9000', annotator_list=full_annotator_list) #on IUSecure
    cn = pywrap.CoreNLP(url='http://156.56.14.246:9000', annotator_list=full_annotator_list) #on LAN
    out = cn.basic(data, out_format='xml')
    root= ET.fromstring(out.text)
    dep = depParser()
    dep.storeTokens(root)    
    #dep.storeDep(root)
    #dep.lists(root)
    dep.parseDeps(root)
    
def readFile(filename):
     
    with open(filename) as f:
        file = f.read()
        print(file)
    return(file)    


class depParser():

#     labels = Enum('word', 'lemma', 'type', 'pos')
    #values = Enum('ROOT')
    labels = Enum('labels','id word lemma POS NER type')
    #tokens = [ { labels.word:'', labels.lemma:'', labels.type: 'ROOT' } ]
    #td = {labels.id:'', labels.word:'', labels.lemma:'', labels.POS:'', labels.NER:'', labels.type:''}
    tokens = [{labels.id:0, labels.word:'', labels.lemma:'', labels.POS:'ROOT', labels.NER:''}]
    
#     token_listofdict = []
#     token_dict = {}
#     Token = namedtuple("token", ['id','word','lemma','POS','NER','type'], rename = True)
    
    
    # list of dictionaries

    dependencies = {}
    constituents = []

    dep2id = {}
    id2dep = {}
    
    
    def storeTokens(self,root):
        
#         for i in root.findall('.//tokens/*'):
#             t = Token._make([token.get('id'),token.find('word').text,token.find('lemma').text,token.find('POS').text,token.find('NER').text])
#       
        td = {}
        #print(self.tokens)
        #print(self.labels.__members__.items())
        for i in root.findall('.//tokens/*'): 
            #print(i)
            td[self.labels.id] = int(i.get('id'))
            td[self.labels.word] = i.find('word').text
            td[self.labels.lemma] = i.find('lemma').text
            td[self.labels.POS] = i.find('POS').text
            td[self.labels.NER] = i.find('NER').text
            #td[self.labels.type] = 'notROOT'
            #print(td)
            self.tokens.append(td.copy())
        #print(self.tokens)
        
        
#         for i in self.tokens:
#             print(i)
         
         
        return(self.tokens)
    
    deprel_dict = {}
#     governor_of = {}
#     dependent_of = {}
    governor_of = {};gov_list = [];dep_list = []
    dependent_of = {}
    gov_tup = []; dep_tup = []
    
    
    def storeDep(self,root):
        
        deprels = []; #gov_dep = defaultdict(list); dep_dep = defaultdict(list)
        for i in root.findall('.//dependencies[@type="basic-dependencies"]/*'):
            ###############################################################################################
            #print(i.items()); print(i,i.items(),i.getchildren())
            #deprel_dict = dep rel:(governor,dependent)
            #self.deprel_dict[self.getDepID(i.attrib['type'])]=int(i[0].attrib['idx']),int(i[1].attrib['idx']) 
            #print(self.getDepID(i.attrib['type']))
            #self.other_dict[int(i[0].attrib['idx'])] = self.getDepID(i.attrib['type']),int(i[1].attrib['idx'])
            
            #with integer dependencies
            #self.governor_of[int(i[0].attrib['idx'])] = self.getDepID(i.attrib['type']),int(i[1].attrib['idx'])
            #self.dependent_of[int(i[1].attrib['idx'])] = self.getDepID(i.attrib['type']),int(i[0].attrib['idx'])
            ###
            
            #print(i.items())
#             self.gov_tup.append((int(i[0].attrib['idx']),i.attrib['type'],int(i[1].attrib['idx'])))
#             self.dep_tup.append((int(i[1].attrib['idx']),i.attrib['type'],int(i[0].attrib['idx'])))
            #self.governor_of[int(i[0].attrib['idx'])] = i.attrib['type'],int(i[1].attrib['idx'])
            #print(self.governor_of)
            #self.dependent_of[int(i[1].attrib['idx'])] = i.attrib['type'],int(i[0].attrib['idx'])
            #print(self.dependent_of)
            #print('--------------------------------')

        #print(self.governor_of)
            ###############################################################################################
            print(i[0].text,i[1].text)
            self.governor_of[i[0].text]=(i.attrib['type'],i[1].text)
            self.gov_list.append(self.governor_of.copy())                                
            #print(self.governor_of)
        
        #print(self.gov_list)
        #print(self.governor_of)
        for i in self.gov_list:
            print(i)
        
        #print(self.gov_tup);print(self.dep_tup)
        print('--------------------------------')
         
        #print(self.dependent_of)

        return(self.consolidate(self.governor_of,self.dependent_of))
    
    def lists(self,root):
        for i in root.findall('.//dependencies[@type="basic-dependencies"]/*'):
            
            self.gov_list.append(i[0].text)
            self.dep_list.append(i[1].text)
        #print(set(self.gov_list),set(self.dep_list))   
        
        self.gov_list = set(self.gov_list);self.dep_list = set(self.dep_list)
             
        return(self.gov_list,self.dep_list)
    
    def parseDeps(self,root):
        
        
        gov_lst,dep_lst = self.lists(root)
        l = []
        
        for i in root.findall('.//dependencies[@type="basic-dependencies"]/*'):
            if i[0].text in gov_lst:
                #print(i[0].text)
                #self.governor_of[i[0].text].append((i.attrib['type'],i[1].text))
               #print(self.governor_of)
                self.governor_of[i[0].text] = i.attrib['type'],i[1].text
                l.append(self.governor_of)
        
        print(l)
        
        
        return
    
        
        
            
            
        
    def consolidate(self,governor_of,dependent_of):  
        
        for key in set(self.governor_of.keys() + self.dependent_of.keys()):
            try:
                self.dependencies.setdefault(key,[]).append(self.governor_of[key])        
            except KeyError:
                pass

            try:
                self.dependencies.setdefault(key,[]).append(self.dependent_of[key])          
            except KeyError:
                pass

        #print(self.dependencies)
#         for i in self.dependencies.items():
#             print(i)
        
        
        return(self.dependencies)  

    def getDepID(self, label):
        """return the ID for a dependency label"""

        if label in self.dep2id:
            return self.dep2id[label]
        newid = len(self.dep2id) + 1
        self.dep2id[label] = newid
        self.id2dep[newid] = label
        return newid


    def getDepLabel(self, idn):
        """return the label for a dependency ID"""

        if idn in self.id2dep:
            return self.id2dep
        return 0



    def input1(self,data,cn):
 
        out = cn.basic(data, out_format='xml')
        root= ET.fromstring(out.text)
        #root = tree.getroot()
        target_tokens = root.findall('.//tokens/*')
        target_dep = root.findall('.//dependencies[@type="basic-dependencies"]/*')  #considering basic dependencies only
        pxt = self.parseXmlTokens(root,target_tokens)
        self.parseXmlDep(root, target_dep, pxt)
        

        
    def parseXmlTokens(self,root,target_tokens):
    #extractedTokenInfo = [];
     
        for token in target_tokens:
            t = Token._make([token.get('id'),token.find('word').text,token.find('lemma').text,token.find('POS').text,token.find('NER').text])
            #print t
            token_dict[t.id] = t.word,t.lemma,t.POS,t.NER
            #extractedTokenInfo.append(t)
        #print token_dict
        return(token_dict)       
        






    def parseXmlDep(self,root,target_dep,t):
        
        #print("[VERB, "+", SUBJECT, "+"OBJECT]")
        verb_subj_obj = [[],[],[]]
      
        
        verb_id = 0;verb_text = None
        subj_id = 0;subj_text = None
        obj_id = 0;obj_text = None
        cop_id = 0; cop_text = None
        ccomp_verb_id = 0 ; ccomp_triple = defaultdict(list)
        
        
        for dep in target_dep:
            #print(dep)    
     
            if(dep.attrib['type'] == "root"):
                verb_text = dep[1].text
                verb_id = dep[1].attrib['idx']
                verb_subj_obj[0].append(verb_id)
                #print(verb_text,verb_id)
            #print(verb_text,verb_id)    
            if(dep.attrib['type'] == "nsubj" and dep[0].attrib['idx'] == verb_id):
                subj_text = dep[1].text
                subj_id = dep[1].attrib['idx']
                verb_subj_obj[1].append(subj_id)
                #print(subj_id,subj_text)
                
                if(self.constructCompounds(target_dep,subj_id) is not None):
                    verb_subj_obj[1].append(self.constructCompounds(target_dep,subj_id))
                    verb_subj_obj[1].sort(key=int)
                
                #print(subj_text,subj_id)
                
            if(dep.attrib['type'] == "dobj" and dep[0].attrib['idx'] == verb_id):
                obj_text = dep[1].text
                obj_id = dep[1].attrib['idx']
                verb_subj_obj[2].append(obj_id)
                #print(obj_text,obj_id)
                if(constructCompounds(target_dep,obj_id) is not None):
                    verb_subj_obj[2].append(constructCompounds(target_dep,obj_id))
                    verb_subj_obj[2].sort(key=int)
                
            if(dep.attrib['type'] == "ccomp"):
                print("........found ccomp")
                ccomp_verb_id = dep[1].attrib['idx']
                ccomp_triple_list = constructCCompTriple(target_dep,dep,ccomp_verb_id)
                ccomp_triple[ccomp_verb_id].append(ccomp_triple_list)
                verb_subj_obj[2].append(ccomp_verb_id)
            
            if(dep.attrib['type'] == "cop"):
                cop_id = dep[1].attrib['idx']
                cop_nmod_list = self.resolveForCop(target_dep,dep,cop_id)
                #print(cop_nmod_list)
                #verb_subj_obj[0].pop()
                #verb_subj_obj[0].append(cop_nmod_list[0])
                verb_subj_obj[2].append(cop_nmod_list[1])
                
        return(verb_subj_obj)   
    def resolveForCop(self,target_dep,dep,cop_id):
    
        #print(target_dep,dep,cop_id)
        cop_gov_id = 0 #This is also the governor for nmod
        cop_nmod_list = [[],[]]
        
        print(".........inside resolveForCop")
        print(cop_id)
        for i in target_dep:
            if(i.attrib['type'] == "cop" and i[1].attrib['idx'] == cop_id):
                #print(i[0].text,i[1].text)
                cop_gov_id = i[0].attrib['idx']
                cop_nmod_list[0].append(cop_gov_id)
                cop_nmod_list[0].append(i[0].attrib['idx'])
            if(i.attrib['type'] == "nmod" and i[0].attrib['idx'] == cop_gov_id):
                cop_nmod_list[1].append(i[1].attrib['idx'])
                
        return(cop_nmod_list)
    
    """
    Input: parent dependency tag, current dependency sibling and the id of the ccomp dependency
    returns: a [V,S,O] list corresponding to the ccomp
    """
    def constructCCompTriple(self,target_dep,dep,ccomp_verb_id):
        
        print("CCOMP TRIPLE: [VERB],[SUBJECT],[OBJECT]")
        ccomp_triple_list = [ccomp_verb_id,[],[]]
        print("........inside constructCCompTriple")
        cc_subj_text = None; cc_subj_id = 0
        
        
        for c_dep in target_dep:
            #print(c_dep)
            if(c_dep.attrib['type'] == "nsubj" and c_dep[0].attrib['idx'] == ccomp_verb_id):
                cc_subj_id = c_dep[1].attrib['idx']
                cc_subj_text = c_dep[1].text
                #print("subj of ccomp: ",cc_subj_id,cc_subj_text)
                ccomp_triple_list[1].append(cc_subj_id)
                if(constructCompounds(target_dep,cc_subj_id) is not None):
                    ccomp_triple_list[1].append(constructCompounds(target_dep,cc_subj_id))
                    ccomp_triple_list[1].sort(key=int)
                
            if(c_dep.attrib['type'] == "dobj" and c_dep[0].attrib['idx'] == ccomp_verb_id):
                #print("found obj of ccomp")
                cc_obj_text = c_dep[1].text
                cc_obj_id = c_dep[1].attrib['idx'] 
                #print("obj of ccomp:",obj_id,obj_text)
                ccomp_triple_list[2].append(cc_obj_id)
                if(constructCompounds(target_dep,cc_obj_id) is not None):
                    ccomp_triple_list[1].append(constructCompounds(target_dep,cc_obj_id))
                    ccomp_triple_list[1].sort(key=int)            
        
        print("ccomp triple:",ccomp_triple_list)
        return(ccomp_triple_list)
        
    """
    What it does: checks if an id belongs to a compound
    Input: dep tree, sub or obj id
    Returns: other part of the compound from compound tag in dependency tree
    """
    def constructCompounds(self,target_dep,dep_id):           
     
        
        print("........... inside construct compounds func")
        #print(dep_id)
        #print(target_dep)
        
        compound_dep_id = None
        
        for dep in target_dep:
            #print("..........................inside for")
            governor = dep[0]  
            dependent = dep[1]
            #comp = None          
            #print(dep_id)
            if(dep.attrib['type'] == "compound" and governor.attrib['idx'] == dep_id):
                #print(dependent.text)
                compound_dep_id = dependent.attrib['idx']
                #print(compound_dep_id)
                return(compound_dep_id)
    
    
    
    
    
    


if __name__ == "__main__":
    main()