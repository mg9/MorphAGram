from segmentation import parse_segmentation_output, segment_file
from analysis import *

output_path = 'hungarian.train.segments'
segmentation_model = parse_segmentation_output('/kuacc/users/mugekural/workfolder/dev/git/MorphAGram/data/hungarian/pycfg/standard/output/output-train.cfg0-s.txt', 'PrefixMorph', 'Stem', 'SuffixMorph', output_path, 'Hungarian')
#segmentation_model = parse_segmentation_output('/kuacc/users/mugekural/workfolder/dev/git/MorphAGram_YEDEK/data/turkish/pycfg/output_old/output-traindev.cfg1-s.txt', 'PrefixMorph', 'Stem', 'SuffixMorph', output_path, 'Turkish')


segmented_text = segment_file('/kuacc/users/mugekural/workfolder/dev/git/MorphAGram/data/hungarian/data/hun.test.txt', '/kuacc/users/mugekural/workfolder/dev/git/MorphAGram/data/hungarian/data/hun.out', segmentation_model, "\t", "\t", False, 'Hungarian' )


'''
wmorphs = dict()
with open(output_path, 'r') as reader:
    for line in reader:
        word, morphs = line.strip().split('\t')
        wmorphs[word] = morphs

# write only morphemes to file
words = []
with open('data/turkish/data/turkish.dev', 'r') as reader:
    for line in reader:
        words.append(line.strip())
with open('ag_mc05-10agg.segments', 'w') as f:
    for word in words:
        if word in wmorphs:
            f.write(wmorphs[word]+'\n')
'''
        