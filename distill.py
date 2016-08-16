#!/usr/bin/python3
''' This script allows the user to specify a search query and Reddit subforum to
    submit to Reddit. It receives the relevant comments returned from the
    Reddit website, normalizes them, and performs analysis of the terms within
    to identify relevant keywords.
'''

import argparse    # Command line argument parsing
import praw        # Python Reddit API Wrapper
from collections import Counter # Allows combining dicts while adding values
import time        # Timing computation
import distillery_funcs # helper functions
import sys         # sys.stdout, sys.exit()

# To get rid of the "unclosed socket" ResourceWarning, you must uncomment the
#following two lines of code. Unfortunately this disables ALL warnings.
#import warnings
#warnings.filterwarnings('ignore')

DEFAULT_SEARCH = 'PRAW'
DEFAULT_SUB = 'cscareerquestions'
NUM_RESULTS = 20

# Parse command line arguments
parser = argparse.ArgumentParser(
    description='Reddit Topic Analyzer',
    epilog='Author: Josh Granberry (jdgranberry@gmail.com)')

#-s SUBFORUM -q QUERY
parser.add_argument('-s', '--subreddit', help='Subreddit',
    action='store', default=DEFAULT_SUB, type=str)
parser.add_argument( '-q', '--query', help='Search query',
    action='store', default=DEFAULT_SEARCH, type=str)
args = parser.parse_args()
query = args.query
target_subreddit = args.subreddit

# Login information file containing two lines for username and password
user_info = open('user_info.txt')

# Connect to Reddit and identify script
r = praw.Reddit(user_agent='Python3 Reddit Information Distillery v0.1.0'
    'Created by /u/jdgranberry'
    'Designed to refine search results into a collection of '
    'significant keywords and topics.')

# Login with username and password
username, password = [line.rstrip('\n') for line in user_info]
user_info.close()
r.login(username, password, disable_warning=True)

# Reddit target forum for search
subreddit = r.get_subreddit(target_subreddit)

# Get list of stopwords and add query to it
stopwords = distillery_funcs.load_stopwords(query)


# Start timer
time_start = time.time()

# Generate results from a search
print('\nQUERY: ' + query)
print('SUBREDDIT: ' + target_subreddit)
comment_count = 0
word_count = 0
comment_word_freq = Counter()
collection_word_freq = Counter()
TFIDF_values = Counter()

comment_corpus = r.search(query, target_subreddit, sort=None, Period=None)

for submission in comment_corpus:
    # Flatten comment trees into a single unordered list.
    flat_comments = praw.helpers.flatten_tree(submission.comments)
    for comment in flat_comments:

        # Verify comment is a Comment (rather than MoreComments) object
        if isinstance(comment, praw.objects.Comment):
            comment_count += 1
            comment = distillery_funcs.normalize_string(
                comment.body, stopwords)
            for word in comment:
                word_count += 1
                collection_word_freq[word] += 1
            unique_words_in_comment = set(comment)
            for word in unique_words_in_comment:
                comment_word_freq[word] += 1

            # Update comment counter display
            sys.stdout.write("\rCOMMENTS PROCESSED: " + str(comment_count))
            sys.stdout.flush()


# Calculate inverse document frequencylen
inverse_doc_freq = distillery_funcs.inverse_document_frequency(
    comment_word_freq, comment_count)

# Calculate collection term frequency
collection_word_freq = distillery_funcs.term_frequency(
    collection_word_freq, word_count)

# Calculate the TF-IDF
if (len(collection_word_freq) == len(inverse_doc_freq)):
    for key in inverse_doc_freq:
        TFIDF_values[key] = collection_word_freq[key] * inverse_doc_freq[key]
else:
    print("TF and IDF do not contain the same number of keys.")
    sys.exit()


# End timer
time_end = time.time()

# Print results
print("\n\nTOP " + str(NUM_RESULTS) + ": ")
for k, v in TFIDF_values.most_common(NUM_RESULTS):
    print(k + ": " + str(round(v * 100, 2)))
print("\nRUNTIME:     " + str(round(time_end - time_start, 2)) + "s")
