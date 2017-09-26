'''

1. loads sentences from vectors/
2. clusters sentences based on the feature data: vector[4:] 
3. outputs [...label_data (vector[:4])..., cluster] for analysis into clusters

'''

import csv;
from sklearn.cluster import KMeans;
import plac;
import datetime;


def load_sentences(input_loc):
    ## read all lines
    data_list = [];
    with open(input_loc, "rb") as f:
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            data_list.append(line);
            if(i % 1000 == 0): print("reading line " + str(i))
    return data_list;


def reduce_to_feature_data(sentences):
    feature_data = [];
    for sentence in sentences:
        feature_data.append(sentence[4:]);
    return feature_data;
        
def record_results(sentences, clusters, output_title):
    results = [];
    for index in range(len(sentences)):
        result = sentences[index][:4];
        result.append(clusters[index]);
        results.append(result);

    ## output data as csv
    with open("clusters/"+output_title+".csv", "w+") as file:
        writer = csv.writer(file);
        for i, data in enumerate(results):
            if(i % 200 == 0): print("writing sentence " + str(i));
            writer.writerow(data); 


        
        
        
@plac.annotations(
    source_file=("Path to source file"),
    n_clusters=("Number of clusters")
)
def main(source_file, n_clusters):
    n_clusters = int(n_clusters);
    base_file_name = ".".join(source_file.split("/")[-1].split(".")[:-1]); # retreive file name w/o extension
    
    print("loading sentences...");
    sentences = load_sentences(source_file);
    
    print("reducing to features...");
    features = reduce_to_feature_data(sentences);
    
    print("clustering...");
    clusters = KMeans(n_clusters=n_clusters).fit_predict(features);
    
    print("saving results...");
    record_results(sentences, clusters, base_file_name + "_n"+str(n_clusters)+"_"+str(datetime.datetime.now().strftime("%Y.%m.%d.%H.%M"))); ## note, timestamp included in file name so that we can have multiple results for the same n_clusters and the same file. kmeans results vary each time.
    
    
    
    
    
if __name__ == '__main__':
    plac.call(main)



