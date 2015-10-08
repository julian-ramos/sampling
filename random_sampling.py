import parallel_jobs
import random
import instrumento as ins

#p is the probability of each sample from each file being chosen 
#   Note, we are not guaranteeing that p*filesize samples will be chosen
#filenames are strings of files to open and sample from
def parallel_random_sampling(p, filenames, num_parallel_jobs=8):
    ins.instrumento()
    ins.act("start random sampling")
    ins.params(p, filenames)
    if p >= 1.0 or p < 0.0: 
        print "Invalid probability, must be (0.0, 1.0]"
        
    job_args = []
    for filename in filenames:
        job_args.append((p,filename))
            
    job_results = parallel_jobs.parallel_jobs(random_sampling,job_args,num_parallel_jobs)
    ins.act("end random sampling")
    return job_results

def random_sampling(in_args):
    probability, filename = in_args
        
    count = 0
    random.seed(None)
    outputfilename = filename+"-rand-"+str(probability)
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
    ins.instrumento()
    ins.act("start outbox sampling")
    ins.params(bottom_left, top_right, p, filenames)
    if p > 1.0 or p < 0.0: 
        print "Invalid probability, must be (0.0, 1.0]"
    
    job_args = []
    for filename in filenames:
        job_args.append((bottom_left, top_right, p, filename))
            
    job_results = parallel_jobs.parallel_jobs(outbox_sampling,job_args,num_parallel_jobs)
    ins.act("end outbox sampling")
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
    ins.instrumento()
    ins.act("start inbox sampling")
    ins.params(bottom_left, top_right, p, filenames)
    if p >= 1.0 or p < 0.0: 
        print "Invalid probability, must be (0.0, 1.0]"
        
    job_args = []
    for filename in filenames:
        job_args.append((bottom_left, top_right, p, filename))
            
    job_results = parallel_jobs.parallel_jobs(inbox_sampling,job_args,num_parallel_jobs)
    ins.act("end inbox sampling")
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
