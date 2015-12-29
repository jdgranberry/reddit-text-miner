#!/usr/bin/python3
''' A collection of helper functions for Reddit Information Distillery. '''
from collections import Counter # Allows combining dicts while adding values
import math        # math.log()
import string      # string.maketrans(), string.punctuation
import re          # regular expressions

STOPWORDS_FILE = "stopwords.txt"

def load_stopwords():
    ''' Get list of stopwords from text file where each word is delimited by a
        new line.

        Returns a list of stopwords. '''

    try:
        stopfile = open(STOPWORDS_FILE, mode='r')
    except IOError:
        sys.exit("Cannot open stopwords file.")
    else:
        stopwords = [' ']
        for line in stopfile:
            stopwords.append(line.rstrip('\n'))
        stopfile.close()

    return stopwords

def normalize_string(comment, stopwords, query):
    ''' Normalize the text as such:
            Remove common words and query ("is," "the, "etc.")
            Convert words to lowercase.
            Remove punctuation.

        Returns a list of individual words in comment.'''
    comment = comment.lower().split()
    words = [w.strip(string.punctuation) for w in comment if w not in stopwords]

    return words


def inverse_document_frequency(termlist, total_comments):
    ''' Input is a Counter dictionary of frequency of unique appearances within
        each comment in a body of comments (words found multiple times in a
        single comment are only counted once) and total number of comments.
        Output a dictionary of the inverse document frequency of terms

        Compute the inverse term frequency as follows:
        Log_e(Total number of documents /
              Number of documents containing term t) '''
    cnt = Counter()
    if (total_comments != 0):
        for key, value in termlist.items():
        	cnt[key] = (value / total_comments)
#            cnt[key] = math.log(total_comments / value)
        return cnt
    else: #divide by 0
        print("IDF attempted to divide by 0.\n")
        return cnt
