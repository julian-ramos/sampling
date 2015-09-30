import random

infile = open("data.txt","r")
outfile = open("data.tsv","w")
outfile1 = open("part1.tsv","w")
outfile2 = open("part2.tsv","w")

for line in infile:
    s = line.replace(",","\t")
    outfile.write(s)
    if random.random() > 0.5:
        outfile1.write(s)
    else:
        outfile2.write(s)
