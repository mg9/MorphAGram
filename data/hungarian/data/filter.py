lines =[]
with open("/kuacc/users/mugekural/workfolder/dev/git/MorphAGram/data/hungarian/data/hun.word.test.gold.tsv_FILTERED.txt", "r") as reader:
    for line in reader:
        lines.append(line.split('\t')[0]+'\n')

with open("/kuacc/users/mugekural/workfolder/dev/git/MorphAGram/data/hungarian/data/hun.filtered.txt", "w") as writer:
    for line in lines:
        writer.write(line)
