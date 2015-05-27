__author__ = 'nathanael'

import numpy as np
from scipy import stats
import preprocess as pp
import pandas as pd
import matplotlib.pyplot as plt
from scipy import ndimage


def filter_text(text_df, semantic_graph, sigma):
    """
    Filter on over the spatial and semantic domain
    with the given sigma
    :param text_df:
    :param semantic_graph:
    :param sigma:
    :return:
    """
    semantic_filter(text_df, semantic_graph, sigma)
    spatial_filter(text_df, sigma)
    return text_df


def spatial_filter(text_df, sigma, derivative=0):
    """
    Filters the given values with the 1D Gaussian kernel
    for a given sigma
    :param text_df: A pandas series
    :param sigma: Filter window
    :param derivative: Made available if filtering on
    a derivative of the Gaussian
    :return:
    """
    vals = text_df.values
    for i in range(len(vals)):
        vals[i] = ndimage.filters.gaussian_filter1d(vals[i], sigma, order=derivative)


def plot_text(text_df):
    """
    Wraps pyplot imshow()
    :param text_df:
    :return:
    """
    plt.imshow(text_df, cmap='Greys', interpolation='none')
    plt.show()


def return_2d_array(text, unique_list):
    """
    Build's 2d binary array from text where unique_list is a
    vocabulary on the y-axis and text determines the
    position of each word on the x-axis.
    :param text: The text file to convert to a 2d binary array
    :param unique_list: A vocabulary list defining the semantic
    axis
    :return:
    """
    words = pp.prep_text(text)
    unique_txt = set(words)
    # Make sure words in text are in the vocabulary
    unique_union = list(unique_txt.union(unique_list))
    text_img = np.zeros((len(unique_union), len(words)))
    df_img = pd.DataFrame(text_img, index=unique_union, columns=words)
    for i in words:
        df_img.loc[i, i] = 1
    return df_img


def gaussian_filter(graph, word, sigma):
    """
    Applies a gaussian filter to the array of neighbors
    for the given word in a semantic graph. The graph
    is represented as a dictionary with keys as words
    and values being an structured array of types (word, distance).
    :param graph: The semantic graph
    :param word: The word to filter
    :param sigma: The filter window
    :return:
    """
    freq_arr = get_neighbors(graph, word)
    #get smoothed kernel basd on graph of neighbors
    word_signal = np.zeros(len(freq_arr['freq']))
    #all filtering takes place with on the original 1,0 signal
    word_signal[0] = 1
    kernel = get_kernel(freq_arr['freq'], sigma)
    word_signal = np.convolve(kernel, word_signal)
    word_signal = word_signal[:len(freq_arr)]
    return word_signal


def get_kernel(arr, sigma):
    """
    :param arr:
    :param sigma:
    :return:
    """
    ker = np.zeros(len(arr))
    for i in range(len(arr)):
        ker[i] = stats.norm.pdf(arr[i], 0, sigma)
        #print ker[i]
    return ker


def get_neighbors(graph_dict, word):
    """
    Return the array of neighbors for a given word
    sorted by distance from the the word.
    :param graph_dict: representation of the semantic
    graph
    :param word: word being retrieved
    :return: Returns an structured array of type
     ('word', 'freq') for the given word, (0 otherwise: TODO)
    """
    if word in graph_dict:
        col = graph_dict[word].copy()
        col.sort(order='freq')
        return col
    else:
        col = np.array([1, 0, 0])
    return col


def semantic_filter(text_df, graph, sigma):
    """
    Takes a binary text data frame and applies a
    gaussian filter to each word based on the
    words neighbors in the semantic graph.
    :param text_df: Binary text array with vocabulary
        positions represented by the y coordinate
    :param graph: The semantic graph
    :param sigma: The filter window
    :retrun: Returns the binary data frame with the
        smoothed values
    """
    col_index = text_df.columns
    for word in col_index:
        if word in graph:
            neighbors = get_neighbors(graph, word)
            smoothed = gaussian_filter(graph, word, sigma)
            for index in range(len(neighbors)):
                word_index = text_df.index
                if neighbors['word'][index] in word_index:
                    text_df.loc[neighbors['word'][index], word] = smoothed[index]
                  #DB  print(smoothed[index])
        else:
            text_df.loc[word][word] = stats.norm.pdf(1, 1, sigma)
    return text_df

