import csv
import numpy

# if i is index in new feature vector,
# feature_order[i] is the index into the file's original features
def load_tsv_features_truth(filename, feature_order, truth_idx):
    features = []
    truth = []

    input_file = open(filename, 'r')
    input_reader = csv.reader(input_file, delimiter="\t")

    for row in input_reader:
        feature_row = []
        
        if feature_order==[]:
            feature_order=range(len(row))
        for i in range(len(feature_order)):
            feature_row.append(float(row[feature_order[i]]))
        features.append(numpy.array(feature_row))
        truth.append(float(row[truth_idx]))

    input_file.close()

    return numpy.array(features), numpy.array(truth)