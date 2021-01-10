##  MorphAGram: A Framework for Unsupervised and SemiSupervised Morphological Segmentation using Adaptor Grammars ##

### Publications

[MorphAGram, Evaluation and Framework for Unsupervised Morphological Segmentation](https://www.aclweb.org/anthology/2020.lrec-1.879.pdf "MorphAGram, Evaluation and Framework for Unsupervised Morphological Segmentation")

[Extending the Use of Adaptor Grammars for Unsupervised
Morphological Segmentation of Unseen Languages](https://www.aclweb.org/anthology/C16-1086.pdf "Extending the Use of Adaptor Grammars for Unsupervised
Morphological Segmentation of Unseen Languages")

[Unsupervised Morphological Segmentation for Low-Resource Polysynthetic Languages](https://www.aclweb.org/anthology/W19-4222.pdf "Unsupervised Morphological Segmentation for Low-Resource Polysynthetic Languages")

[Automatically Tailoring Unsupervised Morphological Segmentation to the Language](https://www.aclweb.org/anthology/W18-5808.pdf "Automatically Tailoring Unsupervised Morphological Segmentation to the Language")

---

### Preprocessing Phase

MorphAGram uses the Pitman-Yor Adaptor-Grammar Sampler (PYAGS), developed by Mark Johnson, for training. The sampler can be downloaded from [here](http://web.science.mq.edu.au/~mjohnson/code/py-cfg-2013-09-23.tgz "here").

For complete information about how the sampler works, please refer t the following [paper](https://cocosci.princeton.edu/tom/papers/adaptornips.pdf "paper").

The sampler requires two types of inputs: a grammar and a list of training units. For the purpose of unsupervised morphological segmentation, a grammar should specify word structure, while the list of training units is a list of raw words. In addition, MorphAGram requires the text to be in the Hex format in order to meet the language-independence assumption and to escape special characters. Also the grammar should have the characters in the word list as terminals.

The first step is to provide an initial CFG (Context-Free grammar) and a list of words (one word per line) to MorphAGram, which in turn converts them into inputs to PYAGS. The initial CFG should have two parameters associated with each production rule (default values are zeros). The first number represents the value of the probability of the rule in the generator, and the second number is the value of the α parameter in the Pitman-Yor process. Below is an example CFG.

*1 1 Word --> Prefix Stem Suffix<br/>
Prefix --> ^^^<br/>
Prefix --> ^^^ PrefixMorphs<br/>
1 1 PrefixMorphs --> PrefixMorph PrefixMorphs<br/>
1 1 PrefixMorphs --> PrefixMorph<br/>
PrefixMorph --> SubMorphs<br/>
Stem --> SubMorphs<br/>
Suffix --> $$$<br/>
Suffix --> SuffixMorphs $$$<br/>
1 1 SuffixMorphs --> SuffixMorph SuffixMorphs<br/>
1 1 SuffixMorphs --> SuffixMorph<br/>
SuffixMorph --> SubMorphs<br/>
1 1 SubMorphs --> SubMorph SubMorphs<br/>
1 1 SubMorphs --> SubMorph<br/>
SubMorph --> Chars<br/>
1 1 Chars --> Char<br/>
1 1 Chars --> Char Chars*

MorphAGram has three learning settings; Standard, Scholar-Seeded and Cascaded.  Here is how to preprocess the data for each setup:

#### a) Standard Setup
The standard setup is a language-independent one, with no scholar knowledge and with only one learning phase.

###### Steps:
\# Read the initial lexicon (word list), and convert it into HEX.<br/>
`words, encoded_words, hex_chars = process_words(lexicon_path)`<br/>
`write_encoded_words(encoded_words, encoded_lexicon_path)`<br/>
\# Read the initial CFG and append the HEX encoded characters as terminals.<br/>
\# encoded_lexicon_path and final_grammar_path then become the input to the PYAGS sampler.<br/>
`grammar = read_grammar(grammar_path)`<br/>
`appended_grammar = add_chars_to_grammar(grammar, hex_chars)`<br/>
`write_grammar(appended_grammar, final_grammar_path)`<br/>


#### b) Scholar-Seeded Setup
The scholar-seeded setup seeds scholar information in the form of prefixes and suffixes into the grammar tree prior to running the learning phase. The setup first requires the preparation of an LK file (LK=Linguistic Knowledge). An example LK file should be formatted as follows, where it contains an unlimited number of prefixes and suffixes.

*###PREFIXES###*<br/>
*prefix1*<br/>
*prefix2*<br/>
*prefix3*<br/>
*###SUFFIXES###*<br/>
*prefix1*<br/>
*prefix2*<br/>
*prefix3*

###### Steps:
\# Read the initial lexicon (word list), and convert it into HEX.<br/>
`words, encoded_words, hex_chars = process_words(lexicon_path)`<br/>
`write_encoded_words(encoded_words, encoded_lexicon_path)`<br/>
\# Read the initial CFG.<br/>
`grammar = read_grammar(grammar_path)`<br/>
\# Seed affixes into the grammar, where the affixes are read from the LK file.<br/>
`ss_grammar = prepare_scholar_seeded_grammar(grammar, linguistic_knowledge_path, prefix_nonterminal_to_seed_into, suffix_nonterminal_to_seed_into)`<br/>
`write_grammar(ss_grammar, ss_grammar path)`<br/>
\# Append the HEX encoded characters as terminals.<br/>
\# encoded_lexicon_path and final_grammar_path then become the input to the PYAGS sampler.<br/>
`appended_ss_grammar = add_chars_to_grammar(ss_grammar, hex_chars)`<br/>
`write_grammar(appended_ss_grammar, final_grammar_path)`<br/>

#### c) Cascaded Setup
The cascaded setup approximates the effects of the scholar-seeded setup in a language-independent manner, where affixes are generated automatically in one learning phase and then seeded into the grammar tree in a second round of learning.

###### Steps:
\# Read the initial lexicon (word list), and convert it into HEX.<br/>
`words, encoded_words, hex_chars = process_words(lexicon_path)`<br/>
`write_encoded_words(encoded_words, encoded_lexicon_path)`<br/>
\# Read the initial CFG.<br/>
`grammar = read_grammar(grammar_path)`<br/>
\# Read the automatically generated affixes from the segmentation output of some learning phase.<br/>
`cascaded_grammar = prepare_cascaded_grammar(grammar, segmentation_output_path, number_of_affixes_to_read, prefix_nonterminal_to_read, suffix_nonterminal_to_read, prefix_nonterminal_to_seed_into, suffix_nonterminal_to_seed_into)`<br/>
`write_grammar(cascaded_grammar, cascaded_grammar_path)`<br/>
\# Append the HEX encoded characters as terminals.<br/>
\# encoded_lexicon_path and final_grammar_path then become the input to the PYAGS sampler.<br/>
`appended_cascaded_grammar = add_chars_to_grammar(cascaded_grammar, hex_chars)`<br/>
`write_grammar(appended_cascaded_grammar, final_grammar_path)`<br/>

---

### Training Phase

Download and run the Pitman-Yor Adaptor-Grammar Sampler (PYAGS), developed by Mark Johnson, where the input to the sampler is the output of the preprocessing phase. The sampler can be downloaded from [here](http://web.science.mq.edu.au/~mjohnson/code/py-cfg-2013-09-23.tgz "here").

In order to replicare our results in [MorphAGram, Evaluation and Framework for Unsupervised Morphological Segmentation](https://www.aclweb.org/anthology/2020.lrec-1.879.pdf "MorphAGram, Evaluation and Framework for Unsupervised Morphological Segmentation"), please use the following parameters:
`-r 0 -d 10 -x 10 -D -E -e 1 -f 1 -g 10 -h 0.1 -w 1 -T 1 -m 0 -n 500 -R`

For complete information about how the sampler works, please refer t the following [paper](https://cocosci.princeton.edu/tom/papers/adaptornips.pdf "paper").

---

### Segmentation Phase

#### Transductive Segmentation:
Use this mode to segment words that are already seen in the training data.

###### Steps:
\# Create a segmentation model given the PYAGS segmentation output.<br/>
\# The step requires specifying which nonterminals to split on.<br/>
\# In addition to generating the segmentation model, the step generates a human-readable segmentation output that can be directly used as the prediction input for the evaluation scripts used in the Morpho-Challenge shared task.<br/>
`segmentation_model = parse_segmentation_output(segmentation_output_path, prefix_nonterminal, stem_nonterminal, suffix_nonterminal, segmentation_eval_output_path , min_word_length_to_segment)`<br/>
\# Segment white-space tokenized text string.<br/>
`segmented_text = segment_text(text_to_segment, segmentation_model, morph_separator, stem_marker, whether_to_ignore_segmenting_nonfirst_capitalized_words, min_word_length_to_segment)`<br/>
\# Segment white-space tokenized text file.<br/>
`segment_file(file_to_segment, output_path, segmentation_model, morph_separator, stem_marker, whether_to_ignore_segmenting_nonfirst_capitalized_words, min_word_length_to_segment)`<br/>

#### Deductive Segmentation:
Use this mode to segment any word (either seen or unseen in the training data).

###### Steps:
There are two ways to run deductive segmentation:<br/>
- The first method is to run the same steps as the transductive segmentation above. If a word is seen in the training data, the segmentation is read from the PYAGS output. Otherwise, the segmentation is deduced through an MLE model that assigns the segmentation that gives the highest prefix, stem and suffix probabilities, along with a valid premix-suffix compatibility. This is only applicable when the grammar assigns different nonterminals to prefixes, stems and suffixes.<br/>
- The second method is to convert the PYAGS output grammar to a format that is parsable by the CKY parser here:<br/>
http://web.science.mq.edu.au/~mjohnson/Software.htm<br/>
The conversion is achieved as follows:<br/>
`grammar = generate_grammar(pyags_output_grammar_path)`<br/>
`write_grammar(grammar, final_grammar_path)`<br/>

---

### Utility Functions

#### 1. Language analysis
\# The analysis is based on gold data, where gold_path is a tabular file, where the first column contains the words and the second column contains comma separated segmentations, where a segmentation is white-spaced morphs.<br/>
\# The analysis is assumed to be applicable to the corresponding language as long as the gold is a well representative sample.<br/>
\# gold_info: a map that contains analysis information for the gold. This includes:<br/>
word-morph mapping, number of morphs, unweighted/weighted degree of ambiguity, average token/type morph length, average number of morphs per word and the maximum number of morphs in a word.<br/>
\# morh_info: a map that contains analysis information for each morh. This includes:<br/>
morph count, morph frequency and morph probability (the probability that a sequence of characters forms the corresponding morph).<br/>
`gold_info, morph_info = analyze_gold(gold_path)`<br/>

#### 2. Segmentation-Output Analysis
\# output_path and gold_path are tabular files, where the first column contains the words and the second column containsthe segmentations, where a segmentation is white-spaced morphs. In the case of gold_path, multiple comma-separated segmentations can be listed.<br/>
\# morh_info: a map that contains analysis information for each morh. This includes:<br/>
morph count, morph frequency, morph probability (the probability that a sequence of characters forms the corresponding morph), morph precision, morph recall and morph F1-score.<br/>
`morph_info = analyze_gold(output_path, gold_path)`<br/>

#### 3. Feature Extraction
\# Given a PYAGS segmentation output, the following function extracts affix-relatred information that could then be used as ML features as pointed out [here](https://www.aclweb.org/anthology/W18-5808.pdf "here").<br/>
\# For each simple prefix, complex prefix, simple suffix and complex suffix, the information includes: type count, token count, average count per word and average length.<br/>
\# The function is only applicable when the grammar assigns different nonterminals to prefixes and suffixes.<br/>
`affix_info=get_affix_features(segmentation_output_path, prefix_nonterminal, suffix_nonterminal, min_count_of_affix_to_consider)`<br/>
