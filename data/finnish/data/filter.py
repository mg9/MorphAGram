lines =[]
with open("/kuacc/users/mugekural/workfolder/dev/git/MorphAGram/data/finnish/data/goldstd_combined.segments.fin_filtered", "r", encoding = "ISO-8859-1") as reader:
    for line in reader:
        lines.append(line.strip().split('	')[0]+'\n')

with open("/kuacc/users/mugekural/workfolder/dev/git/MorphAGram/data/finnish/data/fin.filtered.tst.txt", "w") as writer:
    for line in lines:
        writer.write(line)
