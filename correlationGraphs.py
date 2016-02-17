import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# filename="/Users/ingenia/Google Drive/Research collaborations/big data mining/data-validation/datasets/user_bot_data.tsv"
filename="/Users/ingenia/Google Drive/Research collaborations/big data mining/data-validation/datasets/user_bot_data_small_part1.tsv"
path="/Users/ingenia/git/sampling/graphs/"

data=np.genfromtxt(filename,delimiter="\t",)

correlation=[]
index1=[]
index2=[]
for i in range(2,data.shape[1]):
    for i2 in range(i,data.shape[1]):
        if i != i2:
            
            tempCorr=np.corrcoef(data[:,i],data[:,i2])
#             correlation[(i,i2)]=tempCorr[1,0]
            correlation.append(tempCorr[1,0])
            index1.append(i)
            index2.append(i2)
            plt.scatter(data[:,i],data[:,i2])
#             filename=path+"corr_%d-%d.png"%(i,i2)
            plt.title("correlation feature %d vs feature %d"%(i,i2))

#             plt.savefig(filename)
            plt.show()

a=pd.Series(correlation)
b=pd.Series(index1)
c=pd.Series(index2)

cor=pd.DataFrame()
cor['correlation']=a
cor['feat1']=b
cor['feat2']=c
print(cor.columns)
cor.to_csv(path+"correlations.csv",sep=',')

        

