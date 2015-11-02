#Test random sampling
import sys
sys.path.append("/Users/ingenia/git/instrumento/")
sys.path.append("/Users/ingenia/git/utilityFuncs/")
import random_sampling
import instrumento as ins
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from scipy.stats.mstats import mode
from sklearn.metrics import confusion_matrix as cm

log=ins.instrumento(filename="./pilotTest3.txt",printout=True)


log.act("start")


path="/Users/ingenia/git/data/data_sampling/"
dataFilename=path+"user_bot_data.tsv"
randFilename=path+"rand_sample.tsv"
botsFilename=path+"bots_sample.tsv"
fullRandFilename=path+"full_rand_sample.tsv"

# log.act("initial data exploration")
# data=np.genfromtxt(dataFilename,delimiter="\t")
# log.sum(data.shape,"data set size")
# log.sum(np.sum(data[:,1]),"number of bots")
# log.sum(data.shape[0]-np.sum(data[:,1]),"number of people")
# 
# ids=np.argwhere(np.isnan(data))
# print(ids.shape)
# print(mode(ids[:,1]))

# log.act("getting random sample from the data")
# random_sampling.parallel_random_sampling(0.1,[dataFilename], randFilename)


# log.act("exploring random sample")
# rData=np.genfromtxt(randFilename,delimiter="\t")
# log.sum(rData.shape,"data set size")
# log.sum(np.sum(rData[:,1]),"number of bots")
# log.sum(rData.shape[0]-np.sum(rData[:,1]),"number of people")

# log.act("filtering bots from the random data")
# rData=np.genfromtxt(randFilename,delimiter="\t")
# idx=np.argwhere(rData[:,1])
# print(idx.flat[:])
# rData=np.delete(rData,idx.flat[:],0)
# log.sum(rData.shape,"data set size")
# log.sum(np.sum(rData[:,1]),"number of bots")
# log.sum(rData.shape[0]-np.sum(rData[:,1]),"number of people")
# np.savetxt(randFilename,rData,fmt="%.2f",delimiter="\t")

# log.act("storing bots data alone")
# data=np.genfromtxt(dataFilename,delimiter="\t")
# idx=np.argwhere(data[:,1])
# botsData=data[idx.flat[:],:]
# log.sum(botsData.shape,"data set size")
# np.savetxt(botsFilename,botsData,fmt="%.2f",delimiter="\t")


# log.act("creating full random sample")
# randData=np.genfromtxt(randFilename,delimiter=" ")
# botsData=np.genfromtxt(botsFilename,delimiter=" ")
# print(randData.shape)
# print(botsData.shape)
# fullRandData=np.vstack((randData,botsData))
# log.sum(fullRandData.shape,"data set size")
# log.sum(np.sum(fullRandData[:,1]),"number of bots")
# log.sum(fullRandData.shape[0]-np.sum(fullRandData[:,1]),"number of people")
# np.savetxt(fullRandFilename,fullRandData,delimiter="\t",fmt="%.2f")

log.act("building classifier")
data=np.genfromtxt(fullRandFilename,delimiter="\t")
lr=LogisticRegression(penalty="l1",C=0.8)
log.prevLine()
X=np.c_[data[:,2:27],data[:,28]]
print(X.shape)
y=data[:,1]
ids=np.argwhere(np.isnan(X))
print(ids.shape)
lr.fit(X,y)
# log.params("LogisticRegression(penalty=\"l1\",C=0.1)")
log.sum(f1_score(lr.predict(X),y),"f1 score")
log.sum(cm(y,lr.predict(X))," confusion matrix")
print(lr.get_params())
print(lr.coef_)


log.act("end")