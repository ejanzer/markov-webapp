#!/usr/bin/env python

import sys
from random import randint, shuffle
import os

def clean_up_text(text):
    words = text.split()
    for word in words:
        if word == 'Valentine' or word == 'Day':
            word = word.lower()
    return words

def make_chains(input_text, n_gram_size):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""

    words = clean_up_text(input_text)

    d = {}

    # iterate through the words creating n-grams, stopping an n-gram short of the end
    for i in range(len(words) - n_gram_size):
        # build an n-gram to serve as the key in the dictionary (as a tuple)
        key = tuple(words[i:i + n_gram_size])

        # check if the n-gram is already in the dictionary
        if not d.get(key):
            d[key] = [words[i + n_gram_size]]
        else:
            d[key].append(words[i + n_gram_size])

    return d

def make_text(chains, starter_keys, output_length):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""

    key = get_starting_key(starter_keys)

    # Initialize list with the words in the starter key
    words = list(key)
    
    # while the randomly chosen tuple exists in the chains dictionary
    while chains.get(key):
        # get a random value from the values list
        random_number = randint(0, len(chains[key]) - 1)
        random_word = chains[key][random_number]

        # Check if adding this word will put us over the max word length. If so, break.
        if len(words) + 1 > output_length:
            break

        words.append(random_word)

        # Generate the next key from the existing key and the new word
        new_key = list(key[1:])
        new_key.append(random_word)
        key = tuple(new_key)
    
    return ' '.join(words)

def generate_starter_keys(chains):
    """Create a list of all tuples that start with a capital letter."""
    starter_keys = []
    keys = chains.keys()
    for key in keys:
        if ord(key[0][0]) >= ord('A') and ord(key[0][0]) <= ord('Z'):
            starter_keys.append(key)

    return starter_keys

def get_starting_key(starter_keys):
    """Returns a tuple that starts with a capital letter."""
    random_index = randint(0, len(starter_keys) - 1)
    return starter_keys[random_index]

def generate_text(corpus, n_gram_size, wordcount):
    """Returns randomly generated text given a corpus text, 
    n_gram_size and max wordcount."""
    chains = make_chains(corpus, n_gram_size)
    starter_keys = generate_starter_keys(chains)
    return make_text(chains, starter_keys, wordcount)
