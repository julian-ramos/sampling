# import sys
# sys.path.append("/Users/ingenia/git/instrumento/")
# sys.path.append("/Users/ingenia/git/utilityFuncs/")
# import random_sampling
# 
# 
# 
# path="/Users/ingenia/git/data/data_sampling/previous_data/"
# print random_sampling.parallel_random_sampling(0.1,[path+"part1.tsv",path+"part2.tsv"], "/Users/ingenia/git/data/data_sampling/previous_data/rand_sample.tsv")
# print random_sampling.parallel_outbox_sampling((30,30,"*","*"),(60,60,"*","*"),0.1,[path+"part1.tsv",path+"part2.tsv"], 8)
# print random_sampling.parallel_inbox_sampling((30,30,"*","*"),(60,60,"*","*"),0.1,[path+"part1.tsv",path+"part2.tsv"], 8)


# import sys
# sys.path.append("/Users/ingenia/git/instrumento/")
# sys.path.append("/Users/ingenia/git/utilityFuncs/")
# 
# import instrumento as ins
# 
# 
# log=ins.instrumento(filename="./someTest1.txt",printout=True)
# log.act("start")
# log.paramString("LogisticRegression(penalty=\"l1\",C=0.1)")
# a=1
# b=2
# c=3
# log.params(a,b,c)
# log.sum("accuracy = 0.7")
# log.act("end")
from numpy import NaN
import numpy as np
a=[[1, 2 ,3],[4,5,6]]
a=np.array(a)
b=a[:,:2]
d=a[:,2]
print(b.shape)
print(d.shape)
c=np.c_[b,d]
print(c)
# print(a)
# print(np.vstack((a[:,0],a[:,2])))


