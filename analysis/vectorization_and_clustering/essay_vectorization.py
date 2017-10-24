'''
    This file deals with taking constituent sentence vectors and building a single feature vector based on the sentence vectors.

    This can be done in multiple ways:
        1. average all the sentence vectors
        2. build bag of words from k-means cluster assignments of each sentence (e.g., 400 clusters -> 400 features) - very sparce
        3. build vector based on sum or average distance between each sentence and each cluster (like number two, except accounts for features being close to multiple clusters)

'''
import plac;
import csv;
import numpy as np;
import plac;
import json;
import pickle;


#["sentence_id", "essay_id", "essay_set", "score", "cluster"];
def load_sentences(input_loc, dev_limit = -1, cache_path='.cache/essay_vectorization_sentences.pk'):
    #if load_from_pickle:
        ## load from pickle
    #    with open(cache_path, 'rb') as handle:
    #        return pickle.load(handle);

    ## read all lines
    data_list = [];
    with open(input_loc, "rb") as f:
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            #if(i > 1000): break;
            # header line - ['sent_id', 'essay_id', 'score', ...features...]
            this_sent = dict({
                "sentence_id" : line[0],
                "essay_id": line[1],
                "essay_set": line[2],
                "score"   : line[3],
                "features": line[4:],
            })
            data_list.append(this_sent)
            if(i % 1000 == 0): print("reading line " + str(i))
            if(i == dev_limit): break;

    #with open(cache_path, 'wb+') as handle:
    #    pickle.dump(data_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return data_list;

def generate_vectors_with_mean(sentences):
    # purpose: generate vector for each essay by method of averaging sentences
    # method : store sentences for each essay in a dict, after all senteces parsed - average the vectors
    # return : [dict(essay_id, score, features)...]

    ## aggregate features for each essay
    aggregation_dict = dict();
    for sentence in sentences:
        essay_id = sentence["essay_id"]
        if(essay_id not in aggregation_dict):
            aggregation_dict[essay_id] = dict({
                "essay_id" : essay_id,
                "essay_set" : sentence["essay_set"],
                "score" : sentence["score"],
                "features" : [],
            })
        aggregation_dict[essay_id]["features"].append(sentence["features"]);


    ## build list of essays
    essays = [];
    for key, essay in aggregation_dict.iteritems():
        features = np.array(essay["features"]).astype(np.float);
        average_features = np.mean(features, axis=0);
        essay["features"] = average_features; # replace list of features w/ average features
        essays.append(essay);

    #print(essays);
    return essays;

def record_essay_vectors(essays, base_file_name):
    ## output data as csv
    with open("essay_vectors/"+base_file_name+".csv", "w+") as file:
        writer = csv.writer(file);
        for i, data in enumerate(essays):
            vector = [data["essay_id"], data["essay_set"], data["score"]];
            vector.extend(data["features"]);
            if(i % 2000 == 0): print("writing essay " + str(i));
            writer.writerow(vector);

@plac.annotations(
    method=("Vectorization Method", 'positional', None, str, ['mean', 'k-sparce','k-dense']), # (1), (2), (3) from beginning of this file
    sentence_source_file=("Sentence Vector Source File", 'option', "s", str, None, "<REL_PATH>"),
    cluster_source_file=("Cluster Source File", 'option', "c", str, None, "<REL_PATH>"),
)
def main(method, sentence_source_file, cluster_source_file):
    base_file_name = ".".join(sentence_source_file.split("/")[-1].split(".")[:-1]); # retreive file name w/o extension


    print("loading sentences...");
    sentences = load_sentences(sentence_source_file, dev_limit = -1);
    if(method == "mean"):
        essay_vectors = generate_vectors_with_mean(sentences);

    record_essay_vectors(essay_vectors, base_file_name);






if __name__ == '__main__':
    plac.call(main)
