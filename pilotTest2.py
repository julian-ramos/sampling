import numpy as np
import instrumento as ins
import sklearn
import density_sampling as ds
import query_by_committee_sampling as qbc
import random_sampling as rs
import load_tsv
import splitter as spi
import pandas
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
import pickle
import os
import csv
import matplotlib.pyplot as plt
import dataGraphs as dG

log=ins.instrumento(filename="./pilotTest1.txt")
log.act("start")
dataFilename="/Users/ingenia/git/data/data_sampling/user_bot_data.tsv"
randomFilename="/Users/ingenia/git/data/data_sampling/random_sample_p2.tsv"
botsFilename="/Users/ingenia/git/data/data_sampling/botsData.tsv"
ranplusbotFilename="/Users/ingenia/git/data/data_sampling/ranplusbot.tsv"

# file=open(dataFilename,'r')
# count=0
# data=[]
# for i in file:
#     data.append( [float(i2) for i2 in i.split("\t")])
#     count+=1
#     if count>=5000:
#         break
# file.close()
# data=np.array(data)

# log.act("loading data set")
# data=np.genfromtxt(dataFilename, delimiter="\t")

# log.act("Checking the size and distribution of the data set")
# print(data.shape)
# print(np.sum(data[:,1]),data.shape[0]-np.sum(data[:,1]))

# log.act("Creating a sample for the bots data only")
# ids=np.argwhere(data[:,1]==1)
# print(ids.shape)
# botsData=data[ids.flat[:],:]
# print(botsData.shape)
# np.savetxt(botsFilename,botsData,delimiter="\t")



# log.act("Creating a random sample")
# rs.parallel_random_sampling(0.1, [dataFilename],randomFilename)
   
# log.act("Loading random sample and checking proportion of bots to users")
# data=np.genfromtxt(randomFilename, delimiter="\t")
# print(np.sum(data[:,1]),data.shape[0]-np.sum(data[:,1]))
    
    
# log.act("removing bots data from the random sample")
# ids=np.argwhere(data[:,1]==1)
# print(ids.shape)
# data=np.delete(data,ids.flat[:],0)
# print(data.shape)
# # np.savetxt(randomFilename,data,delimiter="\t")
# np.savetxt(randomFilename,data,fmt="%.2f")


# log.act("loading random sample and bots sample and putting it together")
# botsData=np.genfromtxt(botsFilename)
# randomData=np.genfromtxt(randomFilename)    
# data=np.vstack((botsData,randomData))
# print(data.shape)

# log.act("storing random + bots data set")
# np.savetxt(ranplusbotFilename,data,delimiter="\t",fmt="%.2f")

# log.act("training a regression model on the randplusbotdata.tsv")

# data=np.genfromtxt(ranplusbotFilename)
# log.paramString("LogisticRegression(penalty=\"l1\",C=0.1)")
# lr=LogisticRegression(penalty="l1")
# x=data[:,2:]
# y=data[:,1]
# print(x.shape,y.shape)

# print(np.any(np.isnan(x)))
# dG.pairPlot(x, y)
# plt.scatter(x[:,0],y)
# plt.show()



# lr.fit(X,y)
# print(lr.score(X, y))

log.act("end")