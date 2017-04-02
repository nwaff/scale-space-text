__author__ = 'nathanael'
'''
Most functions based on github.com/bdewilde/toolbox
'''

import nltk
import string
import re
from nltk.corpus import stopwords
import string


def read_textfile(filename):
    text = ''
    try:
        f = open(filename)
        text = f.read()
        f.close()
    except IOError:
        print 'Invalid file'
    return text


def prep_text(text):
    text = clean_text(text)
    words = tokenize(text)
    words = remove_stopwords(words)
    return words


def clean_text(text):
    """Removes digits, non-standard white space, URLs, and non-Ascii from raw text.
    """
    text = text.lower()              # remove capitalization
    text = re.sub('\d', ' ', text)   # remove digits
    text = re.sub('\s+', ' ', text)  # standardize white space
    text = remove_urls(text)         # remove all urls
    text = remove_non_ascii(text)    # remove all non-ascii characters
    text = text.translate(string.maketrans("", ""), string.punctuation)
    return text


def clean_and_tokenize(text):
    """Removes digits, non-standard white space, URLs, and non-Ascii from raw text.
        *redundant*
    """
    text = text.lower()              # remove capitalization
    text = re.sub('\d', ' ', text)   # remove digits
    text = re.sub('\s+', ' ', text)  # standardize white space
    text = remove_urls(text)         # remove all urls
    text = remove_non_ascii(text)    # remove all non-ascii characters
    text = text.translate(("", ""), string.punctuation)
    words = tokenize(text)
    words = remove_stopwords(words)
    return words



# redundant
def clean_words(words):
    """Removes digits, non-standard white space, URLs, and non-Ascii from raw text.
    """
    words = words.lower()              # remove capitalization
    text = re.sub('\d', ' ', text)   # remove digits
    text = re.sub('\s+', ' ', text)  # standardize white space
    text = remove_urls(text)         # remove all urls
    text = remove_non_ascii(text)    # remove all non-ascii characters
    text = text.translate(None, string.punctuation)
    words = tokenize(text)
    words = remove_stopwords(words)
    return words


def tokenize(text):
    return nltk.wordpunct_tokenize(text)


def remove_stopwords(words):
    stops = set(stopwords.words('english'))
    return [w for w in words if w not in stops]


def remove_punctuation(text):
    text = text.translate(string.maketrans("", ""), string.punctuation)
    return text


def unique_list(words):
    return list(set(words))


def words_to_dict(words):
    word_dict = {}
    for i in range(len(words)):
        word_dict[words[i]] = i
    return word_dict


def remove_non_ascii(s):
    """Removes all non-ascii characters from input string.
    """
    return "".join(c for c in s if ord(c) < 128)



def remove_urls(s):
    """Removes all URLs from input string.
    """
    pattern = r'((http|ftp|https):\/\/)?[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?'
    return re.sub(pattern, ' ', s)


