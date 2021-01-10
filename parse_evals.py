import sys

from collections import defaultdict

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

#languages_development = ['english', 'german', 'turkish', 'finnish', 'estonian', 'arabic', 'zulu', 'georgian']
#languages_development = ['japanese']
#languages_development = ['english', 'german', 'turkish', 'finnish', 'estonian', 'zulu', 'georgian']
#languages_development = ['georgian']
#languages_development = ['english', 'georgian', 'finnish', 'estonian']
languages_development = ['finnish', 'turkish']

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
#min_segmentation_length_for_material_languages = [1]

#run_indexes = [1, 2, 3, 4, 5]
#run_indexes = [1, 2, 3]
run_indexes = [1, 2, 3]

data_types = ['traindev']
#data_types = ['bible', 'biblewiki10', 'sigmorphonbiblewiki10', 'biblewiki20', 'biblewiki30', 'sigmorphonbiblewiki20', 'sigmorphonbiblewiki30']

#splitting_setups = ['l', 'u']
splitting_setups = ['l']

output_file = sys.argv[1]

results = {}
with open(output_file, "r", encoding="utf-8") as fin:
    for line in fin:
        columns = line.split('\t')
        results[columns[0]] = (columns[1], columns[2], columns[3])

all_precisions = defaultdict(float)
all_recalls = defaultdict(float)
all_fscores = defaultdict(float)

dev_precisions = defaultdict(float)
dev_recalls = defaultdict(float)
dev_fscores = defaultdict(float)

grammars = []

for i in range(len(languages)):
    language = languages[i]
    data_types = ['traindev']
    if language in ['mexicanero', 'nahuatl', 'mayo', 'wixarika']:
        data_types = ['traindev', 'traindevtest']
    for data_type in data_types:
        for grammar_setting in grammar_settings:
            for grammar_index in grammar_indexes:
                for splitting_setup in splitting_setups:
                    total_precision = 0
                    total_recall = 0
                    total_fscore = 0
                    for run_index in run_indexes:
                        segmentation = main_dir + '/' + language + '/pycfg/' + grammar_setting + '/output/segmentation-' + splitting_setup + '-eval-' + data_type + '.cfg' + str(grammar_index) + '-' + str(run_index) + '.txt';
                        (precision, recall, fscore) = results[segmentation]
                        total_precision += float(precision)
                        total_recall += float(recall)
                        total_fscore += float(fscore)
                    ave_precision = total_precision/len(run_indexes)
                    ave_recall = total_recall/len(run_indexes)
                    ave_fscore = total_fscore/len(run_indexes)
                    grammar = grammar_setting+'-'+str(grammar_index)+'-'+splitting_setup

                    grammars.append(grammar)

                    if data_type == 'traindev':
                        all_precisions[grammar] += ave_precision
                        all_recalls[grammar] += ave_recall
                        all_fscores[grammar] += ave_fscore
                        if language in languages_development:
                            dev_precisions[grammar] += ave_precision
                            dev_recalls[grammar] += ave_recall
                            dev_fscores[grammar] += ave_fscore


                    print(language+'\t'+data_type+'\t'+grammar_setting+'\t'+str(grammar_index)+'-'+splitting_setup+'\t'+str(ave_precision)+'\t'+str(ave_recall)+'\t'+str(ave_fscore))

print('------------------------------------------------------')
for grammar in set(grammars):
    print(grammar+"\t"+str(all_precisions[grammar]/len(languages))+"\t"+str(all_recalls[grammar]/len(languages))+"\t"+str(all_fscores[grammar]/len(languages)))

if len(languages_development) > 1:
    print('------------------------------------------------------')
    for grammar in set(grammars):
        print(grammar+"\t"+str(dev_precisions[grammar]/len(languages_development))+"\t"+str(dev_recalls[grammar]/len(languages_development))+"\t"+str(dev_fscores[grammar]/len(languages_development)))