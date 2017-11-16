'''

1. loads sentences from vectors/
2. conduct TSNE on sentences, display sentence score in graph as label
    https://medium.com/@luckylwk/visualising-high-dimensional-datasets-using-pca-and-t-sne-in-python-8ef87e7915b
'''

import csv;
import pandas as pd
import plac;
import datetime;
import numpy as np;
from sklearn.decomposition import PCA
from ggplot import *
import matplotlib.pyplot as plt;
import time
from sklearn.manifold import TSNE




def load_sentences(input_loc):
    ## read all lines
    data_list = [];
    with open(input_loc, "rb") as f:
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            #if(i > 1000): break;
            data_list.append(line);
            if(i % 1000 == 0): print("reading line " + str(i))
    return data_list;


def convert_to_dataframe(sentences, label_cols = ["sentence_id", "essay_id", "essay_set", "score"]):
    ## data["sentence_id"], data["essay_id"], data["essay_set"], data["score"]
    len_of_features = len(sentences[0]) - len(label_cols); ## features = all - labels
    print("length of features " + str(len_of_features));
    feat_cols = [ 'attr_'+str(i) for i in range(len_of_features) ];
    frame_cols = label_cols;
    frame_cols.extend(feat_cols);
    print(frame_cols);
    df = pd.DataFrame(sentences, columns=frame_cols);

    df["coarse_score"] = df['score'].apply(lambda i: str(int(round(float(i)*10)) - 1)); ## converts scores into 1-10 based on the tenth of their %, e.g., 95% -> 10, 93% -> 9, 53% -> 5, then subtracts one
    df["score"] = df['score'].apply(lambda i: (float(i))) ## convert score to float


    print(df.shape);
    print(df);
    return df, feat_cols;

def conduct_histogram_of_scores(df, title):
    scores = df["score"].values;
    weight = np.ones_like(scores) / float(len(scores)); ## normalize, so that all bars add to one and y axis implies percentage
    label = "scores";
    data_list = [scores];
    weights = [weight];
    labels = [label];

    #colors = ['green', '#dbf8ff', 'white'];
    #colors = colors[:len(metrics)];
    this_fig, this_axis = plt.subplots()
    num_bins = 50;
    min_val = 0;
    max_val = 1;
    this_axis.hist(data_list, num_bins, weights=weights, label=labels, range=(min_val, max_val)) #, range=(-0.2, 1)
    this_axis.legend(prop={'size': 10})

    plt.title(title);
    plt.xticks(np.arange(min_val, max_val+0.01, 0.1))
    this_fig.tight_layout();
    #this_fig.show();
    this_fig.savefig("results_analysis/"+title+".png");

def conduct_pca(df, feat_cols, rndperm, title = "pca_plot"):
    pca = PCA(n_components=3)
    pca_result = pca.fit_transform(df[feat_cols].values)

    df['pca-one'] = pca_result[:,0]
    df['pca-two'] = pca_result[:,1]
    df['pca-three'] = pca_result[:,2]

    print 'Explained variation per principal component: {}'.format(pca.explained_variance_ratio_)

    chart = ggplot( df.loc[rndperm[:1000],:], aes(x='pca-one', y='pca-two', color='coarse_score') ) \
            + geom_point(size=75,alpha=0.8) \
            + ggtitle("First and Second Principal Components colored by digit")
    #print(chart)
    ##chart.make();

    chart.save("results_analysis/"+title+".png")

def conduct_tsne(df, feat_cols, rndperm, title = "tsne_plot"):
    n_sne = 7000; ## limit components do display to 7k

    time_start = time.time()
    tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=300)
    tsne_results = tsne.fit_transform(df.loc[rndperm[:n_sne],feat_cols].values)

    print 't-SNE done! Time elapsed: {} seconds'.format(time.time()-time_start)

    df_tsne = df.loc[rndperm[:n_sne],:].copy()
    df_tsne['x-tsne'] = tsne_results[:,0]
    df_tsne['y-tsne'] = tsne_results[:,1]

    chart = ggplot( df_tsne, aes(x='x-tsne', y='y-tsne', color='coarse_score') ) \
            + geom_point(size=70,alpha=0.8) \
            + ggtitle("tSNE dimensions colored by coarse-score")
    print(chart)
    chart.save("results_analysis/"+title+".png")


@plac.annotations(
    source_file=("Path to source file"),
)
def main(source_file):
    base_file_name = ".".join(source_file.split("/")[-1].split(".")[:-1]); # retreive file name w/o extension

    print("loading sentences...");
    sentences = load_sentences(source_file);

    print("convert to dataframe...");
    df, feat_cols = convert_to_dataframe(sentences);
    rndperm = np.random.permutation(df.shape[0]); ## create list of indicies in random order, use df(rndperm[:50]) to get random 50 sentences);
    print(len(rndperm));

    if(True):
        print("draw histogram of scores...");
        conduct_histogram_of_scores(df, "score_histogram-"+base_file_name);

    if(False):
        print("conducting PCA...");
        conduct_pca(df, feat_cols, rndperm, title = "pca_plot-"+base_file_name);

    print("conducting TSNE...");
    conduct_tsne(df, feat_cols, rndperm, title = "tsne_plot-"+base_file_name);

if __name__ == '__main__':
    plac.call(main)
