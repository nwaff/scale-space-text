Script overview
=======

NOTE: The text file names included in the script are
absolute filepaths and would need to be updated match
your file path in order to run.
The corpus used to build the initial pointwise
mutual innformation(PMI) graph
is not included and would need to be rebuilt 
using the build_graph_script.

The paper describing this project is included in the
repo under the title scale_draft1.pdf.
The original paper is here: http://arxiv.org/abs/1212.2145

The main functions are separated into several modules.
Use of the modules is demonstrated in the _script
files


Text files:
------
didion.txt :
     a clip from a book review
paper_draft.txt :
    a draft of the paper handed in with this project

Modules
------
preprocess: routines based on the
    NLTK library for tokenizing and cleaning text.

language_model: functions used to build a semantic graph
    based on pointwise mutual information.

gauss_filter: is used for filtering or smoothing over
    either 1D or 2D binary representations of text.

keyword: contains functions for building a list of
    keywords from a filtered text.


Scripts
-----

build_graph_script.py
    Demonstrates building a graph based on a text file.
    It can take 10-20 minutes to build a graph based
    on a moderate sized corpus

small_vocab_test.py
    Demonstrates filtering on a reduced vocabulary. This
    enables the result to be visualized, since using
    on a full vocabular can make the semantic axis
    much greater than the spatial axis (x).

keyword_script.py
    This script demonstrates extracting keywords from
    a moderate-sized text


Data
------
In the current scripts data is loaded from the semantic_graph.p
file which has around 82,000 bigrams with 16,000 unique words.

