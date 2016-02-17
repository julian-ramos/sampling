import dataOps as dO
import numpy 
import parallel_jobs
import load_tsv
import random
import instrumento as ins
import stringUtils as sU
import shutil
#p is the probability of choosing a sample that classified differenty by >= 2 classifiers
def parallel_query_sampling(model_list, filenames, feature_order, truth_idx, p, num_parallel_jobs=8):
    log=ins.instrumento()
    log.act("start QBC sampling")
    log.params(model_list, filenames, feature_order, truth_idx, p)
    if p >= 1.0 or p < 0.0: 
        print "Invalid probability, must be (0.0, 1.0]"
        
    job_args = []
    
    folderstoDetele,filenames=dO.createSplitFolder(filenames)
    
    
    for filename in filenames:
        features, truth = load_tsv.load_tsv_features_truth(filename, feature_order, truth_idx)
        job_args.append((model_list, features, truth, int(p*len(features)), filename))
            
    job_results = parallel_jobs.parallel_jobs(query_sampling,job_args,num_parallel_jobs)
    
    for i in folderstoDetele:
        shutil.rmtree(i)
#         print("to delete %s"%(i))
    
    log.act("end QBC sampling")
    return job_results

def query_sampling(in_args):
    
    model_list, features, truth, N, filename = in_args
        
    outputfilename = sU.extractPath(filename)+"/"+sU.extractFilename(filename)+"-query-"+str(N)+".tsv"
    inputfile = open(filename, "r")
    outputfile = open(outputfilename,"w")
        
    different_count = numpy.zeros(len(features))
    for model in model_list:
        predict = model.predict(features)
        
        
#         same = numpy.equal(predict,truth) #i think this could be made faster
#         for i in range(len(same)):
#             if same[i]:
#                 different_count[i] = different_count[i] + 1

        #Here is an slightly faster version, ran tests and the outputs are identical
        same = numpy.where(predict==truth)
        different_count[same]+=1
                                
        numpy.argsort
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


if __name__=="__main__":
    import load_tsv
    import numpy
    from sklearn.svm import SVC
    from sklearn.linear_model import LogisticRegression
    from sklearn.naive_bayes import GaussianNB
    from sklearn.externals import joblib

    import query_by_committee_sampling
    
    print("Testing query by committee")
    
    filename="/Users/ingenia/Google Drive/Research collaborations/big data mining/data-validation/datasets/user_bot_data.tsv"
    sampleFilename="/Users/ingenia/git/data/data_sampling/previous_data/part1.tsv"
    
    features, truth = load_tsv.load_tsv_features_truth(filename,range(2,29),1)
    
    inds=numpy.argwhere(truth==1)
    
    botsInds=numpy.random.choice(inds.flatten(),50)
    trainInds=numpy.random.choice(range(features.shape[0]),4950)
    inter=numpy.intersect1d(trainInds, botsInds, assume_unique=True)
    
    trainInds=numpy.setdiff1d(trainInds,botsInds)
    trainInds=numpy.r_[trainInds,botsInds]
    trainData=features[trainInds,:]
    trainLabels=truth[trainInds]
    
    
    # Create, fit, predict with the SVM Classifier
    
    
    svm = SVC(C=1, kernel="linear", probability=True, max_iter=50000)
    svm.fit(trainData, trainLabels)
    
    lr =LogisticRegression()
    lr.fit(trainData,trainLabels)
    
    nb = GaussianNB()
    nb.fit(trainData,trainLabels)
    
    joblib.dump(svm, 'svm.pkl') 
    joblib.dump(nb, 'rb.pkl')
    joblib.dump(lr, 'lr.pkl')
    
    
    
    #vals = query_by_committee_sampling.query_sampling(([svm], features, truth, 0.1, "data/part1.tsv"))
    #features, truth = load_tsv.load_tsv_features_truth("data/part1.tsv", [0,1,2], 3)
#     vals = query_by_committee_sampling.parallel_query_sampling([svm],["/Users/ingenia/git/data/data_sampling/previous_data/part1.tsv"]  ,[0,1,2],3,0.1,1)
    
     

