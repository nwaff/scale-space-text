__author__ = 'nathanael'


import language_model as lm
import preprocess as pp

# Note : this process can takes about 15-20 mins for 1-4mil words
# Building graph from a corpus
filename = "path to corpus"
f = open(filename)
text = f.read()
f.close()
words = pp.prep_text(text)
#If limiting the number of words
#part_words = words[: 1000000]

# filter bigrams < 3 in count
bigram_filter = 3
# build the semantic graph and pickle to file 'semantic_graph_2.p'
semantic_graph = lm.create_graph_from_words(words, 3, 'semantic_graph_2.p')

# rebuild graph based on saved PMI dict
# semantic_graph = lm.rebuild_graph('semantic_graph_2.p', 'npdict_1mil.p')



