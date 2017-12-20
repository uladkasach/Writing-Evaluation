'''
convert each sentence w/ score into [label, :features:] and save as csv in /vectorizations


from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(twenty_train.data)
X_train_counts.shape
'''
import plac;
import numpy as np;
import pandas as pd;
import csv;

from sklearn.feature_extraction.text import CountVectorizer;
from sklearn.feature_extraction.text import TfidfTransformer;

def load_fragments(input_loc, dev_limit = -1):
    ## read all lines
    data_list = [];
    header_list = ["essay_id", "essay_set", "score", "text"];
    with open(input_loc, "rb") as f:
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            data_list.append(line);
            #if(i>10000): break;
            if(i % 1000 == 0): print("reading line " + str(i))
    dataframe = pd.DataFrame(data=data_list, index=None, columns=header_list)
    return dataframe;


def record_vectors(dataframe, vectors, file_name):
    with open("vectors/lsa_"+file_name+".csv", "w+") as file:
        writer = csv.writer(file);
        for index, row in dataframe.iterrows():
            vector = [index, row["essay_id"], row["essay_set"], row["score"]];
            vector.extend(vectors[index]);
            if(index % 2000 == 0): print("writing sentence " + str(index));
            writer.writerow(vector);


@plac.annotations(
    source_file=("Path to source file"),
    lsa_size=("Size to reduce LSA vectors to", 'option', "l", int, None, "INT"),
)
def main(source_file, lsa_size):
    base_file_name = ".".join(source_file.split("/")[-1].split(".")[:-1]); # retreive file name w/o extension
    if(lsa_size is None):
        print("For now, we must conduct LSA as we have not defined an efficient way to method to record a 13k by 38k matrix")
        exit();
         
    ## load fragments
    print("loading fragments...");
    dataset = load_fragments(source_file);
    print(dataset);

    ## gen bag of words
    bag_of_words = CountVectorizer().fit_transform(dataset["text"])
    print(bag_of_words.shape);

    ## convert to TF-IDF
    tf_idf = TfidfTransformer().fit_transform(bag_of_words)
    print(tf_idf.shape);

    ## reduce dimensionality with lsa if requested
    if(lsa_size is not None):
        #################################################################
        ## Reduce Dimensionality of word vectors w/ truncated SVD
        ##      SVD is utilized instead of PCA to deal w/ sparce matrix
        ##      This process is called LSA
        #################################################################
        #https://roshansanthosh.wordpress.com/2016/02/18/evaluating-term-and-document-similarity-using-latent-semantic-analysis/
        print("Reducing dimensionality w/ LSA...");
        from sklearn.decomposition import TruncatedSVD
        svd = TruncatedSVD(n_components = lsa_size)
        lsa = svd.fit_transform(tf_idf)

        print(lsa[0:5]);
        print(lsa.shape);
        #exit();

    ## save vectors
    file_name = base_file_name + "_l" +str(lsa_size);
    record_vectors(dataset, lsa, file_name);

if __name__ == '__main__':
    plac.call(main)
