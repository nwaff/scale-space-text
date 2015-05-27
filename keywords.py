__author__ = 'nathanael'

import gauss_filter as gf
from scipy import ndimage
import numpy as np
from operator import itemgetter
import pandas as pd
import matplotlib.pyplot as plt

def get_keywords(keyword_array2d, word_list, iteration):
    """
    TODO: Include position of max
    Returns a dictionary of the form (word, iteration)
    where iteration is the smoothing level at which the
    word first appears when retracing steps from coarse
    to fine smoothing
    :param keyword_array2d: Matrix indicating relative maxima
     of words during each iteration of smoothing
    :param word_list: list of words
    :param iteration: Number of iterations in smoothing
    :return: dictionary of form (word, iteration)
    """
    words = {}
    for row in range(iteration+1):
        # TODO: group keywords by levels
        nums = np.where(keyword_array2d[iteration - row] == 1)[0]
        current_dict = {}
        for key in nums:
            if key in words:
                entry_level = words[key][1]
                current_dict[key] = (word_list[key], entry_level, key)
            elif key+1 in words:
                entry_level = words[key+1][1]
                current_dict[key] = (word_list[key], entry_level, key)
            elif key-1 in words:
                entry_level = words[key-1][1]
                current_dict[key] = (word_list[key], entry_level, key)
            else:
                current_dict[key] = (word_list[key], iteration-row, key)
        words = current_dict.copy()
        current_dict.clear()
    return words


def get_sorted_keywords(array2d, word_list, iterations):
    """
    Returns sorted list of tuples of form (word, iteration)
    where iteration is the smoothing level at which the word
    first appears
    :param array2d:
    :param word_list:
    :param iterations:
    :return:
    """
    keywords = get_keywords(array2d, word_list, iterations)
    sorted_keywords = sorted(keywords.values(), key=itemgetter(1), reverse=True)
    return sorted_keywords


def build_keyword_array2d(text, sigma, iterations, semantic_graph):
    """
    TODO: could be more efficiently represented as a sparse matrix (dictionary,etc.)
    Creates a binary 2d array where in each row a 1 represents the position
    of a relative maxima at that level of smoothing
    :param text: The text which is to be keyworded
    :param sigma: Fixed sigma for smoothing on the semantic graph
    :param iterations: Number of smoothing iterations
    :param semantic_graph: The semantic graph to be used for smoothing
    :return:
    """
    sem_filter = gf.semantic_filter(text, semantic_graph,sigma)
    # After the semantic fitler the marignal values
    marginal_sum = sem_filter.sum(axis=0)
    keyword_array2d = laplace_filter(marginal_sum, iterations, increment=0.2)
    return keyword_array2d


def marginal_sum(text, sigma, semantic_graph, axis=0):
    """
    Returns the marginal sums across the semantic domain
    after smoothing with a fixed sigma
    :param text: The 2d text array
    :param sigma: parameter for smoothing in the semantic domain
    :param semantic_graph: The graph used for smoothing in the semantic
    domain
    :param axis: axis to sum over
    :return: a 1d array of marginal sums
    """
    sem_filter = gf.semantic_filter(text, semantic_graph, sigma)
    marginal_sum = sem_filter.sum(axis=0)
    return marginal_sum


def laplace_filter(marginals, iterations, increment=0.2):
    """
    Creates a 2d binary array where 1's represent the position
    of relative maxima. Could be made sparse but this was used
    in order to create image of maxima
    :param marginals: The marginals over the semantic domain
    after smoothing by some sigma
    :param iterations: Number of iterations of smoothing
    :param increment: Increment of smoothing for each iteration
    :return:
    """
    maxima = relative_maxima2(marginals)
    array1d = binary_array(maxima, len(marginals))
    array2d = array1d.reshape(1, len(marginals))
    sigma = 0
    for index in range(iterations):
        sigma += increment
        filtered = ndimage.filters.gaussian_filter1d(marginals, sigma, order=1)
        maxima = relative_maxima(filtered)
        bin_array = binary_array(maxima, len(marginals))
        bin_2d = bin_array.reshape(1, len(bin_array))
        ## TODO (dead code)
        if index == 0:
            temp = np.concatenate((array2d, bin_2d), axis=0)
        else:
            temp = np.concatenate((temp, bin_2d), axis=0)
    return temp


def relative_maxima(input):
    """
    return indices of the relative maxima in input array
    :param input: An array filtered with the first-order
    gasussian derivative
    :return: array of indicees of relative maxima in array
    """
    zeros = np.where(np.diff(np.sign(input)) < -1)
    return zeros


def relative_maxima2(arr):
    """
    Return relative maxima of a 1d array.
    TODO: Update to Python for relmaxima function
    :param arr: The array to filter
    :return: an array with the indices of the relative maxima
    """
    maxima = np.array([], dtype=np.int)
    for i in range(len(arr)):
        if i == 0 and arr[1] < arr[0]:
            maxima = np.append(maxima, i)
        elif i < len(arr) - 2:
            if arr[i] > arr[i-1] and arr[i] > arr[i+1]:
                maxima = np.append(maxima, i)
        elif i == len(arr)-1:
            if arr[i] > arr[i-1]:
                maxima = np.append(maxima, i)
    return maxima


def print_top_keywords(keyword_list, cut_off):
    for k,v, i in keyword_list:
        if v > cut_off:
            print 'word: ', k, 'level: ', v, 'index: ', i


def binary_array(index_arr, length):
    """
    Creates a binary row of length length given the an array of
    indices
    :param index_arr: An array of indices
    :param length: Length of array to create
    :return:
    """
    bin_array = np.zeros(length, dtype=np.int)
    for index in index_arr:
        bin_array[index] = 1
    return bin_array


## some utility functions

def plot_series(array):
    ts = pd.Series(array)
    ts.plot()
    plt.show()


def print_list(zeros, df):
    columns = df.columns
    for i in range(len(zeros)):
        print columns[zeros[i]]

a
