#!/usr/bin/python3
''' A collection of helper functions for Reddit Information Distillery. '''
from collections import Counter # Allows combining dicts while adding values
import math        # math.log()
import string      # string.maketrans(), string.punctuation
import re          # regular expressions

STOPWORDS_FILE = "stopwords.txt"

def load_stopwords(query):
    ''' Get list of stopwords from text file where each word is delimited by a
        new line.

        Returns a list of stopwords, including the supplied query string. '''
    try:
        stopfile = open(STOPWORDS_FILE, mode='r')
    except IOError:
        sys.exit("Cannot open stopwords file.")
    else:
        stopwords = [' ']
        for line in stopfile:
            stopwords.append(line.rstrip('\n'))
        stopfile.close()

    for word in query.lower().split():
        stopwords.append(word)

    return stopwords

def normalize_string(comment, stopwords):
    ''' Normalize the text as such:
            Remove common words and query ("is," "the, "etc.")
            Convert words to lowercase.
            Remove punctuation.

        Returns a list of individual words in comment.'''
    comment = comment.lower().split()
    words = [w.strip(string.punctuation) for w in comment if w not in stopwords]

    # Remove empty strings
    words = list(filter(None, words))
    return words

def term_frequency(termlist, word_count):
    ''' Calculate the term frequency of words within the collection of comments.
        Input is a Counter dict of keys (terms) and values (number of
        appearances) and the word count for the collection.

        Computes the term frequency as follows:
        Number of appearances of word within the collection /
        Word count for the collection.

        Returns another Counter with each word and its TF value.
    '''
    cnt = Counter()
    if (word_count != 0):
        for key, value in termlist.items():
            cnt[key] = value / word_count
    else:
        print("TF attempted to divide by 0.\n")
    return cnt



def inverse_document_frequency(termlist, total_comments):
    ''' Input is a Counter dictionary of frequency of unique appearances within
        each comment in a body of comments (words found multiple times in a
        single comment are only counted once) and total number of comments.
        Output a dictionary of the inverse document frequency of terms

        Compute the inverse term frequency as follows:
        Ln(Total number of documents /
              Number of documents containing term t)

        Returns another Counter with each word and its TF value.
    '''
    cnt = Counter()
    if (total_comments != 0):
        for key, value in termlist.items():
            cnt[key] = math.log(total_comments / value)
    else: #divide by 0
        print("IDF attempted to divide by 0.\n")
    return cnt
