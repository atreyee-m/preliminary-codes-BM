# Python to Triple Store and Graph DB


## Connecting to Neo4J

Install the driver using pip:

	pip3 install neo4j-driver



## Master-Plan

The output concepts from the LingData and NLP-component processing have to be wrapped into an API-class.

The API-class has to be mapped to a graph representation:

- Neo4J
- Stardog

We need a test-frontend as a web-form to provide a user interface to the NLP components and:

- form element to submit text
- output of concepts extracted, with relations to other concepts
- view button to see the Graph-DB output or result

The GraphDB should be erasable. That means dropping everything to restart the graph.

We will later add the switches to see the output of competing NLP pipelines.



## Dependency Labels

TODO Please correct the list. It is taken from this paper:

[https://nlp.stanford.edu/pubs/USD_LREC14_paper_camera_ready.pdf](https://nlp.stanford.edu/pubs/USD_LREC14_paper_camera_ready.pdf)


Core dependents of clausal predicates
Nominal dep
- nsubj
- nsubjpass
- dobj
- iobj

Predicate dep
- csubj
- csubjpass
- ccomp / xcomp


Non-core dependents of clausal predicates
Nominal dep
Predicate dep
Modifier word
advcl
advmod
nfincl
neg
nmod
ncmod
Special clausal dependents
Nominal dep
Auxiliary
Other
vocative
aux
mark
discourse
auxpass
punct
expl
cop
Coordination
conj
cc
Noun dependents
Nominal dep
Predicate dep
Modifier word
nummod
relcl
amod
appos
nfincl
det
nmod
ncmod
neg
Compounding and unanalyzed
compound
mwe
goeswith
name
foreign
Case-marking, prepositions, possessive
case
Loose joining relations
list
parataxis
remnant
dislocated
reparandum
Other
Sentence head
Unspecified dependency
root
dep



## Translation Rules


If a ROOT has "nsubj":
- it could also have a dobj (transitive verb)
- it could also have a iobj (di-transitive construction)
- the iobj could be realized as nmod with to (also ditransitive)
- if no dobj then this could be intransitive
- if ccomp to embedded ROOT, then it is a verb with a sentential complement (e.g. *say* in *Mary said that John is stupid.*)
- if xcomp to embedded ROOT, then it is a verb with an infinitival sentenial complement (e.g. *want* in *Mary wants t ocall John.*)


The sentence could have a verbal ROOT:

- It is a sentence with a transitive or intransitive verb.
- An active sentence with a transitive or intransitive verb has to have a *nsubj* dependency. Set the feature of the sentence to *+active*.
- A passive sentence with a transitive or intransitive verb has to have a *nsubjpass* dependency. The target of this dependency is the semantic object, but the syntactic subject. We set the feature for the sentence to *-active* or *+passive*.
- If the sentence has a *iobj* dependency, this is a ditransitive verb. The target of *iobj* is the indirect object. The indirect object could be also depending on ROOT as an nmod with to. The implicature is that we need to check whether the verb is a true ditransitive.
- Indirect or direct objects could be the *nsubjpass*, which means that they are the semantic direct or indirect object, but the syntactic subject.
- If the predicate is passive, the directionality of the relation is reversed, e.g. *Tim Cook owns Apple.* is *Tim Cook -own-> Apple*, while *Apple is owned by Tim Cook.* is not *Apple -own-> Tim Cook.*

- *have* as the ROOT is a special case!


The sentence could have a nominal ROOT:

- The construction could be a copula constructions, in which case there should be a *cop* dependency from the ROOT node. This is something like *Tim Cook is the CEO of Apple.* In this case ROOT is *CEO*.
- We do not expect an *nsubjpass* dependency here, that is, copula constructions are not occurring passivized.
- ...


The sentence could have an adjectival ROOT:

- The construction should have a copula dependency to the copula.
- We do not expect an *nsubjpass* dependency here, that is, copula constructions are not occurring passivized.
- The *nsubj* is the syntactic and semantic subject.

#### Revised Translation Rules 

Determining transitivity:
- If the ROOT has nsubj:
     - If the ROOT has a dobj:
        - If the ROOT has an iobj, then set Ditransitive to True
            - If it has an nmod, look up the verb to see if it is ditransitive. If it is, set Ditransitive = True.
        - Else, Transitive = True (and Ditransitive = False)
     - If the ROOT has no dobj, then Transitive and Ditransitive are both False (i.e., Intransitive = True).


This far we are processing only main clauses!

Here now we have to describe clause types and embeddings.


Then, in the next step we have to map implicatures, as for example:

- The sentence *Tim Cook is the CEO of Apple.* implies that *Tim Cook -worksFor-> Apple*, explicit is *Tim Cook -hasRole-> CEO*
- The sentence *Tim Cook has experience in corporate law.* implies that ...


### Constructions

We need to map constructions, formulaic or idiomatic expressions to representations, including implicatures.





### CoreNLP dependency parser mapping specifics


