
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

def parse_seg(file, morphs):
    '''
    This function parses the output of the word morphologies into
    a human-readable format that denotes a word split into its morphemes
    separated by a '+' character and converting hex denoted characters
    into their respective unicode symbol. It writes these conversions
    into a file.

    Input:
    segmentation_file: a txt file that contains each words' morphology trees
    morphs: a RegEx that denotes the morphemes that will be denoted in the final
    output
    '''
    output = []

    for line in open(file, 'r'):
        fields = line.split('(')
        word = ""
        curr_morph = ""
        stem_open = False
        morph_change = False
        ch_added = False
        inner_child = []
        # Search for a field match with a morph RegEx given as input.
        for field in fields[1:]:
            m = field.split()
            # Keep track of children and current morpheme.
            rgx = r'^' + morphs + r'(#[0-9]*)?$'
            r = re.search(rgx, m[0])
            if r: # RegEx of current morph was matched to input.
                curr_morph = m[0]
            if curr_morph is not "":
                if m[0] != curr_morph:
                    inner_child.append(m[0])
                # Pop all ")".
                if ")" in field:
                    f = list(field)
                    f.pop() # Pop '/n' character.
                    while ")" in f:
                        last_ch = f.pop()
                        if len(inner_child):
                            last_popped_morph = inner_child.pop()
                        else:
                            break
                        if last_popped_morph == "Char":
                            # Parse to hex value and convert.
                            h = field.split()[1]
                            e = h.find(")")
                            ch = convert_hex_to_string(h[:e])
                            # Verify if Stem "(" or ")" is necessary.
                            if re.match("^Stem*", curr_morph) and not stem_open:
                                stem_open = True
                                if len(word)==0:
                                    word += "("
                            elif re.match("^Stem*", curr_morph) is None and stem_open:
                                stem_open = False
                                word += ")"
                            # Add "+" if a change of current morpheme has occurred.
                            # if (curr_morph != last_morph and last_morph != "") or (morph_change and not stem_open):
                            if morph_change and ch_added:
                                word += "+"
                                if stem_open:
                                    word += "("
                                morph_change = False
                                ch_added = False
                            # Remove trailing new line character if necessary.
                            if list(ch)[0] == '\x00':
                                word += str(list(ch)[1])
                                ch_added = True
                            else:
                                word += ch
                                ch_added = True
                            morph_change = False
                        if last_ch == '$'or len(inner_child) == 0:
                            if stem_open:
                                stem_open = False
                                word += ")"
                            morph_change = True
                            curr_morph = ""
                            break
        output.append(word)
    return output

def affix_analyzer(file, n, morphs):
    prefix_counter = {}
    suffix_counter = {}

    pre = morphs.split("|")[0]
    pre = pre[1:]

    for line in open(file, 'r'):
        fields = line.split('(')
        affix = ""
        curr_morph = ""
        prefix = False
        inner_child = []
        # Search for a field match with a morph RegEx given as input.
        for field in fields[1:]:
            m = field.split()
            # Keep track of children and current morpheme.
            rgx =  r'^' + morphs + r'(#[0-9]*)?$'
            r = re.search(rgx, m[0])
            if r:  # RegEx of current morph was matched to input.
                curr_morph = m[0]
            if curr_morph is not "":
                if re.search(pre, curr_morph):
                    prefix = True
                else:
                    prefix = False
                if m[0] != curr_morph:
                    inner_child.append(m[0])
                # Pop all ")".
                if ")" in field:
                    f = list(field)
                    f.pop()  # Pop '/n' character.
                    while ")" in f:
                        last_ch = f.pop()
                        if len(inner_child):
                            last_popped_morph = inner_child.pop()
                        else:
                            curr_morph = ""
                            break
                        if last_popped_morph == "Char":
                            # Parse to hex value and convert.
                            h = field.split()[1]
                            e = h.find(")")
                            ch = convert_hex_to_string(h[:e])

                            # Remove trailing new line character if necessary.
                            if list(ch)[0] == '\x00':
                                affix += str(list(ch)[1])
                            else:
                                affix += ch
                        if last_ch == '$' or len(inner_child) == 0:
                            print(affix)
                            if prefix:
                                if affix in prefix_counter:
                                    prefix_counter[affix] += 1
                                else:
                                    prefix_counter[affix] = 1
                            else:
                                if affix in suffix_counter:
                                    suffix_counter[affix] += 1
                                else:
                                    suffix_counter[affix] = 1
                            affix = ""
                            curr_morph = ""
                            break
    # Return highest n affixes.
    # Sort prefixes.
    prefix_list_sorted = sorted(prefix_counter.items(), key=lambda x: x[1], reverse=True)
    suffix_list_sorted = sorted(suffix_counter.items(), key=lambda x: x[1], reverse=True)

    n_affixes = []
    p = 0 # index for prefix_list_sorted
    s = 0 # index for suffix_list_sorted
    while n > 0:
        if prefix_list_sorted[p][1] > suffix_list_sorted[s][1]:
            n_affixes.append(prefix_list_sorted[p][0])
            p += 1
        else:
            n_affixes.append(suffix_list_sorted[s][0])
            s += 1
        n -= 1

    return n_affixes


        
if __name__ == '__main__':
    main()
