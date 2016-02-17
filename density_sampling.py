import shutil
import numpy
import math
import parallel_jobs
import load_tsv
import random
import sys
import instrumento as ins
import dataOps as dO


def parallel_density_sampling(filenames, outputfilename, feature_order, truth_idx, density_threshold, p, num_bins, num_parallel_jobs=8):
    """
    parallel_density_sampling:
    Using grid based sampling, divide the state space into a grid and pick points probabilistically relative 
    to the number of points in the cell. In more detail the function takes the files passed and processes them.
    First maximum and minimum for each of the features is computed for each file, later the results are combined.
    After this is done the hyper-dimensional space of each file is segmented into cells and then counts of the data
    points falling into each cell are computed. Finally the cells and its counts are merged. In a way this is similar
    to kernel based density estimation where the kernel has no overlap also since this is in high dimensional space
    kernel density estimation is not feasible. 
     
    
     
    filenames : list of data sets to be used
    outputfilename : output filename including path
    feature_order : features to be used
    truth_idx : Index of the data labels in the data set  
    density_threshold : 
    p :
    num_bins :
    num_parallel_jobs : Number of parallel jobs, the default is 8
    """
    
    folderstoDelete,files=dO.createSplitFolder(filenames)
    
    filenames=files
    #Instrumentation code
    log=ins.instrumento()
    log.act("start density sampling")
    log.params(filenames,outputfilename,feature_order,truth_idx,density_threshold,p,num_bins)
    
    #parallel get mins and maxs
    print("Calculating mins and maxs")
    job_args = []
    for filename in filenames:
        print("working on file %s"%(filename))
        features, truth = load_tsv.load_tsv_features_truth(filename, feature_order, truth_idx)
        if p < 0 or p > 1: 
            print "Invalid starting probability"
            sys.stdout.flush()
        job_args.append((features))
        
    #This section of the code extracts minimums and maximums over the features on 
    #small pieces of data
    job_results = parallel_jobs.parallel_jobs(compute_state_space,job_args,num_parallel_jobs)
    
    #merge mins and maxs of each feature and compute the stepsize
    minimum = numpy.zeros(len(job_results[0][0]))
    maximum = numpy.zeros(len(job_results[0][1]))
    for i in range(len(minimum)):
        minimum[i] = job_results[0][0][i]
        maximum[i] = job_results[0][1][i]
        
    print "printing mins"
    sys.stdout.flush()
    for result in job_results:
        for i in range(len(minimum)):
            if result[0][i] < minimum[i]:
                minimum[i] = result[0][i]
            if result[1][i] > maximum[i]:
                maximum[i] = result[1][i]
    step_size = (maximum-minimum)/num_bins
    
    #put the samples in the grids and collect all the grids
    print("starting sampling")
    job_args = []
    for filename in filenames:
        features, truth = load_tsv.load_tsv_features_truth(filename, feature_order, truth_idx)
        job_args.append((features, minimum, maximum, step_size, num_bins, filename))
        #grid_sampling((features, minimum, maximum, step_size, num_bins, filename))
    job_results2 = parallel_jobs.parallel_jobs(grid_sampling,job_args,num_parallel_jobs)
    
    print "merging output"
    sys.stdout.flush()
    #merge the grids, sample, and print the results
    #outputfile = open(outputfilename,"w")
    grid = job_results2[0][0]
    text_lines = job_results2[0][1]
    for i in range(1,len(job_results2)):
        for key in job_results2[i][0].keys():
            if grid.get(key) == None:
                grid[key] = job_results2[i][0][key]
                text_lines[key] = job_results2[i][1][key]
            else: #must merge two counts and two lists 
                grid[key] = grid[key] + job_results2[i][0][key]
                text_lines[key] = text_lines[key]+job_results2[i][1][key]
    
    print "sampling"
    sys.stdout.flush()
    #randomly sample proportional to the set in the grid cell
    count = 0
    outputfile = open(outputfilename,"w")
    for key in grid.keys():
        if grid[key] >= density_threshold:
            for line in text_lines[key]:
                if random.random() < p:
                    count = count+1
                    outputfile.write(line)
                    outputfile.flush()
                    
    print "completed output"
    sys.stdout.flush()
    outputfile.close()
    
    for i in folderstoDelete:
        shutil.rmtree(i)
    
    log.act("end parallel density sampling")
    return [outputfilename, count]

def compute_state_space(in_args):
    """
    compute_state_space:
    This function calculates the maximum and minimum for each feature in the data passed on 
    in_args.
    """
    
    features = in_args
    
    minimum = numpy.zeros(len(features[0]))
    maximum = numpy.zeros(len(features[0]))
    
    for i in range(len(features[0])):
        minimum[i] = features[0][i]
        maximum[i] = features[0][i]
    
    for observation in features:
        for feature in range(len(observation)):
            if observation[feature] < minimum[feature]:
                minimum[feature] = observation[feature]
            if observation[feature] > maximum[feature]:
                maximum[feature] = observation[feature]
    
    return [minimum,maximum]
    

def grid_sampling(in_args):
    features, minimum, maximum, step_size, num_bins, filename = in_args
    print("working on file %s"%(filename))
    inputfile = open(filename, "r")
    
    grid = {}
    text_lines = {}
    print "printing grid samples"
    sys.stdout.flush()
    for observation in features:
        line = inputfile.readline()
        grid_idx = numpy.zeros(len(observation))
        for i in range(len(observation)):
            grid_idx[i] = math.floor((observation[i]-minimum[i])/step_size[i])
        grid_idx = tuple(grid_idx)
        if grid_idx not in grid.keys():
            grid[grid_idx] = 1
            text_lines[grid_idx] = [line]
        else:
            grid[grid_idx] = grid[grid_idx] +1
            text_lines[grid_idx].append(line)
            
    
    inputfile.close()
        
    return [grid, text_lines]


if __name__=="__main__":
    print("Testing density sampling")
    import load_tsv
    import numpy
    from sklearn.svm import SVC
    import density_sampling
    path="/home/julian/data/"
    ins=ins.instrumento(path=path,logname="log.txt")
#     features, truth = load_tsv.load_tsv_features_truth("/Users/ingenia/git/data/data_sampling/user_bot_data.tsv",[0,1,2],3)
    originalFile=["/home/julian/data/user_bot_data.tsv"]
    
#     files=["user_bot_part00","user_bot_part01","user_bot_part02","user_bot_part03","user_bot_part04","user_bot_part05","user_bot_part06","user_bot_part07"]
#     files=[ path+i for i in files]

    vals = density_sampling.parallel_density_sampling(originalFile, "/home/julian/data/user_bot_data_density_sample.tsv", range(2,29,1), 1, 0, 0.025, 5, 8)
    print vals