
import sys
import argparse
import re
import os

from os import path
from collections import defaultdict

from utils import *


def process_words(word_list_file):
    '''
    This function reads a file of words and produces three lists:
    1- A list of unique words.
    2- A list of unique words in the HEX representation
    3- A list of unique characters in the HEX representation
    '''
    words = []
    encoded_words = []
    hex_chars = []
    #Loop over the file and process word by word.
    for line in open(word_list_file):
        line = line.strip()
        #Ignore comment lines.
        if not line or line.startswith('#') or line.startswith('//'):
            continue
        word = line
        words.append(word)
        #Covert the word to its HEX representation.
        encoded_word = convert_string_to_hex_chars(word)
        encoded_words.append(encoded_word)
        #Keep track of the unique characters (in the HEX representation).
        hex_chars.extend(encoded_word.split())
    #Sort the outputs.
    words.sort()
    encoded_words.sort()
    hex_chars.sort()
    return set(words), set(encoded_words), set(hex_chars)

def write_encoded_words(encoded_words, word_list_file):
    '''
    This function writes a list of encoded words (in the HEX representation) into a file.
    '''
    word_list_writer = open(word_list_file, 'w')
    word_list_writer.writelines('^^^ %s $$$\n' % word for word in encoded_words)
    
def read_grammar(grammar_file):
    '''
    This function reads a grammar file and returns a map of the grammar rules.
    The keys represent the unique LHS terms
    The values are a list of the RHS terms of the corresponding keys
    '''
    grammar = defaultdict(list)
    #Loop over the file and process rule by rule.
    for line in open(grammar_file):
        line = line.strip()
        #Ignore comment lines.
        if not line or line.startswith('#') or line.startswith('//'):
            continue
        #Read the current rule.
        columns = line.partition('-->')
        key = columns[0].strip()
        value = columns[2].strip()
        #Convert terminal chcratcers within "(" and ")" into their HEX representation.
        match = re.search(r'(\(.*?\))', value)
        while match:
            value = convert_string_to_hex_chars(match.group(0)[1:-1])
            value = line.replace(match.group(0), replacement)
            match = re.search(r'(\(.*?\))', value)
        grammar[key].append(value)
    return grammar

def write_grammar(grammar, grammar_file):
    '''
    This function writes a grammar map into a file.
    '''
    grammar_writer = open(grammar_file, 'w')
    for key in grammar:
        for value in grammar[key]:
            grammar_writer.write(key+' --> '+value+'\n')

def add_chars_to_grammar(grammar, hex_chars):
    '''
    This function writes a grammar map into a file
    '''
    grammar['1 1 Char'].extend(hex_chars)
    return grammar

def prepare_scholar_seeded_grammar(grammar, lk_file, prefix_nonterminal, suffix_nonterminal):
    '''
    This function seeds a grammar tree with prefixes and suffixes read from a file (lk_file where lk stands for Loinguistic Knowledge).
    The nonterminals under which the affixes are inserted are denoted by prefix_nonterminal and suffix_nonterminal for prefixes and suffixes, respectively.
    '''
    #Read the prefixes and suffixe from the file.
    prefixes, suffixes = read_linguistic_knowledge(lk_file)
    #Seed the grammar with the prefiexes.
    grammar['1 1 '+prefix_nonterminal].extend([convert_string_to_hex_chars(prefix) for prefix in prefixes])
    #Seed the grammar with the suffixes.
    grammar['1 1 '+suffix_nonterminal].extend([convert_string_to_hex_chars(suffix) for suffix in suffixes])
    return grammar

def read_linguistic_knowledge(lk_file):
    '''
    This function reads the prefixes and suffixes in an lk_file (lk stands for Loinguistic Knowledge).
    '''
    prefixes = []
    suffixes = []
    read_prefixes = False
    read_suffixes = False
    #Loop over the lines in the file.
    for line in open(lk_file):
        line = line.strip()
        if line == '':
            continue
        #Read prefixes.
        if line == '###PREFIXES###':
            read_prefixes = True
            read_suffixes = False
        #Read suffixes.
        elif line == '###SUFFIXES###':
            read_prefixes = False
            read_suffixes = True
        elif line.startswith('###'):
            break
        else:
            #Read a merker line.
            if read_prefixes:
                prefixes.append(line)
            elif read_suffixes:
                suffixes.append(line)
    return prefixes, suffixes

        
if __name__ == '__main__':
    main()
