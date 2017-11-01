#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


"""
CoreNLPXMLParser.py

(C) 2017 by Damir Cavar <damir@cavar.me>, Atreyee M. <>

In LingData use SentenceData to store properties of sentences and all tokens

The output of the CoreNLP parser is a sequence of sentences, plus correference of elements across sentences
"""


__license__ = """Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""
__revision__ = " $Id: CoreNLPXMLParser.py 2 2017-07-25 14:32:00Z damir $ "
__docformat__ = 'reStructuredText'
__author__ = 'Damir Cavar <damir@cavar.me>, Atreyee M.'
__version__='0.1'



import xml.etree.ElementTree as ET
from corenlp_pywrap import pywrap
import os.path, sys, glob, re
from LingData import SentenceData, Document, labels
import PSTree


def main():
    # pass
    annotator_list = ["tokenize", "cleanxml", "ssplit", "pos", "lemma", "ner", "parse", "depparse", "dcoref"]
    myParser = CoreNLPXMLParser()
    myParser.connect('http://156.56.14.247:9000', annotator_list)
    #myParser.connect('http://localhost:9000', annotator_list)
    x = "Tim Cook is the CEO of Apple."
    #x = "Tim Cook is the CEO of Apple."
    print(x)
    myParser.getParseFromConnection(x)
    #print("Root:", myParser.myDoc.sentences[0].getDependencyRoot())

    result = myParser.getConcepts()
    #print(result)
    for x in result:
        print(" ".join( x ) )
    #print(result)



class CoreNLPXMLParser():
    """
    Data structures/variables for tokens and dependencies from Stanford CoreNLP
    """

    def __init__(self):
        """Constructor."""
        self.cn = None
        self.myDoc = None


    def connect(self, url, annotators):
        """
        Establish a remote connection to a CoreNLP server.
        :param url:
        :param annotators:
        :return:
        """
        self.cn = pywrap.CoreNLP(url, annotators)


    def getParse(self, root):
        """Get the parse information for some text. If there is a remote connection, use it, otherwise assume
        that text contains a file name to read and process.
        :param root:
        :return:
        """
        self.myDoc = Document()
        data = None
        for child in root.findall(".//document/*"):
            if child.tag == "sentences":
                #does sentence have a subject?
                varHasNSubj = True

                for sentence in child.findall("*"):
                    mySent = SentenceData()
                    mySent.id = int(sentence.attrib['id'])
                    # parsing the sentence
                    for i in sentence.findall('.//tokens/*'):
                        td = {}
                        td[labels.id] = int(i.get('id'))
                        td[labels.word] = i.find('word').text
                        td[labels.lemma] = i.find('lemma').text
                        td[labels.POS] = i.find('POS').text
                        td[labels.NER] = i.find('NER').text
                        #print(td[labels.word], td[labels.POS])
                        #print(td)
                        mySent.tokens.append(td)
                    for i in sentence.findall('.//dependencies[@type="basic-dependencies"]/*'):
                        # parent and its dependent
                        depID = self.myDoc.getDepID(i.attrib["type"])
                        governor = int(i.find('governor').attrib['idx'])
                        dependent = int(i.find('dependent').attrib['idx'])
                        val = mySent.governor_k.get(governor, [])
                        val.append((dependent, depID))
                        mySent.governor_k[governor] = val
                        val = mySent.dependent_k.get(dependent, [])
                        val.append((governor, depID))
                        mySent.dependent_k[dependent] = val
                        # append the tuple with governor dependent for the dependency as key
                        mySent.depRelDict[depID] = mySent.depRelDict.get(depID, []) + [ (governor, dependent) ]
                        mySent.govRelation[(governor, depID)] = mySent.govRelation.get((governor, depID), []) + [ dependent ]
                    self.govOfDeprel(mySent,"dobj")
                    #print("depRelDict",mySent.depRelDict)
                    # call generateDeps
                    data = sentence.find('parse').text
                    #print(data)
                    #data = re.sub('[ \t\n]+',' ',data)
                    #pst = PSTree()
                    #pst.getClauses(data)
                    #print(list(pst.parseBrackets(data)))

                    #print(self.hasNsubj(mySent))
                    # if(self.hasNsubj(mySent)):
                    #     if(self.checkDobj(mySent)):
                    #         print("dobj present in the sentence")
                            #print(self.myDoc.getDepLabel(i),mySent.tokens[j[0][0]][labels.word],mySent.tokens[j[0][1]][labels.word])

                        #self.generateDeps(i, mySent,self.myDoc)
                    #if(self.hasDeprelType(mySent,"nsubj")):
                    #    pass

                    # add the sentence object to the Document instance
                    self.myDoc.addSentence(mySent)

            elif child.tag == "coreference":
                for x in child.findall('*'):
                    antecedent = None
                    anaphora = []
                    for z in x.findall('.mention'):
                        sentence = int(z.find('sentence').text)
                        start = int(z.find('start').text)
                        end = int(z.find('end').text)
                        head = int(z.find('head').text)
                        text = z.find('text').text
                        if 'representative' in z.attrib:
                            antecedent = (sentence, start, end, head, text)
                        else:
                            anaphora.append( (sentence, start, end, head, text) )
                    # process reference and corefs
                    for z in anaphora:
                        # store the anaphora for all antecedent
                        self.myDoc.addReference(z, antecedent)


    def translationRulesRel(self,mySent):

        return


    def hasDeprelType(self,mySent,deprel):
        """
        checks if a sentence has a particular type of deprel using the depreldict [key = depID, val is list of tuples (governor, dependent)]
        :param mySent: sentence object
        :param deprel: dependency relation
        :return: 
        """
        for i in mySent.depRelDict:
            if(self.myDoc.getDepLabel(i) == deprel):
                return True


    def govOfDeprel(self,mySent,deprel):
        #print(mySent.depRelDict)
        for i in mySent.depRelDict:
            if (self.myDoc.getDepLabel(i) == deprel):
                return mySent.tokens[j[0][0]][labels.id] #id of the parent


    def getParseFromConnection(self, text):
        """

        :param text:
        :return:
        """
        if self.cn:
            # parse by talking to remote server
            # resultXML = self.cn.basic(text, out_format='xml')
            result = self.cn.basic(text, out_format='xml').text

            root = ET.fromstring(result)
            self.getParse(root)


    def getConcepts(self):
        """

        :return:
        """
        return self.myDoc.getConcepts()


    def getParseFromFile(self, filename):
        """

        :param filename:
        :return:
        """
        if not os.path.exists(filename):
            print("Cannot read from file:", filename)
            exit(1)

        # process file content
        content = ""
        try:
            ifp = open(filename, mode='r', encoding='utf8')
            content = ifp.read()
            ifp.close()
        except IOError:
            print("Cannot read from file:", filename)
            exit(1)
        if content:
            root = ET.fromstring(self.cn.basic(content, out_format='xml').text)
            self.getParse(root)


if __name__ == "__main__":
    main()

