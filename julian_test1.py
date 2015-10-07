import pickle as pick
import density_sampling as dsam
import dataGraphs as dG
import instrumento as ins
import load_tsv
import numpy as np

file=open("./data2/user_bot_fields.txt")
header=[ i.split('.')[1] for i in file]
header=np.array(header)

log=ins.instrumento(path=".",logname="log_julian_test1")

log.act("start")
datafilename="./data2/user_bot_data.tsv"
outputfilename="./data2/user_bot_data_sample.tsv"

# 
# log.act("loading data")
# features, truth = load_tsv.load_tsv_features_truth(datafilename,[],1)
#   
# log.act("creating intermediate data set")
# features=features[1:1000,:]
# truth=truth[1:1000]
#    
# filename="./data2/intermediate_data.pik"
# file=open(filename,'wb')
# pick.dump(features,file)
# file.close()
# filename="./data2/intermediate_labels.pik"
# file=open(filename,'wb')
# pick.dump(truth,file)
# file.close()

# log.act("checking intermediate data contents")
# filename="./data2/intermediate_data.pik"
# file=open(filename,'rb')
# features=pick.load(file)
# file.close()
# filename="./data2/intermediate_labels.pik"
# file=open(filename,'rb')
# truth=pick.load(file)
# file.close()


log.act("sampling data")
dsam.parallel_density_sampling([datafilename],outputfilename,range(2,29),1,10,0.1,10)


# dG.pairPlot(features[:,18:22], truth,header=header[18:22])


log.act("end")

