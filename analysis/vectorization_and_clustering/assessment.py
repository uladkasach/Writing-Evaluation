'''

for each clustering, analyze:
1. the mean and stdev of the score

'''
import csv;
import numpy as np;
import plac;
import json;


import matplotlib.pyplot as plt
from scipy.stats import norm



header_row = ["sentence_id", "essay_id", "essay_set", "score", "cluster"];
def load_results(input_loc):
    ## read all lines
    data_list = [];
    with open(input_loc, "rb") as f:
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            data_list.append(line);
            #if(i > 10): break;
            if(i % 1000 == 0): print("reading line " + str(i))
    return data_list;

def scores_by_cluster(results):
    clusters = dict();
    for result in results:
        this_cluster = result[header_row.index("cluster")];
        if this_cluster not in clusters: clusters[this_cluster] = [];
        clusters[this_cluster].append(float(result[header_row.index("score")]));
    return clusters;

def calculate_statistics_on_clusters(clusters):
    stats = dict();
    #print(clusters);
    for key, val in clusters.iteritems():
        stats[key] = dict({
            "n" : len(val),
            "mean" : np.mean(val),
            "stdev" : np.std(val),
        });
    return stats;


def plot_the_statistics(statistics, base_file_name, normalize = False):
    cluster_count = len(statistics.keys());

    total_n = 0;
    for key, statistic in statistics.iteritems():
        total_n += statistic["n"];
    print(total_n);

    for key, statistic in statistics.iteritems():
        mu = statistic["mean"];
        variance = statistic["stdev"]**2;
        sigma = statistic["stdev"];
        x_axis = np.arange(-0.25, 1.25, 0.001);
        #x = np.linspace(mu-3*variance,mu+3*variance, 100)
        y_axis = norm.pdf(x_axis,mu,sigma);
        scaled_y_axis = y_axis * statistic["n"] / total_n;

        if(normalize):
            plt.plot(x_axis, scaled_y_axis)
        else:
            plt.plot(x_axis, y_axis)

    plt.title("approximate scores from cluster statistics, n = " + str(cluster_count) + " \n"+base_file_name);
    #plt.show()
    return plt;


@plac.annotations(
    source_file=("Path to source file"),
    normalize=("normalize vectors or not (y/N)")
)
def main(source_file, normalize):
    base_file_name = ".".join(source_file.split("/")[-1].split(".")[:-1]); # retreive file name w/o extension

    print("loading results...");
    results = load_results(source_file);

    print("segmenting results by cluster...");
    clusters = scores_by_cluster(results);

    print("assessing statistics...");
    stats = calculate_statistics_on_clusters(clusters);

    with open('results/'+base_file_name+'.txt', 'w+') as outfile:
        json.dump(stats, outfile, sort_keys=True, indent=4)
        print json.dumps(stats, sort_keys=True, indent=4)

    normalize = True if (normalize == "y" or normalize == "Y") else False;
    normalized_name_changer = "_normalized" if (normalize) else "";
    plt = plot_the_statistics(stats, base_file_name, normalize );
    plt.savefig('results/'+base_file_name+normalized_name_changer+'.png');


if __name__ == '__main__':
    plac.call(main)
