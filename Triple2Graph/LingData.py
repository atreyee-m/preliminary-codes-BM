# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
*LingData.py*

(C) 2017 by Damir Cavar <damir@cavar.me>, Atreyee M. <>

Provides classes for linguistic data coming from parsers

**Date Created on:**
Tue Jun 20 16:30:00 2016

**Copyright:**
Copyright 2016-2017 by Damir Cavar, Atreyee Mukherjee

**Note:**
This needs some more specification specification and optimization.


**Bug:** None (we never code bugs!)

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
__revision__ = " $Id: LingData.py 2 2017-07-25 14:32:00Z damir $ "
__docformat__ = 'reStructuredText'
__author__ = 'Damir Cavar <damir@cavar.me>, Atreyee M.'
__version__='0.1'


from enum import Enum
#import PSTree

labels = Enum('labels', 'id word lemma POS SPOS NER foreign isReferent hasAntecedent RefText RefS RefFrom RefTo RefHead')
wtypes = Enum('wtypes', 'verb noun pronoun copula unknown')

def main():
    pass



class Document():
    """This is the main class that holds documents, which consist of a set of sentences.
    """

    def __init__(self):
        self.sentences = [] #: list of sentences
        self.sIDs = {}      #: dictionary with sentence IDs as keys and the sentence number in the list as value
        self.index = 0      #: helping variable for iterations
        self.dep2id = {}    #: dictionary with dependencies as strings (keys) and int IDs as values
        self.id2dep = {}    #: dictionary of dependency IDs as values and the string representation

        # coreference relations
        # key tuple(token_from, token_to); value is tuple(sentence_ID, from, to)
        self.corefs = {}  #: coreference relations coded in keys and values, keys are tuple(token_from, token_to), value is tuple(sentence_ID, from, to)
        # list of references for a token sequence
        self.refs = {}    #: key is a tuple of indices over tokens, the value is a reference


    def addSentence(self, sentenceObject):
        """Adds a sentence object to the list of sentences keeping track of ID to index in the list."""

        if sentenceObject.id:
            self.sIDs[sentenceObject.id] = len(self.sentences)
        self.sentences.append(sentenceObject)


    def getSentenceByID(self, sentenceID):
        """Returns the sentence for an ID"""

        index = self.sIDs.get(sentenceID, None)
        if index != None:
            return self.sentences[index]
        else:
            return None


    def __iter__(self):
        self.index = -1
        return self


    def __next__(self):
        if self.index >= len(self.sentences) - 1:
            raise StopIteration
        self.index = self.index + 1
        return self.sentences[self.index]


    def addReference(self, anaphora, antecedent):
        """Add coreferences."""

        anaphora = tuple(anaphora)
        antecedent = tuple(antecedent)
        self.refs[antecedent] = self.refs.get(antecedent, []) + [ anaphora ]

        # store the antecedent for the anaphora
        self.corefs[anaphora] = antecedent

        # store facts in tokens
        anaphoraSentence = self.getSentenceByID(anaphora[0])

        # this generates Tim Cook from he or from CEO
        mw = (anaphora[2] - anaphora[1]) > 1
        for i in range(anaphora[1], anaphora[2]):
            anaphoraSentence.antecedent[i] = antecedent
            if mw:
                anaphoraSentence.mw[i] = anaphora
        antecedentSentence = self.getSentenceByID(antecedent[0])

        # store the antecedent as refering to itself (this generates Tim Cook from Cook)
        for i in range(antecedent[1], antecedent[2]):
            antecedentSentence.antecedent[i] = antecedent



    def getTokens(self, s, f, to):
        """Returns the tokens for a sentence."""

        sentence = self.getSentenceByID(s)
        return [ x[labels.lemma] for x in sentence.tokens[f:to] ]


    def getString4TokID(self, s, tokID):
        """Return the correct string for a token ID"""

        if tokID in s.mw:  # this is a MW
            val = s.mw[tokID]
            tokString = " ".join([s.tokens[x][labels.lemma] for x in range(val[1], val[2])])
        else:
            if tokID in s.antecedent:
                tmp = s.antecedent[tokID]
                tokString = " ".join(self.getTokens(tmp[0], tmp[1], tmp[2]))
            else:
                tokString = s.tokens[tokID][labels.lemma]
        return tokString


    def getTokenType(self, s, tokID):
        """Return the type of the token."""

        if s.tokens[tokID][labels.POS][0] == 'N':
            return wtypes.noun
        elif s.tokens[tokID][labels.POS][0] == 'V':
            return wtypes.verb
        return wtypes.unknown


    def getConcepts(self):
        """Returns the concept tuples from the text."""

        res = []
        for s in self.sentences:
            # print out root
            rootData = s.governor_k.get(0, None)
            rootTokenID = rootData[0][0]

            # determine the governor string
            governor = self.getString4TokID(s, rootTokenID)

            # determine the governor type
            governorType = self.getTokenType(s, rootTokenID)

            # get the subject relation
            subjRelID = s.govRelation.get( (rootTokenID, self.getDepID("nsubj")), [])
            for sdep in subjRelID:
                dependent = self.getString4TokID(s, sdep)

                if governorType == wtypes.noun:
                    # print(dependent, "-isA->", governor)
                    res.append( (dependent, 'isA', governor) )
                elif governorType == wtypes.verb:
                    # check for obj:
                    objRelID = s.govRelation.get((rootTokenID, self.getDepID("dobj")), [])

                    #print(objRelID)
                    for obdep in objRelID:
                        # TODO track and aggregate all nmod dependencies in the chain
                        # TODO track and aggregate all amod from nmods in the chain
                        odependent = self.getString4TokID(s, obdep)
                        #print(dependent, "-" + governor + "->", odependent)
                        res.append( (dependent, governor, odependent) )
                        nmodRelID = s.govRelation.get((obdep,self.getDepID("nmod")),[])
                        #print(res,nmodRelID)
        return res


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
            return self.id2dep[idn]
        return 0



class ClauseData():
    """Clause class"""

    def __init__(self):
        self.transitive = False
        self.ditransitive = False
        self.fromToken = -1
        self.toToken = -1
        self.root = -1
        self.matrix = True
        self.finite = True
        self.interrogative = False
        self.passive = False



class SentenceData():
    """This is the main class that holds sentence data.
    """

    def __init__(self):
        self.tokens = [{labels.id: 0, labels.word: 'ROOT', labels.lemma: '', labels.POS: 'ROOT', labels.SPOS: 'ROOT', labels.NER: '', labels.isReferent:False, labels.hasAntecedent:False}]
        self.clauses = [] #: list of ClauseData objects
        self.mood = None
        self.id = None
        self.text = None
        #self.interrogative = False


        # List of dictionaries
        self.token_dict = {}
        #self.dependencies = {}
        self.constituents = []

        # table to hold mapping of internal to our dep labels, int to int
        # key = depID, val is list of tuples (governor, dependent)
        self.depRelDict = {}
        # key = tokenID of governor, val = list of tuples of tokenID of dependent and dependencyID
        self.governor_k = {}
        # key = tokenID of depdendent, val = list of tuples of tokenID of governor and dependencyID
        self.dependent_k = {}
        # key = tuple of tokenID of governor and dependencyID, val = list of dependenceIDs
        self.govRelation = {}

        # Antecedent lookup table, key index of token, val
        self.antecedent = {} #:
        # store multi word expressions, key = tokenID, val = span of mw
        self.mw = {}


    def __str__(self):
        # return (self.data + "\n" + json.dumps(self.d_dict) + "\n" + str(self.t_listofdict))
        res = str(self.id)
        for x in self.tokens:
            res += "\n" + x[labels.word]
        res += "\nGoverning: "
        for x in self.governor_k:
            for y in self.governor_k[x]:
                res += self.tokens[x][labels.word] + ":" + str(y[1]) + ":" + self.tokens[y[0]][
                    labels.word] + " "
        return res


    def getDependencyRoot(self):
        """Returns the root token ID for the dependency parse."""
        return self.governor_k[0][0]


    def getTokens(self, fromt, to):
        """Get a span of tokens (the literal strings) from the sentence."""
        return [x[labels.word] for x in self.tokens[fromt: to]]


    def getLemmas(self, fromt, to):
        """Get a span of lemmata from the sentence."""
        return [x[labels.lemma] for x in self.tokens[fromt: to]]


    def hasScopeOver(self, x, y):
        """Returns True, if X has scope over Y in the phrase structure."""
        pass




if __name__ == "__main__":
    main()
