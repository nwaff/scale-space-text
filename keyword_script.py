__author__ = 'nathanael'

import language_model as lm
import numpy as np
import gauss_filter as gf
from scipy import ndimage
import preprocess as pp
import pickle
import keywords as kw
import matplotlib.pyplot as plt


"""
# Reubuild graph from PMI scores
pmi_scores = pickle.load(open('pmi_scores.p', "rb"))
p_dict = pickle.load(open('pmi_dict_new.p', "rb"))

semantic_graph = lm.dist_dict(p_dict, vocab)
"""

######### Start keyword script here

# Load the semantic graph. The pmi_dict is really
# just used to build the vocabulary list
semantic_graph = lm.load_semantic_graph('semantic_graph.p')

vocab = semantic_graph.keys()

# This is an absolute path! sorry needs to update to read local path.
# filename = '/home/nathanael/IdeaProjects/pointMutualInfo/text_filter2d/didion.txt'
filename = '/home/nathanael/IdeaProjects/pointMutualInfo/text_filter2d/paper_draft.txt'

# Load a text
text = pp.read_textfile(filename)
# Build 2d array from tex
text_array = gf.return_2d_array(text, vocab)

# Making a copy to use in case we want to re-use th original
copy = text_array.copy()

# This is the fixed semantic filter
sigma = .5
iterations = 70
keyword_array2d = kw.build_keyword_array2d(copy, sigma, iterations, semantic_graph)


# get keywords
marginals = kw.marginal_sum(copy, sigma, semantic_graph, axis=0)
keywords = kw.get_sorted_keywords(keyword_array2d, marginals.index, iterations)

cutoff = 40
kw.print_top_keywords(keywords, cutoff)



"""
##------ plotting scripts
##--- Used to create images of the spatial filtering

sigma = 40
filtered = ndimage.filters.gaussian_filter1d(marginals, sigma, order=0)
kws.plot_series(filtered)

##--- Plot kw array -- Shows trace of maxima

gf.plot_text(keyword_array2d)

##### plot with labels
plt.imshow(keyword_array2d, cmap='Greys', interpolation='none')
plt.ylabel('Sigma - filter iteration')
plt.xlabel('Word position')
plt.show()
"""