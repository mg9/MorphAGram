import sys

#main_dir = '/Users/ramy/workspaces/columbia-workspace/AG-LREC-2020'
main_dir = '/Users/ramy/workspaces/columbia-workspace/AG-NAACL-2021'
#main_dir = '/Users/ramy/workspaces/columbia-workspace/AG-EMNLP-2021'

#languages = ['english', 'german', 'turkish', 'finnish', 'estonian', 'arabic', 'zulu', 'georgian', 'mexicanero', 'nahuatl', 'mayo', 'wixarika']
#languages = ['swahili', 'tagalog', 'somali', 'bulgarian', 'lithuanian', 'pashto', 'farsi']
#languages = ['japanese']
#languages = ['turkish', 'finnish', 'georgian', 'amharic']
#languages = ['english', 'german', 'turkish', 'finnish', 'estonian', 'zulu']
#languages = ['english', 'german', 'turkish', 'finnish', 'estonian', 'zulu', 'georgian']
#languages = ['georgian']
#languages = ['english', 'georgian', 'finnish', 'estonian']
languages = ['finnish', 'turkish']

#grammar_indexes = [1, 15]
#main_grammar = [0, 1, 2, 3, 4, 13, 15, 18, 19]
#grammar_indexes = [1, 15, 18]
grammar_indexes = [1, 15]

#grammar_settings = ['standard', 'standardls-1', 'standardls-2', 'standardls-3', 'standardls-4', 'standardls-5', 'standardls-6', 'standardls-7', 'standardls-8']
#grammar_settings = ['cascaded15', 'cascadednew', 'scholar_seedednew']
#grammar_settings = ['standard']
#grammar_settings = ['cascaded', 'cascadednew1', 'cascadednew2', 'cascadednew3', 'cascadednew4', 'cascadednew5']
#grammar_settings = ['cascadednew3-1', 'cascadednew3-15', 'cascadednew5-1', 'cascadednew5-15']
#grammar_settings = ['scholar_seeded', 'scholar_seedednew3', 'scholar_seedednew5']
#grammar_settings = ['standard', 'standardls-1', 'standardls-3', 'standardls-6', 'standardls-7', 'cascaded1', 'cascaded15', 'cascaded18', 'cascaded1ls-1', 'cascaded15ls-1', 'cascaded18ls-1', 'cascaded1ls-3', 'cascaded15ls-3', 'cascaded18ls-3', 'cascaded1ls-6', 'cascaded15ls-6', 'cascaded18ls-6', 'cascaded1ls-7', 'cascaded15ls-7', 'cascaded18ls-7']
grammar_settings = ['standard', 'standardls-1', 'cascaded1', 'cascaded15', 'cascaded1ls-1', 'cascaded15ls-1']

min_segmentation_length_for_research_languages = [3, 3, 3, 3, 3, 3, 3, 3, 6, 6, 6, 6]
#min_segmentation_length_for_material_languages = [3, 3, 3, 3, 3, 3, 3]
#min_segmentation_length_for_research_languages = [1]

#run_indexes = [1, 2, 3, 4, 5]
#run_indexes = [1, 2, 3]
run_indexes = [1, 2, 3]

data_types = ['traindev']
#data_types = ['bible', 'biblewiki10', 'sigmorphonbiblewiki10', 'biblewiki20', 'biblewiki30', 'sigmorphonbiblewiki20', 'sigmorphonbiblewiki30']

#splitting_setups = ['l', 'u']
splitting_setups = ['l']

eval_script = sys.argv[1]

for i in range(len(languages)):
    language = languages[i]
    data_types = ['traindev']
    if language in ['mexicanero', 'nahuatl', 'mayo', 'wixarika']:
        data_types = ['traindev', 'traindevtest']
    for data_type in data_types:
        for grammar_setting in grammar_settings:
            for grammar_index in grammar_indexes:
                for splitting_setup in splitting_setups:
                    for run_index in run_indexes:
                        gold = main_dir + '/' + language + '/data/' + language + '.dev.gold'
                        segmentation = main_dir + '/' + language + '/pycfg/' + grammar_setting + '/output/segmentation-' + splitting_setup + '-eval-' + data_type + '.cfg' + str(grammar_index) + '-' + str(run_index) + '.txt';
                        print('python3 ' + eval_script + ' -g ' + gold + ' -p ' + segmentation)