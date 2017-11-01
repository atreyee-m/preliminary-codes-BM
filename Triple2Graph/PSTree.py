#!/usr/bin/env python
#
# (C) 2017 by D. Cavar <damir@cavar.me>, ...
# Add Apache License 2 code here

"""
PSTree.py

(C) 2017 by D. Cavar <damir@cavar.me>, ...

Add Apache License 2 code here

Created: 2017-07-05 by D. Cavar
Changed: 2017-07-05 by D. Cavar
         2017-07-07 by A. Mukherjee

This class is encoding an acyclic phrase structure tree in a data-structure that contains only immediate dependency
relations.

For fast lookup we map the immediate dependency relations on a helper data structure that contains all dependency
relations in the resulting tree.

API notes

Status

Assumptions:

All trees are acyclic.
There is no theoretical restriction on the number of daugthers of a node.
"""

import LingData
#import re


__license__ = """Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""
__revision__ = " $Id: PSTree.py 2 2017-07-25 14:32:00Z damir $ "
__docformat__ = 'reStructuredText'
__author__ = 'Damir Cavar <damir@cavar.me>, Atreyee M.'
__version__='0.1'



def main():
    pst = PSTree()
    #data = '(ROOT  (S (NP (NNP Mary)) (VP (VBD said)   (SBAR (IN that)  (S (NP (NNP John)) (VP (VBZ is)   (ADJP (JJ stupid)))))) (. .)))'
    #data = "(ROOT  (S (S   (NP (NN TC))   (VP (VBZ is)  (NP (NP (DT the) (NN CEO)) (PP (IN of)   (NP (NNP Apple)))))) (CC and) (S   (NP (NNP BK))   (VP (VBZ is)  (NP (NP (DT the) (NN CEO)) (PP (IN of)   (NP (NNP Google)))))) (. .)))"
    #data = ""
    #pst.parseBrackets(data)
    #x = list(pst.parseBrackets(data))
    #print(x)
    # for i in x:
    #     print(i)


class PSTree():
    dominance = {}

    idominance = {}

    nodelabels = {}  # key is ID, value is label

    nodeIDs = {}  # key is string, value is ID

    root = -1

    def __init__(self):
        pass

    def __str__(self):
        pass

    def __len__(self):
        pass

    def __repr__(self):
        pass

    def __iter__(self):
        pass

    def getID(self, label):
        """Return the ID for a label."""
        if label in self.nodeIDs:
            return self.nodeIDs[label]
        self.nodeIDs[label] = len(self.nodeIDs) + 1
        return self.nodeIDs[label]

    def getLabel(self, ajdee):
        """Return label for ID."""
        return self.nodelabels.get(ajdee, None)

    def hasScopeOver(self, x, y):
        """   """
        return True

    def parseBrackets(self):
        """
        Map bracketted annotation to the internal tree representation.
        
        """

        pass

    def getClauses(self, data):
        """
        get clauses from a sentence using the constituency tree
        in progress...
        """


        print("inside getClauses.........")
        stk = []  # using stack
        l = []
        for i, j in enumerate(data):
            if (j == '('):
                stk.append(i)
            elif (j == ')' and len(stk) != 0):
                match_brac = stk.pop()
                #print(data[match_brac+1:i])
                l.append(data[match_brac+1:i])
                #print(data[match_brac + 1: i])
                #yield (len(stk), data[match_brac + 1: i])
        #print(l)
        l = ["(" + i for i in l]
        #print(l)
        #print("original list", l)
        #print("removed ones ................")
        lst = []

        result = []
        # for i in l:
        #     i = re.sub('[ \t\n]+',' ',i)
        #     pattern = re.compile(r"^(?!\(S \(S |\(ROOT )")  #\(S((?!\(ROOT).)*$
        #     #print(pattern)
        #     if(pattern.search(i)):
        #         #print(i)
        #         #lst.append(i)
        #         i = re.sub(pattern,'',i)
        #         #print(i)
        #         patt = re.compile(r"^\(S ")
        #         if(patt.search(i)):
        #             print(i)


                # for i in lst:
        #     print(i)

    def dominates(self, x, y):
        """Does X dominate Y?"""
        return True

    def CCommands(self, x, y):
        """Does X c-command Y?"""
        return True

    def isTerminal(self, x):
        """Is X a terminal?"""
        return True

    def getBrackets(self):
        return ""

    def getJSON(self):
        return ""


if __name__ == "__main__":
    main()
