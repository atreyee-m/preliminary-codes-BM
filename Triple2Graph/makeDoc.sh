#!/bin/sh
for x in LingData spacyRPCClient spacyRPCServer CoreNLPXMLParser neo4j_ops
do
	pydoc3 -w $x
done
 
