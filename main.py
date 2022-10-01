from preprocessing import *

'''# encode data
lexicon_path = 'data/turkish/data/turkish.train'
encoded_lexicon_path = 'train.txt'
words, encoded_words, hex_chars = process_words(lexicon_path)
write_encoded_words(encoded_words, encoded_lexicon_path)

# grammar chars addition
grammar_path = 'data/turkish/grammar/standard/PrStSu_SM.txt'
final_grammar_path = 'train.cfg0.txt'
grammar = read_grammar(grammar_path)
appended_grammar = add_chars_to_grammar(grammar, hex_chars)
write_grammar(appended_grammar, final_grammar_path)
'''


# encode data
#lexicon_path = 'data/turkish/data/filtered_traindev.tur'
#lexicon_path = 'data/hungarian/data/hun.filtered.txt'
lexicon_path = 'data/finnish/data/fin.filtered.txt'

encoded_lexicon_path = 'encoded_lexicon_fin'
words, encoded_words, hex_chars = process_words(lexicon_path)
write_encoded_words(encoded_words, encoded_lexicon_path)

# grammar chars addition
grammar_path = 'data/finnish/grammar/standard/PrStSu_SM.txt'
final_grammar_path = 'final_grammar_traindev'
grammar = read_grammar(grammar_path)
appended_grammar = add_chars_to_grammar(grammar, hex_chars)
write_grammar(appended_grammar, final_grammar_path)


'''# calisti
lexicon_path = 'data/arabic/data/arabic.dev'
encoded_lexicon_path = 'encoded_lexicon'
grammar_path = 'data/arabic/grammar/standard/grammar0.txt'
final_grammar_path = 'final_grammar'
words, encoded_words, hex_chars = process_words(lexicon_path)
write_encoded_words(encoded_words, encoded_lexicon_path)
grammar = read_grammar(grammar_path)
appended_grammar = add_chars_to_grammar(grammar, hex_chars)
write_grammar(appended_grammar, final_grammar_path)'''



