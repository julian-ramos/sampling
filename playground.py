import os
import density_sampling as dsam

path="/Users/ingenia/git/data/data_sampling/splits"
files=os.listdir(path)

files=[path+"/"+i for i in files]
print(files)


outputfilename="/Users/ingenia/git/data/data_sampling/samples/sample1.tsv"

dsam.parallel_density_sampling(files,outputfilename,range(2,29) ,3, 3, 0.2, 5, 8)

