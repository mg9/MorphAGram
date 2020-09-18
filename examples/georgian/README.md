This directory includes the adaptor-grammar data for Georgian according to Eskander et al., 2020. The directories are as follows:

Grammar:
- A list of 22 grammars in the standard, scholar seeded and cascaded settings.
- The mapping from the grammar references in Eskander et al., 2016 and Eskander et al., 2020 is as follows:
PrStSu: Grammar0
PrStSu+SM: Grammar1
PrStSu+Co+SM: Grammar2
Simple: Grammar3
Simple+SM: Grammar4
Morph+SM: Grammar13
PrStSu2a+SM: Grammar15
PrStSu2b+SM: Grammar18
PrStSu2b+Co+SM: Grammar19

Data:
gold.txt: Gold annotated data used for evaluation (in-house annotations)
dev.txt: Unsegmented gold data
train.txt: Unsegmented training data (based on Wikipedia)
traindev.txt: Unsegmented training+gold data
lk.txt: Scholar-seeded knowledge

PyCFG
The inputs and outputs to the PYCFG sampler.
The outputs include the grammar, segmentation output and trace logs.

