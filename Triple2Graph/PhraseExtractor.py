__author__ = 'atreyee'

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
from corenlp_pywrap import pywrap
import os,os.path, sys, glob
from Triple2Graph.CoreNLPXMLParser import *



def main():
    ext = Extractor()
    ext.conn()


class Extractor():

    def conn(self):
        annotator_list = ["tokenize", "cleanxml", "ssplit", "pos", "lemma", "ner"]
        #dir = os.listdir('/home/atreyee/PycharmProjects/BusinessMining/Triple2Graph/input_sentences/')
        for i in glob.glob('/home/atreyee/PycharmProjects/BusinessMining/Triple2Graph/input_sentences/*.txt'):
            #print(i)
            data = self.readFile(i)
            cn = pywrap.CoreNLP(url='http://156.56.14.247:9000') #, annotator_list=annotator_list)  # 149.161.139.120
            out = cn.basic(data, out_format='xml')
            root = ET.fromstring(cn.basic(data, out_format='xml').text)
            #print(out.text)
            r = self.parseNERs(root)
            print(r)


        # data = self.readFile("newsent.txt")
        # cn = pywrap.CoreNLP(url='http://156.56.14.247:9000', annotator_list=annotator_list)  # 149.161.139.120
        # out = cn.basic(data, out_format='xml')
        # root = ET.fromstring(cn.basic(data, out_format='xml').text)
        # #print(out.text)
        # r = self.parseNERs(root)
        # print(r)

    def parseNERs(self,root):
        var_date = []; var_money = []

        for iner in root.findall('.//tokens/*'):
            if(iner.find('NER').text == 'DATE'):
                #var_date.append(iner.find('word').text)
                var_date.append(iner.find('NormalizedNER').text)
            elif(iner.find('NER').text == 'MONEY'):
                var_money.append(iner.find('word').text)
        return (" ".join(str(x) for x in set(var_date))+'\t'+" ".join(str(x) for x in var_money)+'\n')




    def readFile(self,filename):
        with open(filename) as f:
            file = f.read()
        return (file)


if __name__ == "__main__":
    main()