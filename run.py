from preprocessing import *
from utils import *
from constants import *
from segmentation import *
from analysis import *


segmentation_model = parse_segmentation_output('/Users/ramy/workspaces/columbia-workspace/AG-LREC-2020/english/pycfg/standard/output/output-traindev.cfg1-1.txt', 'PrefixMorph', 'Stem', 'SuffixMorph', 'out.txt' , 3)
segmented_text = segment_text('offshores players Playing plays', segmentation_model, '+', '@@', True, 3)
print(segmented_text)
segmented_text = segment_text('offshores players Playing plays', segmentation_model, '+', '@@', False, 3)
print(segmented_text)
segment_file('in.txt', 'seg-in.txt', segmentation_model, '+', '@@', False, 3)
exit(1)

'''
languages = ['english'] #, 'german', 'turkish', 'finnish', 'estonian', 'arabic', 'zulu', 'georgian', 'mexicanero', 'nahuatl', 'mayo', 'wixarika']
for language in languages:
    print(language)
    gold_info, morph_info = analyze_gold('/Users/ramy/workspaces/columbia-workspace/AG-LREC-2020/'+language+'/data/'+language+'.dev.gold')
    morph_info = analyze_output('/Users/ramy/workspaces/columbia-workspace/AG-LREC-2020/'+language+'/pycfg/standard/output/segmentation-l-eval-traindev.cfg1-1.txt', '/Users/ramy/workspaces/columbia-workspace/AG-LREC-2020/'+language+'/data/'+language+'.dev.gold')
    for morph in morph_info:
        if morph_info[morph][COUNT] >= 5:
            print(morph + '\t' + str(morph_info[morph][COUNT]) + '\t' + str(morph_info[morph][FREQUENCY]) + '\t' + str(morph_info[morph][PROBABILITY]) +  '\t' + str(morph_info[morph][PRECISION]) + '\t' + str(morph_info[morph][RECALL]) + '\t' + str(morph_info[morph][F1SCORE]))

exit(1)
'''

prefix_lower_nonterminals = {}
prefix_lower_nonterminals[0] = 'PrefixMorph'
prefix_lower_nonterminals[1] = 'PrefixMorph'
prefix_lower_nonterminals[2] = 'PrefixMorph'
prefix_lower_nonterminals[3] = 'Prefix'
prefix_lower_nonterminals[4] = 'Prefix'
prefix_lower_nonterminals[13] = 'Morph'
prefix_lower_nonterminals[15] = 'PrefixMorph'
prefix_lower_nonterminals[18] = 'PrefixMorph'
prefix_lower_nonterminals[19] = 'PrefixMorph'

prefix_upper_nonterminals = {}
prefix_upper_nonterminals[0] = 'PrefixMorphs'
prefix_upper_nonterminals[1] = 'PrefixMorphs'
prefix_upper_nonterminals[2] = 'Compound'
prefix_upper_nonterminals[3] = 'Prefix'
prefix_upper_nonterminals[4] = 'Prefix'
prefix_upper_nonterminals[13] = 'Morph'
prefix_upper_nonterminals[15] = 'PrefixMorphs'
prefix_upper_nonterminals[18] = 'PrefixMorphs'
prefix_upper_nonterminals[19] = 'Compound'

stem_lower_nonterminals = {}
stem_lower_nonterminals[0] = 'Stem'
stem_lower_nonterminals[1] = 'Stem'
stem_lower_nonterminals[2] = 'Stem'
stem_lower_nonterminals[3] = 'Stem'
stem_lower_nonterminals[4] = 'Stem'
stem_lower_nonterminals[13] = 'Morph'
stem_lower_nonterminals[15] = 'Stem'
stem_lower_nonterminals[18] = 'Stem'
stem_lower_nonterminals[19] = 'Stem'

stem_upper_nonterminals = {}
stem_upper_nonterminals[0] = 'Stem'
stem_upper_nonterminals[1] = 'Stem'
stem_upper_nonterminals[2] = 'Compound'
stem_upper_nonterminals[3] = 'Stem'
stem_upper_nonterminals[4] = 'Stem'
stem_upper_nonterminals[13] = 'Morph'
stem_upper_nonterminals[15] = 'Stem'
stem_upper_nonterminals[18] = 'Stem'
stem_upper_nonterminals[19] = 'Compound'

suffix_lower_nonterminals = {}
suffix_lower_nonterminals[0] = 'SuffixMorph'
suffix_lower_nonterminals[1] = 'SuffixMorph'
suffix_lower_nonterminals[2] = 'SuffixMorph'
suffix_lower_nonterminals[3] = 'Suffix'
suffix_lower_nonterminals[4] = 'Suffix'
suffix_lower_nonterminals[13] = 'Morph'
suffix_lower_nonterminals[15] = 'SuffixMorph'
suffix_lower_nonterminals[18] = 'SuffixMorph'
suffix_lower_nonterminals[19] = 'SuffixMorph'

suffix_upper_nonterminals = {}
suffix_upper_nonterminals[0] = 'SuffixMorphs'
suffix_upper_nonterminals[1] = 'SuffixMorphs'
suffix_upper_nonterminals[2] = 'Compound'
suffix_upper_nonterminals[3] = 'Suffix'
suffix_upper_nonterminals[4] = 'Suffix'
suffix_upper_nonterminals[13] = 'Morph'
suffix_upper_nonterminals[15] = 'SuffixMorphs'
suffix_upper_nonterminals[18] = 'SuffixMorphs'
suffix_upper_nonterminals[19] = 'Compound'

#main_dir = '/Users/ramy/workspaces/columbia-workspace/AG-LREC-2020'
#main_dir = '/Users/ramy/workspaces/columbia-workspace/AG-NAACL-2021'
#main_dir = '/Users/ramy/workspaces/columbia-workspace/AG-EMNLP-2021'
main_dir = '/Users/ramy/workspaces/columbia-workspace/MorphAGram/examples/'

#languages = ['english', 'german', 'turkish', 'finnish', 'estonian', 'arabic', 'zulu', 'georgian', 'mexicanero', 'nahuatl', 'mayo', 'wixarika']
#languages = ['swahili', 'tagalog', 'somali', 'bulgarian', 'lithuanian', 'pashto', 'farsi']
#languages = ['japanese']
#languages = ['turkish', 'finnish', 'georgian', 'amharic']
#languages = ['english', 'german', 'turkish', 'finnish', 'estonian', 'zulu', 'georgian']
#languages = ['english', 'german', 'turkish', 'finnish', 'estonian', 'zulu', 'georgian']
#languages = ['english']
#languages = ['english', 'georgian', 'finnish', 'estonian']
#languages = ['turkish', 'finnish']
languages = ['georgian']

#grammar_indexes = [1, 15]
grammar_indexes = [0, 1, 2, 3, 4, 13, 15, 18, 19]
#grammar_indexes = [1, 15, 18]
#grammar_indexes = [1, 15]

#grammar_settings = ['standard', 'standardls-1', 'standardls-2', 'standardls-3', 'standardls-4', 'standardls-5', 'standardls-6', 'standardls-7', 'standardls-8']
#grammar_settings = ['cascaded15', 'cascadednew', 'scholar_seedednew']
#grammar_settings = ['cascaded', 'scholar_seeded', 'standard']
#grammar_settings = ['cascadednew1', 'cascadednew2', 'cascadednew3', 'cascadednew4', 'cascadednew5']
#grammar_settings = ['scholar_seeded3']
#grammar_settings = ['cascadednew3-1', 'cascadednew3-15', 'cascadednew5-1', 'cascadednew5-15']
#grammar_settings = ['scholar_seedednew3', 'scholar_seedednew5']
#grammar_settings = ['standard', 'standardls-1', 'standardls-3', 'standardls-6', 'standardls-7', 'cascaded1', 'cascaded15', 'cascaded18', 'cascaded1ls-1', 'cascaded15ls-1', 'cascaded18ls-1', 'cascaded1ls-3', 'cascaded15ls-3', 'cascaded18ls-3', 'cascaded1ls-6', 'cascaded15ls-6', 'cascaded18ls-6', 'cascaded1ls-7', 'cascaded15ls-7', 'cascaded18ls-7']
#grammar_settings = ['standard', 'standardls-1', 'cascaded1', 'cascaded15', 'cascaded1ls-1', 'cascaded15ls-1']
grammar_settings = ['standard', 'cascaded', 'scholar_seeded']

min_segmentation_length_for_research_languages = [3, 3, 3, 3, 3, 3, 3, 3, 6, 6, 6, 6]
#min_segmentation_length_for_material_languages = [3, 3, 3, 3, 3, 3, 3]
#min_segmentation_length_for_research_languages = [1]

#run_indexes = [1]
#run_indexes = [1, 2, 3]
run_indexes = [1, 2, 3, 4, 5]

data_types = ['traindev']
#data_types = ['bible', 'biblewiki10', 'sigmorphonbiblewiki10', 'biblewiki20', 'biblewiki30', 'biblewiki40', 'biblewiki50', 'sigmorphonbiblewiki20', 'sigmorphonbiblewiki30', 'sigmorphonbiblewiki40', 'sigmorphonbiblewiki50']

####################################################
#### GENERATE EVALUATION FILES ####
####################################################

for i in range(len(languages)):
    language = languages[i]
    min_segmentation_length = min_segmentation_length_for_research_languages[i]
    print("Processing " + language + "...")
    data_types = ['traindev']
    if language in ['mexicanero', 'nahuatl', 'mayo', 'wixarika']:
        data_types = ['traindev', 'traindevtest']
    for grammar_setting in grammar_settings:
        for grammar_index in grammar_indexes:
            for data_type in data_types:
                for run_index in run_indexes:
                    output_file = main_dir + '/' + language + '/pycfg/' + grammar_setting + '/output/output-' + data_type + '.cfg' + str(grammar_index) + '-' + str(run_index) + '.txt';
                    if grammar_index in [1, 15]:
                        parse_segmentation_output(output_file, prefix_lower_nonterminals[grammar_index], 'StemMorph' if ('ls-2' in grammar_setting or 'ls-3' in grammar_setting or 'ls-4' in grammar_setting or 'ls-5' in grammar_setting) else stem_lower_nonterminals[grammar_index], suffix_lower_nonterminals[grammar_index],
                                                        output_file.replace("output-", "segmentation-"),
                                                        min_segmentation_length)

                    if grammar_index in [0, 2, 4, 13, 18, 19]:
                        parse_segmentation_output(output_file, prefix_upper_nonterminals[grammar_index], stem_upper_nonterminals[grammar_index], suffix_upper_nonterminals[grammar_index],
                                                        output_file.replace("output-", "segmentation-"),
                                                        min_segmentation_length)


####################################################
#### BUILD GRAMMARS ####
####################################################
'''
for language in languages:
    print("Processing " + language + "...")
    if language in ['mexicanero', 'nahuatl', 'mayo', 'wixarika']:
        data_types = ['traindev', 'traindevtest']
    for grammar_index in grammar_indexes:
        for data_type in data_types:
            if language == 'amharic' and 'sigmorphon' in data_type:
                continue
            for grammar_type in grammar_settings:
                words, encoded_words, hex_chars = process_words(main_dir+'/'+language + '/'+'data'+'/'+language + '.' + data_type)
                write_encoded_words(encoded_words, main_dir+'/'+language+'/'+'pycfg'+'/'+grammar_type+'/'+data_type+'.txt')
                grammar = read_grammar(main_dir+'/'+language+'/'+'grammar'+'/'+'standard'+'/'+'grammar'+str(grammar_index)+'.txt')
                output_file = main_dir+'/'+language+'/'+'pycfg'+'/'+'standardls-1'+'/'+'output'+'/'+'output-'+data_type+'.cfg1-1.txt'
                cascaded_grammar = prepare_cascaded_grammar(grammar, output_file, 40, 'PrefixMorph', 'SuffixMorph', prefix_lower_nonterminals[grammar_index], suffix_lower_nonterminals[grammar_index])
                write_grammar(cascaded_grammar, main_dir+'/'+language+'/'+'grammar'+'/'+grammar_type+'/'+'grammar'+str(grammar_index)+'.txt')
                appended_cascaded_grammar = add_chars_to_grammar(cascaded_grammar, hex_chars)
                write_grammar(appended_cascaded_grammar, main_dir+'/'+language+'/'+'pycfg'+'/'+grammar_type+'/'+data_type+'.cfg'+str(grammar_index)+'.txt')
     
    for grammar_index in grammar_indexes:
        for data_type in data_types:
            if language == 'amharic' and 'sigmorphon' in data_type:
                continue
            grammar_type ='standard'
            words, encoded_words, hex_chars = process_words(main_dir+'/'+language+'/'+'data'+'/'+language + '.' + data_type)
            write_encoded_words(encoded_words, main_dir+'/'+language+'/'+'pycfg'+'/'+grammar_type+'/'+data_type+'.txt')
            grammar = read_grammar(main_dir+'/'+language+'/'+'grammar'+'/'+grammar_type+'/'+'grammar'+str(grammar_index)+'.txt')
            appended_grammar = add_chars_to_grammar(grammar, hex_chars)
            write_grammar(appended_grammar, main_dir+'/'+language+'/'+'pycfg'+'/'+grammar_type+'/'+data_type+'.cfg'+str(grammar_index)+'.txt')
    
    for grammar_index in grammar_indexes:
        for data_type in data_types:
            grammar_type = 'scholar_seedednew5'
            words, encoded_words, hex_chars = process_words(main_dir+'/'+language + '/'+'data'+'/'+language + '.' + data_type)
            write_encoded_words(encoded_words, main_dir+'/'+language+'/'+'pycfg'+'/'+grammar_type+'/'+data_type+'.txt')
            grammar = read_grammar(main_dir+'/'+language+'/'+'grammar'+'/'+'standard'+'/'+'grammar'+str(grammar_index)+'.txt')
            ss_grammar = prepare_scholar_seeded_grammar(grammar, main_dir +'/' + language +'/' +'data' +'/' +'lk.txt', prefix_lower_nonterminals[grammar_index], suffix_lower_nonterminals[grammar_index])
            write_grammar(ss_grammar, main_dir+'/'+language+'/'+'grammar'+'/'+grammar_type+'/'+'grammar'+str(grammar_index)+'.txt')
            appended_ss_grammar = add_chars_to_grammar(ss_grammar, hex_chars)
            write_grammar(appended_ss_grammar, main_dir+'/'+language+'/'+'pycfg'+'/'+grammar_type+'/'+data_type+'.cfg'+str(grammar_index)+'.txt')
    '''
'''
grammar = generate_grammar('/Users/ramy/workspaces/columbia-workspace/AG-LREC-2020/english/pycfg/standard/output/grammar-traindev.cfg1-1.txt', ['Prefix', 'Suffix', 'Stem', 'PrefixMorph', 'SuffixMorph', 'SubMorph'])
for g in grammar:
    print(g)
'''

'''
parse_segment('/Users/ramy/workspaces/columbia-workspace/AG-LREC-2020/english/pycfg/standard/output/output-traindev.cfg1-1.txt', 'PrefixMorph', 'Stem', 'SuffixMorph', '/Users/ramy/1.txt', '/Users/ramy/2.txt', '/Users/ramy/3.txt', '/Users/ramy/workspaces/columbia-workspace/MorphAGram/to_test_data', '/Users/ramy/workspaces/columbia-workspace/MorphAGram/out')
'''


'''
with open('/Users/ramy/workspaces/columbia-workspace/AG-ACL-2021/japanese/pycfg/standard/traindev.txt', 'r', encoding="utf-8") as fin:
    for line in fin:
        line = line.replace("^^^", "").replace("$$$", "").strip();
        word = ''
        for char in line.split():
            word += convert_hex_to_string(char)
        print(word)
        
ALL_HEX = []
with open('/Users/ramy/workspaces/columbia-workspace/AG-ACL-2021/japanese/pycfg/standard/traindev.cfg1.txt', 'r', encoding="utf-8") as fin:
    for line in fin:
        if 'Char -->' in line:
            line = line.strip()
            ALL_HEX.append(line.split()[-1])
ALL_HEX = set(ALL_HEX)

words, encoded_words, hex_chars = process_words('/Users/ramy/workspaces/columbia-workspace/AG-ACL-2021/japanese/data/japanese.traindev')
write_encoded_words(encoded_words, '/Users/ramy/workspaces/columbia-workspace/AG-ACL-2021/japanese/pycfg/standard/traindev.txt')
write_encoded_words(encoded_words, '/Users/ramy/workspaces/columbia-workspace/AG-ACL-2021/japanese/pycfg/standardls/traindev.txt')

for h in hex_chars:
    if h not in ALL_HEX:
        print(h, convert_hex_to_string(h))
'''


