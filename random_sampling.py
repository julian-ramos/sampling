# import sys
# sys.path.append("/Users/ingenia/git/instrumento/")

import parallel_jobs
import random
import instrumento as ins
import stringUtils as sU
import os
import numpy as np
import shutil
import dataOps as dO

def parallel_random_sampling(p, filenames,outputFilename, num_parallel_jobs=8):
    """
    parallel_random_sampling
    This function performs random sampling on a file and produces
    a random sample. The random sample file will be stored in the same
    folder were the data is with the prefix -rand
    
    p         :    is the probability of each sample from each file being chosen 
    filenames :    List of files to be used for the random sampling
   Note, we are not guaranteeing that p*filesize samples will be chosen
   filenames are strings of files to open and sample from
   """
    log=ins.instrumento()
    log.act("start random sampling")
    log.params(p, filenames)
    if p >= 1.0 or p < 0.0: 
        print "Invalid probability, must be (0.0, 1.0]"
    
    files=[]
    path=""
    folderstoDelete=[]
    
        
#     for i in filenames:
#         idx=np.random.randint(0,10,5)
#         idx=[str(s) for s in idx]
#         idx="".join(idx)
#         path=sU.extractPath(i)+"/temp_"+idx
#         folderstoDelete.append(path)
#         if not(os.path.isdir(path)):
#             os.mkdir(path)
#         files+=dO.splitter(i,path,prefix="split")


    folderstoDelete,files=dO.createSplitFolder(filenames)
        
    #Currently because of this line of code it will only work with a single    
    path=dO.createFolder(filenames[0])
    folderstoDelete.append(path)
        
    job_args = []
    for filename in files:
        
        job_args.append((p,filename,path))
        
        
    
            
    job_results = parallel_jobs.parallel_jobs(random_sampling,job_args,num_parallel_jobs)
    
    
    
    randFiles=[ i[0] for i in job_results]
    
#     print(job_results)
    
    
    dO.combiner(randFiles,outputFilename)
    log.act("end random sampling")
    
#     print(folderstoDelete)
    
    for i in folderstoDelete:
        shutil.rmtree(i)
#         print("to delete %s"%(i))
    
    #TODO
#     Consider erasing all of the files in path once done
#     also erase all of the random files
    
    
    return job_results

def random_sampling(in_args):
    probability, filename,outputPath = in_args
        
    count = 0
    random.seed(None)
#     return filename
#     
    outputfilename = outputPath+"/"+sU.extractFilename(filename)+"-rand-"+str(probability)+".tsv"
#     outputfilename = filename+"-rand-"+str(probability)
    inputfile = open(filename, "r")
    outputfile = open(outputfilename,"w")
          
    for line in inputfile:
        if random.random() < probability:
            outputfile.write(line)
            count = count + 1
      
    outputfile.close()
    inputfile.close()
          
    return [outputfilename, count]


# looks for points outside bounding box and samples from that (numbers only)
# "*" for a feature means anything is ok to sample in this feature
# bottom_left is all the smaller values, top_right is all the larger values
# assumes tab separated format
def parallel_outbox_sampling(bottom_left, top_right, p, filenames, num_parallel_jobs=8):
    log=ins.instrumento()
    log.act("start outbox sampling")
    log.params(bottom_left, top_right, p, filenames)
    if p > 1.0 or p < 0.0: 
        print "Invalid probability, must be (0.0, 1.0]"
    
    job_args = []
    for filename in filenames:
        job_args.append((bottom_left, top_right, p, filename))
            
    job_results = parallel_jobs.parallel_jobs(outbox_sampling,job_args,num_parallel_jobs)
    log.act("end outbox sampling")
    return job_results

    
def outbox_sampling(in_args):
    bottom_left, top_right, p, filename = in_args
        
    count = 0
    random.seed(None)
    outputfilename = filename+"-outbb-"+str(p)
    inputfile = open(filename,"r")
    outputfile = open(outputfilename,"w")
        
    if len(bottom_left) != len(top_right):
        print "bounding box feature lengths do not match"
        return []

    for line in inputfile:
        outside_bound = True
        vals = line.split("\t")
        if len(vals) != len(bottom_left):
            print "feature lengths do not match in "+filename+"\n"
            print line
            return [outputfilename, count]
        for i in range(len(vals)):
            this_bound = (bottom_left[i]=="*" or top_right[i]=="*" or float(vals[i]) < bottom_left[i] or float(vals[i]) > top_right[i])
            outside_bound = outside_bound and this_bound
        if outside_bound and random.random() < p:
            outputfile.write(line)
            count = count + 1

    outputfile.close()
    inputfile.close()
    return [outputfilename, count]


# looks for points INside bounding box and samples from that (numbers only)
# "*" for a feature means anything is ok to sample in this feature
# bottom_left is all the smaller values, top_right is all the larger values
# assumes tab separated format
def parallel_inbox_sampling(bottom_left, top_right, p, filenames, num_parallel_jobs=8):
    log=ins.instrumento()
    log.act("start inbox sampling")
    log.params(bottom_left, top_right, p, filenames)
    if p >= 1.0 or p < 0.0: 
        print "Invalid probability, must be (0.0, 1.0]"
        
    job_args = []
    for filename in filenames:
        job_args.append((bottom_left, top_right, p, filename))
            
    job_results = parallel_jobs.parallel_jobs(inbox_sampling,job_args,num_parallel_jobs)
    log.act("end inbox sampling")
    return job_results

def inbox_sampling(in_args):
    bottom_left, top_right, p, filename = in_args
    
    count = 0
    random.seed(None)
    outputfilename = filename+"-inbb-"+str(p)
    inputfile = open(filename,"r")
    outputfile = open(outputfilename,"w")
        
    if len(bottom_left) != len(top_right):
        print "bounding box feature lengths do not match"
        return []

    for line in inputfile:
        inside_bound = True
        vals = line.split("\t")
        if len(vals) != len(bottom_left): 
            print "feature lengths do not match in "+filename+"\n"
            print line
            return [outputfilename, count]
        for i in range(len(vals)):
            inside_bound = inside_bound and (bottom_left[i]=="*" or top_right[i]=="*" or (float(vals[i]) > bottom_left[i] and float(vals[i]) < top_right[i]))
        if inside_bound and random.random() < p:
            outputfile.write(line)
            count = count + 1

    outputfile.close()
    inputfile.close()
    return [outputfilename, count]


    
    

#parallel_random_sampling(0.1,["data/part1.tsv","data/part2.tsv"],8)
#parallel_outbox_sampling((30,30,"*","*"),(60,60,"*","*"),0.1,["data/part1.tsv","data/part2.tsv"],8)
#parallel_inbox_sampling((30,30,"*","*"),(60,60,"*","*"),0.1,["data/part1.tsv","data/part2.tsv"],8)

if __name__=="__main__":
    print("Testing random sampling")
#     parallel_random_sampling(0.1, ["/Users/ingenia/git/data/data_sampling/user_bot_data.tsv"], 
#                              "/Users/ingenia/git/data/data_sampling/random_sample.tsv")
    
    path="/Users/ingenia/git/data/data_sampling/previous_data/"
    
    print parallel_random_sampling(0.1,[path+"part1.tsv",path+"part2.tsv"], "/Users/ingenia/git/data/data_sampling/previous_data/rand_sample.tsv")
    print parallel_outbox_sampling((30,30,"*","*"),(60,60,"*","*"),0.1,[path+"part1.tsv",path+"part2.tsv"], 8)
    print parallel_inbox_sampling((30,30,"*","*"),(60,60,"*","*"),0.1,[path+"part1.tsv",path+"part2.tsv"], 8)
