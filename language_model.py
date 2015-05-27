__author__ = 'nathanael'


import nltk
from math import log
from operator import itemgetter
import numpy as np
import preprocess as pp
import pickle
from nltk.collocations import *

# Class not used
class LanguageModel:
    def __init__(self, semantic_graph):
        self.semantic_graph = semantic_graph
        self.word_list = semantic_graph.index.values


def load_semantic_graph(filename):
    """
    Loads prebuilt semantic_graph with
    filename = file
    :return: semantic_graph
    """
    semantic_graph = pickle.load(open(filename, 'rb'))
    return semantic_graph


def rebuild_graph(save_file, open_file):
    """
    Rebuilds semantic graph given saved npi_dict
    and bigram_distribution
    :param save_file  filename to save graph
    :param open_file filename of npi dict
    :return:
    """
    try:
        pmi_dict = pickle.load(open(open_file, "rb"))
        unique_list = unique_words(pmi_dict)
        semantic_graph = dist_dict(pmi_dict, unique_list)
        pickle.dump(semantic_graph, open(save_file, "wb"))
    except IOError:
        print 'Invalid file'
    return semantic_graph


def create_graph_from_text(text, count_filter, filename):
    """
      Same as create_graph_from_words but with built in
      text processing
    """
    words = pp.prep_text(text)
    semantic_graph = create_graph_from_words(words, count_filter, filename)
    return semantic_graph


def create_graph_from_words(words, count_filter, filename):
    """
    Creates semantic_graph from words. All bigrams with
    a count lower than count_filter are removed.
    Builds dictionary of pmi_scores from which
    the semantic_graph is built. The graph keys are
    words and the value is a structured array of
    type ('word', 'freq') which records all neighboring
    words 'normalized' PMI value.
    """

    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(words)
    # Remove bigrams with less than filter count
    finder.apply_freq_filter(count_filter)
    pmi_scores = finder.score_ngrams(bigram_measures.pmi)
    # get bigram distribution
    # bigram_dist = nltk.FreqDist(nltk.bigrams(words))
    pmi_dict = build_pmi_dict(pmi_scores)
    unique_list = unique_words(pmi_dict)
    semantic_graph = dist_dict(pmi_dict, unique_list)
    pickle.dump(semantic_graph, open(filename, "wb"))
    return semantic_graph


def unique_words(pmi_dict):
    """
    Create list of uniqe words from
    pmi_dict keys.
    :param pmi_dict: Dictionary of k=words, v=PMI
    :return:unique word list
    """
    #pmi_dict = pickle.load(open(open_file, "rb"))
    list1 = set(e[1] for e in pmi_dict.keys())
    list2 = set(e[0] for e in pmi_dict.keys())
    unique_list = list(list1.union(list2))
    return unique_list


## new dictionary function
def dist_dict(pmi_dict, word_list):
    """
    Function returns a dictionary of
    structured arrays with 'word', 'freq'
    entries for each bigram in the
    dictionary of pmi frequencies -- pmi_dict
    The word_list is set of words from the dictionary
    (and could be created within the function)
    :param pmi_dict: dictionary with bigram keys and
    frequency values
    :param word_list:
    :return:
    """
    sparse_dict = {}
    for a in word_list:
        keycount = 0
        freq_list = [(a, 0)]
        for b in word_list:
            if a != b:
                key = (a, b)
                if key in pmi_dict:
                    keycount += 1
                    freq_list.append((b, pmi_dict[key]))
            if keycount > 0:
                # note -- word length limited to 60
                sparse_dict[a] = np.array(freq_list,
                                          dtype=[('word', 'a40'), ('freq', 'f4')])
    return sparse_dict



# return a dictionary of normalized pmi with
# bigrams as keys and normalized pmi as values
def build_pmi_dict(pmi_scores):
    """
    Returns a dictionary with key(bigrams)
    and value frequencies. The frequencies have
    been constrained to the 0,4 range.
    TODO: (Mostly this removes punctuation bigrams
    which should be handled earlier and converts
    to a dictionary. Possibly redundant if conversion
    can be direct to the 'graph' dictionary).
    :param pmi_scores:
    :return:
    """
    # Testing with out scaling
    distance_graph = {}
    max_val = max(pmi_scores,key=itemgetter(1))[1]
    for (a, b), v in pmi_scores:
        if a.isalpha() and b.isalpha() and v > 0:
            #dist = v/max_val
            #dist = 8 - (8*pmi)
            dist = max_val - v
            distance_graph[(a, b)] = dist
    return distance_graph


