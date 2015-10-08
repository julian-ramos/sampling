import os
import density_sampling as dsam
import time
import psutil, os

# Increasing priority
p = psutil.Process(os.getpid())
p.nice(10)

time_in_millis = lambda: int(round(time.time() * 1000))


mainFile="/Users/ingenia/git/data/data_sampling/user_bot_data.tsv"
path="/Users/ingenia/git/data/data_sampling/splits"
files=os.listdir(path)

files=[path+"/"+i for i in files]
print(files)


outputfilename="/Users/ingenia/git/data/data_sampling/samples/sample1_split.tsv"

t0=time_in_millis()
dsam.parallel_density_sampling(files,outputfilename,range(2,20) ,3, 3, 0.2, 10, num_parallel_jobs=8)
t1=time_in_millis()
print(t1-t0,(t1-t0)/1000.0/60.0,"Time spent using multiple files")


outputfilename="/Users/ingenia/git/data/data_sampling/samples/sample1_whole.tsv"
t2=time_in_millis()
dsam.parallel_density_sampling([mainFile],outputfilename,range(2,20) ,3, 3, 0.2, 10,  num_parallel_jobs=8)
t3=time_in_millis()
print(t3-t2,(t3-t2)/1000.0/60.0,"Time spent using a single file")
