import re
from collections import defaultdict

def convert_string_to_hex(string):
    """
    This function converts a regular string into its HEX representation.
    :param string: regular string
    :return: HEX representation
    """

    try:
        hex_chars = []
        for char in list(string):
            hex_char = char.encode('utf-16').hex()
            hex_chars.append(hex_char)
        return ' '.join(hex_chars)
    except:
        print(ERROR_MESSAGE)
        return None


def convert_hex_to_string(hex):
    """
    This function converts a HEX string into its regular representation.
    :param hex: HEX string
    :return: regular representation
    """

    try:
        string = bytes.fromhex(hex).decode('utf-16')
        # Remove trailing new line character if necessary.
        if list(string)[0] == '\x00':
            return str(list(string)[1])
        else:
            return string
    except:
        print(ERROR_MESSAGE)
        return None


def sort_unique(sequence):
    """
    This function sorts a list and removes duplicates.
    :param sequence: a list
    :return: sorted and unique elements
    """

    try:
        sequence.sort()
        seen = set()
        return [x for x in sequence if not (x in seen or seen.add(x))]
    except:
        print(ERROR_MESSAGE)
        return None


def get_morphs_from_tree(tree, nonterminals):
    """
    This function gets the different nonterminals from a morphological parse tree
    :param tree :a line in the segmentation output
    Example: "(Word (Prefix#110 ^^^ (Chars (Char fffe6200) (Chars (Char fffe6500))))
    (Stem#52 (Chars (Char fffe6300) (Chars (Char fffe6f00) (Chars (Char fffe6d00)))))
    (Suffix#1109 (Chars (Char fffe6500) (Chars (Char fffe7300))) $$$))
    :param nonterminals: nonterminals to patse
    :return: a map of nonterminals and their terminal values (characters)
    """

    try:
        morphs = defaultdict(list)
        parts = tree.split()
        # Loop over each nonterminal.
        for nonterminal in set(nonterminals):
            read = False
            count = 0
            current_chars = []
            # Read the components of the current tree.
            for part in parts:
                if not read and re.match('^\(?' + nonterminal + '(#[0-9]+)?$', part):
                    read = True
                # Read the characters.
                elif read and re.match('^([a-f\d]{4,8})\)*$', part):
                    hex_str = part.replace(')', '')
                    current_chars.append(convert_hex_to_string(hex_str))
                if read:
                    # Keeo track of the parentheses.
                    count += part.count('(')
                    count -= part.count(')')
                    if count <= 0:
                        # Detect the current morph.
                        if len(current_chars) > 0:
                            morph = ''.join(current_chars)
                            morphs[nonterminal].append(morph)
                        read = False
                        count = 0
                        current_chars = []
        return morphs
    except:
        print(ERROR_MESSAGE)
        return None
