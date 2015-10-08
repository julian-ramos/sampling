
import parallel_jobs
import load_tsv
import random
import math
import numpy
import heapq
import sklearn.linear_model
import instrumento as ins

def parallel_reg_uncertainty_sampling(model, filenames,feature_order, truth_idx, p, 
                                      number_parallel_jobs=8):
    ins.instrumento()
    ins.act("start uncertainty sampling")
    ins.params(model, filenames,feature_order, truth_idx, p)
    
    if p > 1.0 or p < 0.0:
        print "Invalid probability, must be (0.0,1.0)"
        
    job_args = []
    for filename in filenames: 
        features, truth = load_tsv.load_tsv_features_truth(filename, 
                                                           feature_order, 
                                                           truth_idx)
        job_args.append((model, features, truth, int(p*len(features)), filename))

    job_results = parallel_jobs.parallel_jobs(reg_uncertainty_sampling, 
                                              job_args, number_parallel_jobs)
    
    ins.act("end uncertainty sampling")
    return job_results

# the model must have a score function that outputs the R^2 value up to 1.0 
# with score values, bigger is better
# the model must be already trained
# threshold is the value <= 1.0 that we start sampling from the score under
# p is the probability of choosing a sample that meets the threshold requirement
# for example, all of the worst points might be threshold = 0.2, p = 1.0
def reg_uncertainty_sampling(in_args):
    model, features, truth, N, filename = in_args
    
    count = 0
    random.seed(None)
    outputfilename = filename+"-regunc-"+str(N)
    inputfile = open(filename,"r")
    outputfile = open(outputfilename,"w")
    
    predict = model.predict(features)
    residuals = numpy.fabs(numpy.subtract(truth,predict))
    
    indexes = numpy.argsort(residuals)
    sample_idxs = indexes[-N:]
    count = 0

    #this reads in the inputfile again so that the 
    # sampled data can be written out in the same format
    for line in inputfile:
        if count in sample_idxs:
            outputfile.write(line)
        count = count + 1

    outputfile.close()
    inputfile.close()
    return [outputfilename, numpy.sort(residuals)[-N:], sample_idxs, N]


# p here is the proportion of data from each file to sample
def parallel_maxent_uncertainty_sampling(model, filenames, 
                                         feature_order, truth_idx, 
                                         p, number_parallel_jobs=8):
    
    ins.instrumento()
    ins.act("start maxent_uncertainty sampling")
    ins.params(model, filenames,feature_order, truth_idx, p)
    if p > 1.0 or p < 0.0:
        print "Invalid probability, must be (0.0,1.0)"
        
    job_args = []
    for filename in filenames: 
        features, truth = load_tsv.load_tsv_features_truth(filename, 
                                                           feature_order, 
                                                           truth_idx)
        job_args.append((model, features, int(p*len(features)),filename))

    job_results = parallel_jobs.parallel_jobs(class_maxentunc_sampling, 
                                              job_args, number_parallel_jobs)
    ins.act("end maxent_uncertainty sampling")
    return job_results
        
# maximum entropy uncertainty sampling for classification algorithms
# requires that the model passed in has a predict_proba function
# returns the N highest entropy samples between the classes y 
# where entropy = - sum_y p(y)log_2p(y)
def class_maxentunc_sampling(in_args):
    model, features, N, filename = in_args
    
    count = 0
    outputfilename = filename+"-maxentunc-"+str(N)
    inputfile = open(filename,"r")
    outputfile = open(outputfilename,"w")

    #compute the predict_proba for the features 
    probabilities = model.predict_proba(features)

    #first we're going to compute the entropies 
    # and put them in a heap to sort
    heap = []
    count = 0
    for probs in probabilities:
        entropy = 0
        for prob in probs:
            entropy = entropy - (prob*math.log(prob,2))
        heapq.heappush(heap,(count,entropy))
        count = count + 1
        
    #get out the top N sorted by entropy (item 1)
    largest = heapq.nlargest(N, heap, key=lambda item: item[1])
    indexes = [item[0] for item in largest]
    samples = numpy.array([features[i] for i in indexes])
        
    #now we can go back through the file and write out 
    # the sampled lines we care about
    count = 0
    for line in inputfile:
        if count in indexes:
            outputfile.write(line)
        count = count + 1

    inputfile.close()
    outputfile.close()

    return [outputfilename, samples, indexes, N]

# p here is the proportion of data from each file to sample
def parallel_smallmargin_uncertainty_sampling(model, filenames, 
                                              feature_order, truth_idx, 
                                              p, number_parallel_jobs=8):
    
    ins.instrumento()
    ins.act("start small_margin_uncertainty sampling")
    ins.params(model, filenames,feature_order, truth_idx, p)
    if p > 1.0 or p < 0.0:
        print "Invalid probability, must be (0.0,1.0)"
        
    job_args = []
    for filename in filenames: 
        features, truth = load_tsv.load_tsv_features_truth(filename, 
                                                           feature_order, 
                                                           truth_idx)
        job_args.append((model, features, int(p*len(features)),filename))

    job_results = parallel_jobs.parallel_jobs(class_smallmarginunc_sampling, 
                                              job_args, number_parallel_jobs)
    ins.act("end small_margin_uncertainty sampling")
    return job_results


# smallest margin uncertainty sampling for classification algorithms
# requires that the model passed in has a predict_proba function
# returns the N samples with smallest margin between top 2 classes y1 and y2 
def class_smallmarginunc_sampling(in_args):
    model, features, N, filename = in_args
    
    count = 0
    outputfilename = filename+"-smallmarginunc-"+str(N)
    inputfile = open(filename,"r")
    outputfile = open(outputfilename,"w")
    
    #compute the predict_proba for the features 
    probabilities = model.predict_proba(features)
    
    #first we're going to compute the entropies 
    # and put them in a heap to sort
    heap = []
    count = 0
    for probs in probabilities:
        probs.sort()
        heapq.heappush(heap,(count,probs[len(probs)-1]-probs[len(probs)-2]))
        count = count + 1

    #get out the top N sorted by entropy (item 1)
    smallest = heapq.nsmallest(N, heap, key=lambda item: item[1])
    indexes = [item[0] for item in smallest]
    samples = numpy.array([features[i] for i in indexes])
    
    #now we can go back through the file and write out 
    # the sampled lines we care about
    count = 0
    for line in inputfile:
        if count in indexes:
            outputfile.write(line)
        count = count + 1
        
    inputfile.close()
    outputfile.close()

    return [outputfilename, samples, indexes, N]


#features, truth = load_tsv.load_tsv_features_truth("data/part1.tsv", [0,1,2], 3)
#linreg = linear_model.LinearRegression()
#linreg.fit(features,truth)
#vals = parallel_reg_uncertainty_sampling(linreg, 
#                                         ["data/part1.tsv","data/part2.tsv"], 
#                                      [0,1,2], 3, 
#                                      1.0, 1.0, 
#                                      number_parallel_jobs=8)
    
