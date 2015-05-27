__author__ = 'nathanael'

import language_model as lm
import numpy as np
import gauss_filter as gf
from scipy import ndimage
import preprocess as pp


#rebuilding graph
#semantic_graph = lm.rebuild_graph('semantic_graph.p', 'npdict_1mil.p')

#load saved semantic graph
#Would need pickled file for semantic_graph current directory
filename = 'semantic_graph.p'
semantic_graph = lm.load_semantic_graph(filename)


# using a reduced vocabulary
vocab = ['new', 'york', 'time', 'offers', 'free', 'phone', 'gift',
         'shop', 'customer', 'people', 'support', 'city']

sentence = ('New York Time offers free phone as gift for new customer '
            'in new York')

vocab_list = list(set(vocab))

# create 2d array from text and vocabulary
orig_df = gf.return_2d_array(sentence, vocab)
# show original plot
gf.plot_text(orig_df)


copy_df = orig_df.copy()

# filter to sigma = 2
sigma = 1
filtered_df = gf.filter_text(copy_df, semantic_graph, sigma)
# plot smoothed text
gf.plot_text(filtered_df)


