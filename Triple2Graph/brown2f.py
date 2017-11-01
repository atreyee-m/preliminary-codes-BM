#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


"""
brown2f.py

(C) 2017 by Damir Cavar <damir@cavar.me>

This module provides a function to convert a Brown-corpus tag into a feature structure.

"""

import sys, csv
from collections import namedtuple

FStructure = namedtuple('FStructure', ['category', 'subcategory', 'features'])
Features = namedtuple('Features', ['gender', 'number', 'person', 'tense', 'interrogative', 'negation', 'case'])


tagComboDict = {
    'AP+AP': (('many-much',), ('AP', 'AP'), ('many', 'much')),
}

def tag2f(tag, token):
    """ """
    pass


def printFeatures(fStruct):
    """ """
    feat = fStruct.features
    print(", ".join((fStruct.category, fStruct.subcategory, ", ".join(feat.gender, feat.number, feat.interrogrative))))


def _procTag2f(tag, token):
    """ """
    if tag == 'WRB+MD' and token == "where'd":
        result = []
        result += _procTag2f("WRB", "where")
        result += _procTag2f("MD", "'d")
        return (tuple(result))
    myFeatures = Features.__new__.__defaults__ = (None,) * len(Features._fields)
    myFeatureStructure = FStructure.__new__.__defaults__ = (None,) * len(FStructure._fields)
    if tag == "WRB":
        myFeatures.interrogative = True
        myFeatureStructure.category = "Adv"
        myFeatureStructure.features = myFeatures
        return ((myFeatureStructure,))
    if tag == "MD":
        myFeatureStructure.category = "V"
        myFeatureStructure.subcategory = "modal"
        myFeatureStructure.features = myFeatures
        return ((myFeatureStructure,))
    myFeatureStructure.features = myFeatures
    myFeatureStructure.category = tag
    return ((myFeatureStructure,))


def _convert(btag, token, features):
    """ """
    msubtag = ""
    if btag == "ABL" and token == "quite":
        mtag = "Adv"
    elif btag == "ABN" and token in ('all', 'half', 'many', 'nary'):
        # PRON	PreQuant			all half many nary	determiner/pronoun, pre-quantifier
        msubtag = "PreQuant"
        mtag = 'Pron'
    elif:
        return ((btag, mtag, msubtag, token, features))


def main():
    """
    Main function for testing the conversion script.
    :return:
    """
    # key = Brown tag, value = set of FStructure
    # tag2f = {}
    # structs for the value

    with open('BrownTagsetTranslation.csv', newline='') as csvfile:
        myreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in myreader:
            print(', '.join(row))
            # print(tuple(row[0].split('+')))
            btag = row[0]
            print("btag:", btag)
            mtag = row[1]
            if mtag == "#NULL":
                mtag = ""
            print("mtag:", mtag)
            msubtag = row[2]
            print("msubtag:", msubtag)
            features = row[3]
            tokens = row[4].split()
            print("tokens:", tokens)

            for x in tokens:
                print("x:", x)
                result = _convert(btag, mtag, x, features)
                print("result:", result)
                for y in result:
                    print("y:", y)
                    # printFeatures(y)


if __name__ == "__main__":
    main()
