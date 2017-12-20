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
            # header line - ['sent_id', 'essay_id', 'essay_set', 'score', ...features...]
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



def load_cluster_centroids(input_loc):
    centroids = [];
    with open(input_loc, "rb") as f:
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            this_centroid = np.array(line).astype(float);
            centroids.append(this_centroid);
            if(i % 1000 == 0): print("reading cluster line " + str(i))
    print("Total centroids found : " + str(len(centroids)));
    return centroids;

def load_clusters_mapped_by_sentence_id(input_loc, dev_limit = -1):
    clusters_mapped_by_sentence_id = dict();
    max_cluster_number = 0;
    with open(input_loc, "rb") as f:
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            #if(i > 1000): break;
            # header line - ['sent_id', 'essay_id', 'essay_set', 'score', 'cluster']
            sentence_id = line[0];
            cluster_id = line[4];
            clusters_mapped_by_sentence_id[sentence_id] = int(cluster_id);
            if(int(cluster_id) > max_cluster_number):
                max_cluster_number = int(cluster_id);
            if(i % 1000 == 0): print("reading cluster line " + str(i))
            if(i == dev_limit): break;
    cluster_count = max_cluster_number + 1;
    print("Total clusters found : " + str(cluster_count));
    return clusters_mapped_by_sentence_id, cluster_count;

def generate_vectors_with_k_sparce(sentences, clusters_mapped_by_sentence_id, cluster_count):
    # purpose: generate vector for each essay by counting how many times each essay's constituent sentences appeared in each cluster ("bag of clusters")
    # method : create vector for each essay on the fly in a dict and add up each time a sentence cluster is seen
    # return : [dict(essay_id, score, features)...]

    aggregation_dict = dict();
    for sentence in sentences:
        essay_id = sentence["essay_id"]
        if(essay_id not in aggregation_dict):
            aggregation_dict[essay_id] = dict({
                "essay_id" : essay_id,
                "essay_set" : sentence["essay_set"],
                "score" : sentence["score"],
                "features" : np.zeros(cluster_count),
            })
        cluster_number = clusters_mapped_by_sentence_id[sentence["sentence_id"]];
        aggregation_dict[essay_id]["features"][cluster_number] += 1; ## increment count of that cluster number

    ## build list of essays
    essays = [];
    for key, essay in aggregation_dict.iteritems():
        essays.append(essay);

    #print(essays);
    return essays;


def generate_vectors_with_k_dense(sentences, centroids):
    # purpose: generate vector for each essay by calculating distance between each compositional sentence and each centroid and taking the average distance of all sentences
    # method : create dict to store essay sentences w/ a vector created for each sentence w/ L2 norm distance to each centroid from sentence vector
    # return : [dict(essay_id, score, features)...]
    ## aggregate features for each essay
    aggregation_dict = dict();
    for index, sentence in enumerate(sentences):
        essay_id = sentence["essay_id"]
        if(essay_id not in aggregation_dict):
            aggregation_dict[essay_id] = dict({
                "essay_id" : essay_id,
                "essay_set" : sentence["essay_set"],
                "score" : sentence["score"],
                "features" : [],
            })
        if(index % 1000 == 0): print("writing essay " + str(index));
        l2_distance_for_each_centroid = np.sqrt(((centroids - np.array(sentence["features"]).astype(float))**2).mean(axis=1))
        aggregation_dict[essay_id]["features"].append(l2_distance_for_each_centroid);

    ## build list of essays
    essays = [];
    for key, essay in aggregation_dict.iteritems():
        features = np.array(essay["features"]).astype(np.float);
        average_features = np.mean(features, axis=0);
        essay["features"] = average_features; # replace list of features w/ average features
        essays.append(essay);

    #print(essays);
    return essays;

def generate_vectors_with_mean(sentences):
    # purpose: generate vector for each essay by method of averaging sentences
    # method : store sentences for each essay in a dict, after all senteces parsed - average the vectors
    # return : [dict(essay_id, score, features)...]

    ## aggregate features for each essay
    aggregation_dict = dict();
    for index, sentence in enumerate(sentences):
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
    with open("essay_vectors/essay_"+base_file_name+".csv", "w+") as file:
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
    cluster_centroids_source_file=("Cluster Source File", 'option', "k", str, None, "<REL_PATH>"),
)
def main(method, sentence_source_file, cluster_source_file, cluster_centroids_source_file):
    base_file_name = ".".join(sentence_source_file.split("/")[-1].split(".")[:-1]); # retreive file name w/o extension

    print("loading sentences...");
    sentences = load_sentences(sentence_source_file, dev_limit = -1);
    if(cluster_source_file is not None):
        clusters_mapped_by_sentence_id, cluster_count = load_clusters_mapped_by_sentence_id(cluster_source_file);

    if(cluster_centroids_source_file is not None):
        centroids = load_cluster_centroids(cluster_centroids_source_file);

    if(method == "mean"):
        essay_vectors = generate_vectors_with_mean(sentences);
    elif(method == "k-sparce"):
        assert(cluster_source_file is not None);
        essay_vectors = generate_vectors_with_k_sparce(sentences, clusters_mapped_by_sentence_id, cluster_count);
    elif(method == "k-dense"):
        assert(cluster_centroids_source_file is not None);
        essay_vectors = generate_vectors_with_k_dense(sentences, centroids);
    record_essay_vectors(essay_vectors, base_file_name + "_" + method);






if __name__ == '__main__':
    plac.call(main)
