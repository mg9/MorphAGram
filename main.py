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
    # Loop over the file and process word by word.
    for line in open(word_list_file):
        line = line.strip()
        # Ignore comment lines.
        if not line or line.startswith('#') or line.startswith('//'):
            continue
        word = line
        words.append(word)
        # Covert the word to its HEX representation.
        encoded_word = convert_string_to_hex_chars(word)
        encoded_words.append(encoded_word)
        # Keep track of the unique characters (in the HEX representation).
        hex_chars.extend(encoded_word.split())
    # Sort the outputs.
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
    # Loop over the file and process rule by rule.
    for line in open(grammar_file):
        line = line.strip()
        # Ignore comment lines.
        if not line or line.startswith('#') or line.startswith('//'):
            continue
        # Read the current rule.
        columns = line.partition('-->')
        key = columns[0].strip()
        value = columns[2].strip()
        # Convert terminal chcratcers within "(" and ")" into their HEX representation.
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
            grammar_writer.write(key + ' --> ' + value + '\n')


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
    # Read the prefixes and suffixe from the file.
    prefixes, suffixes = read_linguistic_knowledge(lk_file)
    # Seed the grammar with the prefiexes.
    grammar['1 1 ' + prefix_nonterminal].extend([convert_string_to_hex_chars(prefix) for prefix in prefixes])
    # Seed the grammar with the suffixes.
    grammar['1 1 ' + suffix_nonterminal].extend([convert_string_to_hex_chars(suffix) for suffix in suffixes])
    return grammar


def read_linguistic_knowledge(lk_file):
    '''
    This function reads the prefixes and suffixes in an lk_file (lk stands for Loinguistic Knowledge).
    '''
    prefixes = []
    suffixes = []
    read_prefixes = False
    read_suffixes = False
    # Loop over the lines in the file.
    for line in open(lk_file):
        line = line.strip()
        if line == '':
            continue
        # Read prefixes.
        if line == '###PREFIXES###':
            read_prefixes = True
            read_suffixes = False
        # Read suffixes.
        elif line == '###SUFFIXES###':
            read_prefixes = False
            read_suffixes = True
        elif line.startswith('###'):
            break
        else:
            # Read a merker line.
            if read_prefixes:
                prefixes.append(line)
            elif read_suffixes:
                suffixes.append(line)
    return prefixes, suffixes


def convert_morph_tree_to_word(fields, morphs):
    '''

    :param fields: all morphemes in the grammar morph tree of a word (example: "(Word (Prefix (...) Stem (...)))")
    :param morphs: RegEx specifiying which morphs to parse by.
    :return: a list of affixes and their respective morph type
    '''
    curr_morph = ""
    global_morph = []
    inner_children = []
    all_morphs = []
    morph = ""
    last_popped_morph = ""
    # Search for a field match with a morph RegEx given as input.
    for field in fields:
        m = field.split()
        # Keep track of children and current morpheme.
        rgx = r'^' + morphs + r'(#[0-9]*)?$'
        r = re.search(rgx, m[0])
        if morph and (len(global_morph) == 0 or r):
            new_morph = (curr_morph, morph)
            all_morphs.append(new_morph)
            morph = ""
            curr_morph = ""
        if r:
            curr_morph = m[0]
        if curr_morph is not "":
            if m[0] == curr_morph:
                global_morph.append(m[0])
            else:
                inner_children.append(m[0])
            # Pop all ")".
            if ")" in field:
                f = list(field)
                f.pop()  # Pop '/n' character.
                while ")" in f:
                    last_ch = f.pop()
                    if len(inner_children):
                        last_popped_morph = inner_children.pop()
                    if last_popped_morph == "Char":
                        # Parse to hex value and convert.
                        h = field.split()[1]
                        e = h.find(")")
                        ch = convert_hex_to_string(h[:e])
                        # Add character to word.
                        morph += ch
                    if last_ch == '$' or len(inner_children) == 0:
                        if ")" in f and global_morph:
                            global_morph.pop()
                        break
    if morph:
        new_morph = (curr_morph, morph)
        all_morphs.append(new_morph)
    return all_morphs


def extract_all_words(file, morphs):
    '''
    This function parses the output of the word morphologies into
    a human-readable format that denotes a word split into its morphemes
    separated by a '+' character and converting hex denoted characters
    into their respective unicode symbol. It writes these conversions
    into a file.

    :param file: a txt file that contains each words' morphology trees
    :param morphs: a RegEx that denotes the morphemes that will be denoted in the final
    output
    :return all words parsed by affix (example: "ir+re+(place)+able+s")
    '''
    output = []

    for line in open(file, 'r'):
        fields = line.split('(')
        # Search for a field match with a morph RegEx given as input.
        all_morphs = convert_morph_tree_to_word(fields[1:], morphs)
        # Append affixes together separated by a "+".
        word = ""
        for morph in all_morphs:
            # Append "+".
            if word != "":
                word += "+"
            # Enclose "Stem#[0-9]+" type morphs in "( ... )"
            morph_type = morph[0]
            is_stem = re.match(r'^Stem#[0-9]+', morph_type)
            if is_stem:
                word += "("
            word += morph[1]
            if is_stem:
                word += ")"
        output.append(word)
    return output


def affix_analyzer(file, n, morphs):
    '''
    :param file: file containing grammar morph tree for each word.
    :param n: number indicating how many of the top affixes to return.
    :param morphs: RegEx of morphs to parse for (example: "(Prefix|Suffix)")
    :return: top n affixes, all prefixes and their counts, all suffixes and their counts
    '''
    prefix_counter = {}
    suffix_counter = {}

    pre = morphs.split("|")[0]
    pre = pre[1:]

    for line in open(file, 'r'):
        fields = line.split('(')
        # Search for a field match with a morph RegEx given as input.
        all_morphs = convert_morph_tree_to_word(fields[1:], morphs)
        # Separate into respective affix counter.
        for morph in all_morphs:
            morph_type = morph[0]
            is_prefix = re.match(r'^Prefix', morph_type)
            if is_prefix:
                if prefix_counter.get(morph[1]):
                    prefix_counter[morph[1]] += 1
                else:
                    prefix_counter[morph[1]] = 1
            else:
                if suffix_counter.get(morph[1]):
                    suffix_counter[morph[1]] += 1
                else:
                    suffix_counter[morph[1]] = 1

    # Return highest n affixes.
    # Sort prefixes.
    prefix_list_sorted = sorted(prefix_counter.items(), key=lambda x: x[1], reverse=True)
    suffix_list_sorted = sorted(suffix_counter.items(), key=lambda x: x[1], reverse=True)

    n_affixes = []
    p = 0  # index for prefix_list_sorted
    s = 0  # index for suffix_list_sorted
    while n > 0:
        if prefix_list_sorted[p][1] > suffix_list_sorted[s][1]:
            n_affixes.append(prefix_list_sorted[p][0])
            p += 1
        else:
            n_affixes.append(suffix_list_sorted[s][0])
            s += 1
        n -= 1

    return n_affixes, prefix_counter, suffix_counter


if __name__ == '__main__':
    main()
