#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import xml.etree.ElementTree as ET
from collections import defaultdict
from collections import namedtuple
from corenlp_pywrap import pywrap
import xmlrpclib
import pprint


Token = namedtuple("token", ['id','word','lemma','POS','NER'], rename = True)
token_dict = {}
triple_dict = {}
full_annotator_list = ["tokenize", "cleanxml", "ssplit", "pos", "lemma", "ner", "parse", "depparse"]

def main():
    
    """ connection """
    data = readFile("sent3.txt")
    cn = pywrap.CoreNLP(url='http://149.161.139.120:9000', annotator_list=full_annotator_list) #149.161.139.120
    out = cn.basic(data, out_format='xml')
    print(out.text)
                  
    """ xml parse stuff """
    
    root= ET.fromstring(out.text)
    #root = tree.getroot()
    target_tokens = root.findall('.//tokens/*')
    target_dep = root.findall('.//dependencies[@type="basic-dependencies"]/*')  #considering basic dependencies only
    
    """ function calls to parse dep tree and parse the tokens """
    t = parseXmlTokens(root,target_tokens)
    #print(t)
    t1 = parseXmlDep(root,target_dep,t) #main func for parsing xml
    #print(t1)
    
""" 
reads a file
"""
def readFile(filename):
     
    with open(filename) as f:
         file = f.read()
    
    return(file)
   
class depParse(): pass




""" 
Input: root and tokens from the <tokens> tag which basically has the id of the word, word, lemma, POS, NER
Returns: a dictionary with key = id of the word; value = named tuple containing id,word,lemma,POS,NER
"""
def parseXmlTokens(root,target_tokens):
    #extractedTokenInfo = [];
    
    for token in target_tokens:
        t = Token._make([token.get('id'),token.find('word').text,token.find('lemma').text,token.find('POS').text,token.find('NER').text])
        #print t
        token_dict[t.id] = t.word,t.lemma,t.POS,t.NER
        #extractedTokenInfo.append(t)
    #print token_dict
    return(token_dict)



""" 
Input: root, the basic dependencies from corenlp, token dictionary from parseXmlTokens func
What it does: Parses the dependency tree from corenlp. In case of ccomp, the id of the verb in ccomp is stored as object. This is also
             the key to the dictionary which stores subject and object for the ccomp.
TBD: - compounds?  
     - consider the POS and NER from token dictionary and return dependency triple/tuple to make a decision for inserting into neo4j 
        api. Or this could be done in a different function.
Returns: dependencies in (root, subj, obj) where these are ids of the words. 

"""

def parseXmlDep(root,target_dep,t):
    
    
    print("[VERB, "+", SUBJECT, "+"OBJECT]")
    verb_subj_obj = [[],[],[]]
  
    
    verb_id = 0;verb_text = None
    subj_id = 0;subj_text = None
    obj_id = 0;obj_text = None
    cop_id = 0; cop_text = None
    ccomp_verb_id = 0 ; ccomp_triple = defaultdict(list)
    
    
    for dep in target_dep:
        #print(dep)    
        
#DO NOT REMOVE
#-------------------------------------------------------------------
#        governor = dep[0]  ;   dependent = dep[1]
#         if(dep.attrib['type'] == "root" or dep.attrib['type'] == "ccomp"):
#            verb_subj_obj[0].append(dependent.attrib['idx'])   
#            if(dep.attrib['type'] == "nsubj"):
#-------------------------------------------------------------------
 
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
            
            if(constructCompounds(target_dep,subj_id) is not None):
                verb_subj_obj[1].append(constructCompounds(target_dep,subj_id))
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
            cop_nmod_list = resolveForCop(target_dep,dep,cop_id)
            #print(cop_nmod_list)
            #verb_subj_obj[0].pop()
            #verb_subj_obj[0].append(cop_nmod_list[0])
            verb_subj_obj[2].append(cop_nmod_list[1])
            
               
#-------------------------------------------------------------------       
#DO NOT REMOVE...   
     
#         elif(dep.attrib['type'] == "aux"):
#              verb_subj_obj[0].append(dependent.attrib['idx'])
#          
#         elif(dep.attrib['type'] == "nsubj"):
#             verb_subj_obj[1].append(dependent.attrib['idx'])
#             print(dep,dependent.attrib['idx'])
#             #print(governor.attrib['idx'])
#             comp = constructCompounds(target_dep,dependent.attrib['idx']) #dep.attrib['type']
#             verb_subj_obj[1].append(comp)
#                        
#         elif(dep.attrib['type'] == "dobj"):
# #            print(dependent.attrib['idx'])
#             verb_subj_obj[2].append(dependent.attrib['idx'])
#             comp = constructCompounds(target_dep,dependent.attrib['idx'])
#             verb_subj_obj[2].append(comp)
#-------------------------------------------------------------------
    #print(aux)

    #print(verb_subj_obj)
    return(verb_subj_obj)     



def resolveForCop(target_dep,dep,cop_id):
    
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
def constructCCompTriple(target_dep,dep,ccomp_verb_id):
    
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
def constructCompounds(target_dep,dep_id):           
 
    
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

              
              
#not using this but this works = DO NOT REMOVE
# def getRootCComp(target_dep):
#      
#     root = []
#     ccomp = []
#      
#     for dep in target_dep:
#         if(dep.attrib['type'] == "root"):
#             root.append(dep[1].attrib['idx'])
#             #root_ccomp.append(dep[1].text)
#         if(dep.attrib['type'] == "ccomp"): 
#             ccomp.append(dep[1].attrib['idx'])   
#             #root_ccomp.append(dep[1].text)
#      
#     return(root,ccomp)

    
# 
# def getSubj(root,target_dep):
#     
#     
#     return
# 
# def getObj():
#     
#     return
 
            
            


        
            
        
    




if __name__ == "__main__":
    main()  