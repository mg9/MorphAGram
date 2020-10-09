import string
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
    with open(word_list_file, 'r', encoding="utf-8") as fin:
        for line in fin:
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
    hex_chars = sort_unique(hex_chars)
    return set(words), set(encoded_words), hex_chars

def sort_unique(sequence):
    sequence.sort()
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]

def write_encoded_words(encoded_words, word_list_file):
    '''
    This function writes a list of encoded words (in the HEX representation) into a file.
    '''
    with open(word_list_file, 'w') as fout:
        fout.writelines('^^^ %s $$$\n' % word for word in encoded_words)


def read_grammar(grammar_file):
    '''
    This function reads a grammar file and returns a map of the grammar rules.
    The keys represent the unique LHS terms
    The values are a list of the RHS terms of the corresponding keys
    '''
    grammar = defaultdict(list)
    # Loop over the file and process rule by rule.
    with open(grammar_file, 'r', encoding="utf-8") as fin:
        for line in fin:
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
    with open(grammar_file, 'w', encoding="utf-8") as fout:
        for key in grammar:
            for value in grammar[key]:
                fout.write(key + ' --> ' + value + '\n')


def add_chars_to_grammar(grammar, hex_chars):
    '''
    This function writes a grammar map into a file
    '''
    grammar['1 1 Char'].extend(hex_chars)
    return grammar


def separate_jp_char(grammar_file, grammar_file_sep_char):
    '''
    This function takes a Japanese grammar file (already populated by characters as "Char")
    and separates the characters into Japanese and Chinese characters as J_Char and Ch_Char, respectively
    :param grammar_file: original grammar file path
    :param grammar_file_sep_char: grammar file path to character-separated grammars
    :return:
    '''
    hiragana = "ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴ\
    ふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをんゔゕゖ"
    katakana = "ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピ\
    フブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲンヴヵヶヷヸヹヺ"
    all_jp_char = hiragana + katakana
    j_char = set(list(all_jp_char))
    with open(grammar_file, "r", encoding="utf-8") as fin:
        with open(grammar_file_sep_char, "w", encoding="utf-8") as fin_sep:
            for line in fin:
                # Only process lines beginning with "1 1 Char"
                elements = line.split()
                if "1 1 Char -->" in line:
                    ch = convert_hex_to_string(elements[4])
                    if ch in j_char:
                        elements[2] = "J_Char"
                    else:
                        elements[2] = "Ch_Char"
                    new_line = " ".join(elements)
                    new_line += "\n"
                    fin_sep.write(new_line)
                else:
                    fin_sep.write(line)

def prepare_cascaded_grammar(grammar, output_file, n, in_prefix_nonterminal, in_suffix_nonterminal, out_prefix_nonterminal, out_suffix_nonterminal):
    '''
    This function seeds a grammar tree with prefixes and suffixes read from the output of some grammar.
    The nonterminals under which the affixes are inserted are denoted by prefix_nonterminal and suffix_nonterminal for prefixes and suffixes, respectively.
    :param in_prefix_nonterminal: the prefix nonterminal to read from the output
    :param in_suffix_nonterminal: the suffix nonterminal to read from the output
    :param n: the number of most frequent affixes to extract and seed
    :param out_prefix_nonterminal: the prefix nonterminal to seed the prefixes into
    :param out_suffix_nonterminal: the suffix nonterminal to seed the suffixes into
    '''
    _, prefixes, suffixes = analyze_affixes(output_file, n, in_prefix_nonterminal, in_suffix_nonterminal)
    # Seed the grammar with the prefixes.
    grammar['1 1 ' + out_prefix_nonterminal].extend([convert_string_to_hex_chars(prefix) for prefix in prefixes])
    # Seed the grammar with the suffixes.
    grammar['1 1 ' + out_suffix_nonterminal].extend([convert_string_to_hex_chars(suffix) for suffix in suffixes])
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
    This function reads the prefixes and suffixes in an lk_file (lk stands for Liinguistic Knowledge).
    '''
    prefixes = []
    suffixes = []
    read_prefixes = False
    read_suffixes = False
    # Loop over the lines in the file.
    with open(lk_file, 'r', encoding="utf-8") as fin:
        for line in fin:
            line = line.strip()
            if len(line) == 0:
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


def analyze_affixes(file, n, prefix_nonterminal, suffix_nonterminal):
    '''
    :param file: file containing grammar morph tree for each word.
    :param n: number indicating how many of the top affixes to return.
    :param prefix_nonterminal: name of the prefix nonterminal to search for
    :param suffix_nonterminal: name of the suffix nonterminal to search for
    :return: top n affixes, all prefixes, and all suffixes
    '''
    prefix_counter = {}
    suffix_counter = {}
    with open(file, 'r', encoding='utf-8') as fin:
        for line in fin:
            line = line.strip()
            # Search for a nonterminal match with a morph RegEx given as input.
            morphs = get_morphs_from_tree(line, [prefix_nonterminal, suffix_nonterminal])
            # Separate into respective affix counter.
            for nonterminal in morphs:
                for morph in  morphs[nonterminal]:
                    is_prefix = (nonterminal == prefix_nonterminal)
                    if is_prefix:
                        if prefix_counter.get(morph):
                            prefix_counter[morph] += 1
                        else:
                            prefix_counter[morph] = 1
                    else:
                        if suffix_counter.get(morph):
                            suffix_counter[morph] += 1
                        else:
                            suffix_counter[morph] = 1

    # Return top n affixes.
    # Sort prefixes.
    prefix_list_sorted = sorted(prefix_counter.items(), key=lambda x: x[1], reverse=True)
    suffix_list_sorted = sorted(suffix_counter.items(), key=lambda x: x[1], reverse=True)

    n_affixes = []
    p = 0  # index for prefix_list_sorted
    s = 0  # index for suffix_list_sorted

    # Final list of x prefixes and y suffixes such that x+y=n
    prefix_x = []
    suffix_y = []

    # If prefix and suffix lists were empty, return empty lists
    if len(prefix_list_sorted) == len(suffix_list_sorted) == 0:
        return n_affixes, prefix_x, suffix_y

    while n > 0:
        if len(prefix_list_sorted) > 0 and (len(suffix_list_sorted) == 0 or prefix_list_sorted[p][1] > suffix_list_sorted[s][1]):
            n_affixes.append(prefix_list_sorted[p][0])
            prefix_x.append(prefix_list_sorted[p][0])
            p += 1
        else:
            n_affixes.append(suffix_list_sorted[s][0])
            suffix_y.append(suffix_list_sorted[s][0])
            s += 1
        n -= 1

    return n_affixes, prefix_x, suffix_y

def get_morphs_from_tree(tree, nonterminals):
    '''
    :param treea: a line in the segmentation output
    Example: "(Word (Prefix#151 ^^^) (Stem#2 (SubMorphs (SubMorph#22 (Chars (Char 0075)
    (Chars (Char 006e)))) (SubMorphs (SubMorph#11 (Chars (Char 0064)))))) (Suffix#2 $$$))"
    :param nonterminals: the nonterminals to patse 
    :return: a map of nonterminals and their textual values
    '''

    morphs = defaultdict(list)
    parts = tree.split()
    for nonterminal in nonterminals:
        read = False
        count=0
        current_chars = []
        for part in parts:
            if not read and re.match('^\(?'+nonterminal+'(#[0-9]+)?$', part):
                read = True
            elif read and re.match('^([a-f\d]{4,8})\)*$', part):
                hex_str = part.replace(')', '')
                current_chars.append(convert_hex_to_string(hex_str))
            if read:
                count += part.count('(')
                count -= part.count(')')
                if count <= 0:
                    if len(current_chars) > 0:
                        morph = ''.join(current_chars)
                        morphs[nonterminal].append(morph)
                    read = False
                    count = 0
                    current_chars = []
    return morphs
 

def parse_PYAGS_segmentation_output(file, prefix_nonterminal, stem_nonterminal, suffix_nonterminal, segmented_text_file, segmented_dictionary_file):
    '''
    This function parses the output of the segmented_word morphologies into
    a human-readable format that denotes a segmented_word split into its morphemes
    separated by a '+' character and converting hex denoted characters
    into their respective unicode symbol. It writes these conversions
    into 2 files: one file contains only the word segmentations, the other contains
    the segmentation along with its respective word.

    :param file: a txt file that contains each words' morphology trees
    Stem morph in characters
    :param prefix_nonterminal: prefix nonterminal to parse
    :param stem_nonterminal: stem nonterminal to parse
    :param suffix_nonterminal: suffix nonterminal to parse
    :param segmented_text_file: file location to write all word segmentations
    :param segmented_dictionary_file: file location to write all word segmentations
    and their respective word
    :return map of words and their respective parsings by affix
    (example: "irreplaceables" : "ir+re+(place)+able+s")
    '''
    word_segmentation_map = {}
    segmented_word_list = []

    with open(file, 'r', encoding='utf-8') as fin:
        for line in fin:
            line = line.strip()
            if len(line) == 0:
                continue;
            # Extract the morphemes given the nonterminals.
            morphs = get_morphs_from_tree(line, [prefix_nonterminal, stem_nonterminal, suffix_nonterminal])
            word = ''
            segmented_word = ''
            if prefix_nonterminal in morphs and len(morphs[prefix_nonterminal]) > 0:
                word += ''.join(morphs[prefix_nonterminal])
                segmented_word += '+'.join(morphs[prefix_nonterminal])
            if stem_nonterminal in morphs and len(morphs[stem_nonterminal]) > 0:
                if len(segmented_word) > 0:
                    segmented_word += "+"
                word += ''.join(morphs[stem_nonterminal])
                segmented_word += '('+'+'.join(morphs[stem_nonterminal])+')'
            if suffix_nonterminal in morphs and len(morphs[suffix_nonterminal]) > 0:
                if len(segmented_word) > 0:
                    segmented_word += "+"
                word += ''.join(morphs[suffix_nonterminal])
                segmented_word += '+'.join(morphs[suffix_nonterminal])

            if word_segmentation_map.get(word) is None:
                word_segmentation_map[word] = segmented_word
            segmented_word_list.append((word, segmented_word))

    # Write all segmented words to segmented_text_file.
    if segmented_text_file:
        include_word = False
        write_word_segmentations_to_file(segmented_text_file, include_word, segmented_word_list)

    # Write words and their respective segmentation to segmented_text_and_word_file.
    if segmented_dictionary_file:
        include_word = True
        write_word_segmentations_to_file(segmented_dictionary_file, include_word, word_segmentation_map.items())

    return word_segmentation_map

def write_word_segmentations_to_file(file, include_word, word_list):
    '''
    Writes word segmentations to file provided as input.
    :param file: File to write to
    :param include_word: Boolean whether to write non-segmented word to file
    :param word_list: list of words to write
    '''
    with open(file, "w", encoding='utf-8') as fout:
        for w in word_list:
            new_line = ""
            if include_word:
                new_line += w[0] + "\t"
            new_line += w[1] + '\n'
            fout.write(new_line)

def insert_splits(word, count, solutions):
    '''
    Function to insert "+" in word count times. Returns every solution that does not have an empty stem.
    '''
    # If count == 0, no more insertions necessary. Append current solution and return.
    if count == 0:
        solutions.append(word)
        return solutions
    # Add a "+" in all possible places
    for i in range(len(word)):
        # Construct new split.
        new_split = word[:i] + "+" + word[i:]
        # Ignore instances of empty morphs. (for example: "e++xample" will be ignored)
        if "++" in new_split:
            continue
        # Call recursively with a decremented count.
        insert_splits(new_split, count-1, solutions)

    return solutions

def count_affixes_from_segmented_word(affix_morphs, affix_count):
    '''
    This method is a helper function that keeps track of all instances of morphs. Used to pre-process text.
    :param affix_morphs: String sequence of morphs to be counted.
    :param affix_count: Dictionary of all seen morphs and their counts.
    '''
    if affix_morphs == "":
        if "empty" in affix_count:
            affix_count["empty"] += 1
            return
        else:
            affix_count["empty"] = 1
            return
    all_affixes = affix_morphs.split("+")  # List of affixes ex. ['over', 're'].
    joint_affixes = "".join(all_affixes)  # Join all prefixes ex. overre.
    if affix_count.get(joint_affixes):
        if affix_count[joint_affixes].get(affix_morphs):
            affix_count[joint_affixes][affix_morphs] += 1
        else:
            affix_count[joint_affixes][affix_morphs] = 1
    else:
        affix_count[joint_affixes] = {affix_morphs: 1}
    return

def count_stems_from_segmented_word(segmented_word, stem_count):
    '''
    Helper function that counts all instances of seen stems.
    :param segmented_word: String sequence of morphs separated by "+".
    :param stem_count: Dictionary of all instances of stems and their counts.
    '''
    if segmented_word == "":
        if "empty" in stem_count:
            stem_count["empty"] += 1
        else:
            stem_count["empty"] = 1
    while "(" in segmented_word:  # There may be multiple stems in a word. If so, they are all separate entries in map.
        p_open = segmented_word.find("(")
        p_close = segmented_word.find(")")
        stem_morph = segmented_word[p_open+1:p_close]
        if stem_morph in stem_count:
            stem_count[stem_morph] += 1
        else:
            stem_count[stem_morph] = 1
        segmented_word = segmented_word[p_close+1:]
    return

def count_affixes_from_dictionary(dic):
    '''
    Helper function that pre-processes all counts of all affixes in language dictionary.
    :param dic: Dictionary of all words (presumably a comprehensive dictionary of a language) and their corresponding
    morphs (ex: {"irreplaceables": "ir+re+place+able+s"}
    :return: 3 dictionaries: 1) All prefix instances and their counts 2) All stem instances and their counts 3) All
    suffix instances and their counts.
    '''
    prefix_count = {}
    stem_count = {}
    suffix_count = {}

    for item in dic.items():
        segmented_word = item[1]
        full_word = item[0]

        # If prefix exists, count and store prefixes.
        if "+(" in segmented_word:
            morphs = segmented_word.split("+(")
            prefix_morphs = morphs[0] # morphs[0] contains sequence of prefixes ex. over+re+(act) --> over+re.
            count_affixes_from_segmented_word(prefix_morphs, prefix_count)
        else:
            count_affixes_from_segmented_word("", prefix_count)

        # If stem exists, count and store stems.
        if "(" in segmented_word:
            count_stems_from_segmented_word(segmented_word, stem_count)
        else:
            count_stems_from_segmented_word(segmented_word, stem_count)

        # If suffix exists, count and store suffixes.
        if ")+" in segmented_word:
            morphs = segmented_word.split(")+")
            # If there are multiple stems, you want to take the last found instance ex. (abc)+(def)+xyz.
            suffix_morphs = morphs[len(morphs)-1]
            if ")" in suffix_morphs: # No suffix exists. ex. (abc)+(def).
                continue
            count_affixes_from_segmented_word(suffix_morphs, suffix_count)
        else:
            count_stems_from_segmented_word("", suffix_count)

    return prefix_count, stem_count, suffix_count

def count_total_affixes(affix_count):
    '''
    Helper that counts the total number of affixes.
    :param affix_count: A dictionary containing all counts of all instances of an affix sequence
    (ex: "redis": {"re+dis": 5, "red+is": 1})
    :return: an integer total of all affix sequences seen, a dictionary containing just the total counts of a given
    sequence (Using the above example:  6, {"redis": 6})
    '''
    TOTAL = 0
    total_affix_count = {}
    for affix, dic in affix_count.items():
        if affix == "empty":
            continue
        affix_sum = sum(dic.values())
        total_affix_count[affix] = affix_sum
        TOTAL += affix_sum

    return TOTAL, total_affix_count

def restore_casing(segmented_word, casing):
    '''
    Helper function that restores the casing seen in plaintext file.
    :param segmented_word: String morph sequence separated by "+".
    :param casing: List of booleans for all characters in segmented_word; True = lowercase False = uppercase
    :return: segmented_word with proper casings
    '''
    n = 0 # casing index
    restored_segmented_word = ""
    for ch in segmented_word:
        if ch == "+" or ch == "(" or ch == ")" or ch == '̇':
            restored_segmented_word += ch
            # Do not increment n.
            continue
        if not casing[n]:
            new_ch = ch.upper()
            restored_segmented_word += new_ch
        else:
            restored_segmented_word += ch
        n += 1

    return restored_segmented_word

def calculate_MLE(candidate, affix_counts, affix_totals):
    '''
    This function calculates the Maximum Likelihood Estimator for every segmented word candidate.
    :param candidate: Segmented word candidate. Always in form of 2 segments, where middle segment is a stem.
        ex. +(kid)+s or k+(id)+s
    :param affix_counts: A list of total numbers (one for each Prefix, Stem, and Suffix) of all affixes.
    :param affix_totals: A list of dictionaries (one for each Prefix, Stem, and Suffix) containing total counts for each
        affix.
    :return: MLE integer
    '''
    MLE = 1
    EMPTY = "empty"

    morphs = candidate.split("+")
    for x in range(3):
        # x = 0 --> Prefix; x = 1 --> Stem; x = 2 --> Suffix
        affix_morphs = morphs[x]
        #if x == 1:
        #    affix_morphs = affix_morphs[1:len(affix_morphs)-1] # Remove parentheses if necessary.
        affix_count = affix_counts[x]
        affix_total = affix_totals[x]
        if affix_morphs is "":
            affix_morphs = EMPTY
        if affix_morphs in affix_count:
            p_count = affix_count[affix_morphs]
        else: # candidate morph is not in the affix map
            p_count = 0
        MLE *= (p_count / affix_total)
    return MLE

def insert_parentheses(segmented_word):
    '''
    Helper function that takes segmented_word and adds a parentheses around the middle morph=Stem
    :param segmented_word: String sequence of morphs
    :return: segmented_word with parentheses around stem
    '''
    if "(" not in segmented_word:
        # Find first "+" and add "(" at the end.
        p_op = segmented_word.find("+")
        new_segmented_word = segmented_word[:p_op+1]
        new_segmented_word += "("
        # Find second "+" and add ")" at the end.
        next_segment = segmented_word[p_op+1:]
        p_cl = next_segment.find("+")
        new_segmented_word += next_segment[:p_cl]
        new_segmented_word += ")"
        # Add remainder of the word.
        new_segmented_word += next_segment[p_cl:]
        return new_segmented_word
    else:
        return segmented_word

def split_morphs_into_submorphs(segmented_word, affix_maps):
    '''
    Helper function that takes a segmented_word (separated into Prefix, Stem, Suffix) and splits each affix into
    submorphs if it exists.
    :param segmented_word: String sequence of morphs separated by "+".
    :param affix_maps: List of dictionaries (one for each Prefix, Stem, Suffix) that contains subdivisions of morphs
    :return: segmented_word where each morph has been split into submorphs
    '''
    morphs = segmented_word.split("+")
    new_morph = []
    start = 0
    end = len(affix_maps)
    if len(morphs) <= 1:
        return segmented_word
    elif len(morphs) == 2:
        if "+(" in segmented_word:
            end = 2
        elif ")+" in segmented_word:
            start = 1
        else:
            return segmented_word
    for x in range(start, end):
        affix_map = affix_maps[x]
        morph = morphs[x]
        if x == 1:
            morph = morph[1:len(morph)-1]
        if morph in affix_map:
            if type(affix_map[morph]) == int:
                new_morph.append(morphs[x])
                continue
            else:
                all_splits = affix_map[morph]
                all_splits_sorted = sorted(all_splits.items(), key=lambda x: x[1], reverse=True)
                new_morph.append(all_splits_sorted[0][0])
    return "+".join(new_morph)

def segment_file(dic, txt_file, output_file, min_word_length_to_segment, multiway_segmentaion):
    '''
    This function morphologically segments all words in a given plaintext file.
    :param dic: dictionary containing a list of words in the given language.
    It is assumed to be a comprehensive dictionary of the language.
    :param txt_file: plaintext file containing a tokenized sequence of words.
    (All punctuation marks are separated from words by whitespace such as:
    "The dog ' s bowl is empty . ")
    :param output_file: file to write output to
    :param min_stem_length: integer that represents the minimum length of a
    stem in the segmentation output of unseen words
    :param min_word_length_to_segment: integer that represents the minimum length of a
    word to be segmented (in characters)
    :param multiway_segmentaion: boolean value;
        if value is false, the segmented word will contain a three-way split
        (Prefix+Stem+Suffix)
        if value is true, the segmented word will contain a multi-way split
        if applicable (for example: PrefixMorph+Stem+SuffixMorph+SuffixMorph)
    :return:
    '''
    SEGMENT_COUNT = 2
    with open(output_file, "w", encoding='utf-8') as fout:

        # Pre-process dictionary to count all affixes (Prefix, Stem, and Suffix).
        prefix_map, stem_map, suffix_map = count_affixes_from_dictionary(dic)
        prefix_total, prefix_counts = count_total_affixes(prefix_map)
        suffix_total, suffix_counts = count_total_affixes(suffix_map)
        stem_total = sum(stem_map.values())
        affix_maps = [prefix_map, stem_map, suffix_map]
        affix_counts = [prefix_counts, stem_map, suffix_counts]
        affix_totals = [prefix_total, stem_total, suffix_total]

        with open(txt_file, "r", encoding='utf-8') as fin:
            for line in fin:
                words = line.split()
                new_line = [] # List containing all the segmented replacements of word in original line.
                for word in words:
                    #If the word is too short, do not segment it.
                    if len(word) < min_word_length_to_segment:
                        segmented_word = "("+word+")"
                    else:
                        # Save casing of all characters in a word.
                        casing = [ch.islower() for ch in word]
                        word_low = word.lower()
                        # If word already exists in dictionary, replace with existing segmentation.
                        if word_low in dic:
                            segmented_word = dic[word_low]
                            segmented_word = restore_casing(segmented_word, casing)
                            new_line.append(segmented_word)
                            continue
                        elif len(word_low) == 1 and word_low in string.punctuation:
                            punctuation = "("
                            punctuation += word_low + ")"
                            new_line.append(punctuation)
                            continue

                        # Deduce segmentation from existing affixes.
                        all_possible_splits = insert_splits(word_low, SEGMENT_COUNT, [])
                        candidate_score_tracker = {}
                        for candidate in all_possible_splits:
                            score = calculate_MLE(candidate, affix_counts, affix_totals)
                            candidate_score_tracker[candidate] = score
                        candidate_list_sorted = sorted(candidate_score_tracker.items(), key=lambda x: x[1], reverse=True)

                        # Choose highest-scoring candidate and return to original casing.
                        if len(candidate_list_sorted) == 0 or candidate_list_sorted[0][1] == 0.0:
                            segmented_word = "(" + word_low + ")"
                        else:
                            segmented_word = candidate_list_sorted[0][0]
                        segmented_word = insert_parentheses(segmented_word)
                        segmented_word = restore_casing(segmented_word, casing)

                        # If multiway_segmentation is True, further split prefixes and affixes into sub-affixes if applicable.
                        # For example: irre+(place)+ables --> ir+re+(place)+able+s
                        if multiway_segmentaion:
                            segmented_word = split_morphs_into_submorphs(segmented_word, affix_maps)
                    new_line.append(segmented_word)
                full_line = " ".join(new_line)
                full_line += '\n'
                fout.write(full_line)
    return

def parse_segment(word_morph_tree_file, prefix_nonterminal, stem_nonterminal, suffix_nonterminal, segmented_text_file,
                  segmented_dictionary_file, to_parse_file, output_file,
                  min_word_length_to_segment=2, multiway_segmentation=False):
    '''
    Function that takes the output of a word grammar file, creates a segmented
    word dictionary from its output, and uses these to replace the words in a
    text file with their segmented version. This function is a wrapper to the
    functions: parse_PYAGS_segmentation_output and segment_file
    :param word_morph_tree_file: a txt file that contains each words' morphology trees
    :param prefix_nonterminal: prefix nonterminal to parse
    :param stem_nonterminal: stem nonterminal to parse
    :param suffix_nonterminal: suffix nonterminal to parse
    :param segmented_text_file: file location to write all word segmentations
    :param segmented_dictionary_file: file location to write all word segmentations
    and their respective word
    :param to_parse_file: plaintext file containing a tokenized sequence of words.
    (All punctuation marks are separated from words by whitespace such as:
    "The dog ' s bowl is empty . ")
    :param output_file: file to write output to
    stem in the segmentation output of unseen words (inductive)
    :param min_word_length_to_segment: integer that represents the minimum length of a
    word to be segmented (in characters)
    :param multiway_segmentation: boolean value;
        if value is false, the segmented word will contain a three-way split
        (Prefix+Stem+Suffix)
        if value is true, the segmented word will contain a multi-way split
        if applicable (for example: PrefixMorph+Stem+SuffixMorph+SuffixMorph)
    :return:
    '''
    map = parse_PYAGS_segmentation_output(word_morph_tree_file, prefix_nonterminal, stem_nonterminal, suffix_nonterminal, segmented_text_file, segmented_dictionary_file)
    segment_file(map, to_parse_file, output_file, min_word_length_to_segment, multiway_segmentation)
    return


if __name__ == '__main__':
    main()
