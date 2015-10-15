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
from sklearn import svm
import os
from __builtin__ import file


path="/Users/ingenia/git/sampling"
dataFilename="/Users/ingenia/git/data/data_sampling/user_bot_data.tsv"
log=ins.instrumento(filename=path+"/pilotTest1.txt")
splitPath="/Users/ingenia/git/data/data_sampling/splits"
random_sample_filename="/Users/ingenia/git/data/data_sampling/random_sample.tsv"

prefix='split'
lines=10000

log.act("start")

# log.act("loading data")
# features,labels=load_tsv.load_tsv_features_truth(dataFilename,range(2,29),1)
# print(features.shape)


# df=pandas.DataFrame(features[1:1000,:])
# log.act("getting description of the data")
# print(df.describe())
# log.act("density sampling of 5 features")


# log.act("getting the rate of bots vs humans")
# print(np.sum(labels)/(1.0*labels.shape[0]))

# log.act("splitting original data set")
# spi.splitter(dataFilename,splitPath,prefix,lines)
#  

#TODO
# Random sampling is not working very nicely
# for instance the option that generates files with the same name as
# the source data files needs to be fixed and generate a single data file
# ideally all the random sample files are created in a single folder
# and later they are erased together with the folder

log.act("using random sampling to create a training data set")
files=os.listdir(splitPath)
files=[splitPath+"/"+i for i in files if "tsv" in i]
rs.parallel_random_sampling(0.5,files,random_sample_filename)

log.act("checking random sample")
rdata=np.genfromtxt(random_sample_filename,delimiter="\t")
print(rdata.shape)
print(np.sum(rdata[:,1]))

# log.act("query by committee sampling")
# log.act("training models")
# svm.SVC(kernel="rbf",probability=True)



log.act("end") 