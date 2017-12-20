###########################################################################
## import dependencies
###########################################################################
if __name__ == '__main__' and __package__ is None or True:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__))))) ## enables importing of parent sibling
    sys.path.insert(0,'..') ## enables importing from parent dir
###########################################################################

import plac;
import csv;
import json;

from sklearn.svm import SVR;
import numpy as np;

import utilities.training
Batch_and_Shuffler = utilities.training.Batch_and_Shuffler;




def load_data(source_file):
    ## read all lines
    features = [];
    labels = [];
    header_list = ["essay_id", "essay_set", "score"]
    with open(source_file, "r") as f:
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            #if(i>10000): break;
            these_features = [float(ele) for ele in line[3:]]; ## 3 labels, rest is features
            this_label = [float(line[2])]; ## score
            #print(this_label);
            #print(these_features);
            features.append(these_features);
            labels.append(this_label);
            if(i % 1000 == 0): print("reading line " + str(i))
            #if(i>1000): break;
    return labels, features;

def rmse(predicted, actual):
    ## rmse = root, mean, squered, error
    predicted = np.array(predicted);
    actual = np.array(actual);
    #print(np.column_stack((predicted, actual))[np.random.randint(predicted.shape[0], size=50), :]); ## dirsplay randome 100 rows

    rmse = np.sqrt(((predicted - actual) ** 2).mean());
    return rmse;

@plac.annotations(
    source_file=("Path to source file"),
    n_jobs=("Number of Jobs (Default : 1)", "option", "k", int),
)
def main(source_file, n_jobs):
    ## define defaults
    if(n_jobs is None): n_jobs = 1;

    if(n_jobs != 1): print("WARNING - N_JOBS HAS NO EFFECT YET");
    base_file_name = ".".join(source_file.split("/")[-1].split(".")[:-1]); # retreive file name w/o extension

    ## load data
    print("loading data...");
    labels, features = load_data(source_file);
    data_manager = Batch_and_Shuffler(labels, features);
    data_manager.shuffle_data(); ## shuffle data
    labels, features = data_manager.get_all();
    labels = np.array(labels);
    features = np.array(features);
    total_count = len(labels);

    ## split data naively
    print("splitting data into test and train...");
    train_count = int(total_count*3/float(4));
    train_labels = labels[:train_count];
    test_labels = labels[train_count:];
    train_features = features[:train_count];
    test_features = features[train_count:];

    print("training svm");
    clf = SVR(C=1.0, epsilon=0.2)
    clf.fit(train_features, train_labels);


    print("evaluating model on test data...")
    test_properties = (dict({
        "source_file": source_file,
    }));
    print (json.dumps(test_properties, indent=2))

    ## evaluate model
    predictions = clf.predict(test_features);
    rmse_cost = rmse(predictions, test_labels);
    print("RMSE: " + str(rmse_cost));


if __name__ == '__main__':
    plac.call(main)
