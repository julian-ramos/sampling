
import numpy
import parallel_jobs
import load_tsv
import random

#p is the probability of choosing a sample that classified differenty by >= 2 classifiers
def parallel_query_sampling(model_list, filenames, feature_order, truth_idx, p, num_parallel_jobs=8):
    if p >= 1.0 or p < 0.0: 
        print "Invalid probability, must be (0.0, 1.0]"
        
    job_args = []
    for filename in filenames:
        features, truth = load_tsv.load_tsv_features_truth(filename, feature_order, truth_idx)
        job_args.append((model_list, features, truth, int(p*len(features)), filename))
            
    job_results = parallel_jobs.parallel_jobs(query_sampling,job_args,num_parallel_jobs)
    return job_results

def query_sampling(in_args):
    model_list, features, truth, N, filename = in_args
        
    outputfilename = filename+"-query-"+str(N)
    inputfile = open(filename, "r")
    outputfile = open(outputfilename,"w")
        
    different_count = numpy.zeros(len(features))
    for model in model_list:
        predict = model.predict(features)
        same = numpy.equal(predict,truth) #i think this could be made faster
        for i in range(len(same)):
            if same[i]:
                different_count[i] = different_count[i] + 1
        
    indexes = numpy.argsort(different_count)
    sample_idxs = indexes[-N:] #could grab only enough that there must be conflict, the grabs constant number
    
    count = 0
    for line in inputfile:
        if count in sample_idxs:
            outputfile.write(line)
        count = count + 1
    
    outputfile.close()
    inputfile.close()
        
    return [outputfilename, count]
