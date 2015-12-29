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

DEFAULT_SEARCH = 'PRAW'
DEFAULT_SUB = 'cscareerquestions'
# Parse command line arguments
parser = argparse.ArgumentParser(description='Reddit Topic Analyzer',
    epilog='Author: Josh Granberry (jdgranberry@gmail.com)')

#-s SUBFORUM -q QUERY
parser.add_argument('-s', '--subreddit', help='Subreddit',
    action='store', default=DEFAULT_SUB, type=str)
parser.add_argument( '-q', '--query', help='Search query',
    action='store', default=DEFAULT_SEARCH, type=str)
args = parser.parse_args()
query = args.query
target_subreddit = args.subreddit

print('\nRunning analyzer for query \"' + query + '\" on subforum \"' +
    target_subreddit + '"...')
# Login information file
user_info = open('user_info.txt')

# Connect to Reddit and identify script
r = praw.Reddit(user_agent='Python3 Reddit Topic Analyzer v0.1.0'
    'Created by /u/jdgranberry'
    'Designed to refine search results into a collection of '
    'significant keywords and topics.')

# Login with username and password
username, password = [line.rstrip('\n') for line in user_info]
user_info.close()
r.login(username, password, disable_warning=True)

# Reddit target forum for search
subreddit = r.get_subreddit(target_subreddit)

# Generate submissions from a search
comment_count = 0
comment_word_frequency = Counter()

# Get list of stopwords and add query to it
stopwords = distillery_funcs.load_stopwords()
stopwords += query.lower().split()

# Start timer
time_start = time.time()

for submission in r.search(query, target_subreddit, sort=None, Period=None):
    # Flatten comment trees into a single unordered list.
    flat_comments = praw.helpers.flatten_tree(submission.comments)
    for comment in flat_comments:

        # Verify comment is a Comment (rather than MoreComments) object
        if isinstance(comment, praw.objects.Comment):
            comment_count += 1
            unique_words_in_comment = set(
                distillery_funcs.normalize_string(comment.body, stopwords, query))
            #print(unique_words_in_comment)
            for word in unique_words_in_comment:
                #debug
                #if word in stopwords:
                #    print("Exiting")
                #    sys.exit()
                comment_word_frequency[word] += 1

            # Update comment counter display
            sys.stdout.write("\rComments processed: " + str(comment_count))
            sys.stdout.flush()



inverse_doc_freq = distillery_funcs.inverse_document_frequency(
    comment_word_frequency, comment_count)



# End timer
time_end = time.time()

# Print results
print('\nQUERY: ' + query)
print('SUBFORUM: ' + target_subreddit)
print("\nIDF CONTENTS: ")
for k, v in inverse_doc_freq.most_common(10):
    print(k + " : " + str(v))
print("Words in IDF: " + str(len(inverse_doc_freq)))
print("Runtime:     " + str(round(time_end - time_start, 2)))
