# What has been done so far and what needs to be done

## NLP component
  - Generic data structure for reading Stanford dependency parser/spacy output (LingData.py)
  - It needs to be done for Spacy
  - Specific parser to parse XML output of Stanford CoreNLP output
  - parses tokens, dependencies from corenlp xml output
  - stores it into a dictionary data structure
  - coreference resolution
  - considers nsubj and dobj relations only for now
  - need to consider relations like ccomp, nmod, compounds, etc.
  - *Parsing of the constituency tree and figuring out the relevant information*

## from NLP component to mapping to graph DB
  - functions to add node, labels, relations and attributes
  - Since isA relation is implemented in the NLP component. 
    - When this comes in to the neo4j component, it is treated as a label of a node.
    - NLP component gives out triples. The subject is treated as node and the obj as the attribute
  - For now, rest are treated as relations. 
    - Example - ('Tim Cook', 'own', 'Google')
    - If 'Tim Cook' and  'Google' nodes are not present, they are created and the 'own' relation is added.
 
  
  

