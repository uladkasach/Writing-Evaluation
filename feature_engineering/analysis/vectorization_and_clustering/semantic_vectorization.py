'''
convert each sentence w/ score into [label, :features:] and save as csv in /vectorizations

vectorization type may vary:
1. basic intra-sentence similarities
'''

###########################################################################
## import dependencies
###########################################################################
if __name__ == '__main__' and __package__ is None or True:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__))))) ## enables importing of parent sibling
    sys.path.insert(0,'..') ## enables importing from parent dir
###########################################################################
import feature_extraction;
import csv;

embeddings_choice="sense2vec"; ## or sense2vec
header_list = ["essay_id", "essay_set", "score", "text"];
def load_sentences(input_loc):
    ## read all lines
    data_list = [];
    with open(input_loc, "rb") as f:
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            data_list.append(line);
            #if(i>10000): break;
            if(i % 1000 == 0): print("reading line " + str(i))
    return data_list;


def vectorize_sentence(sentence):
    ## extract information
    info = feature_extraction.extract_sentence_information(sentence, chosen_list=["semantic"], embeddings_choice=embeddings_choice);
    vector = info["semantic"]["average"];

    if(vector == False): return False;
    return vector;



## build vector data
input_mod = "essay_set_all";
sentences = load_sentences("inputs/"+input_mod+".csv");
vectors = [];
for index, sentence in enumerate(sentences):
    data_vec = vectorize_sentence(sentence[header_list.index("text")]);
    if(data_vec == False): continue;
    new_vector = dict({
        "sentence_id": index,
        "essay_id": sentence[header_list.index("essay_id")],
        "essay_set": sentence[header_list.index("essay_set")],
        "score": sentence[header_list.index("score")],
        "data": data_vec,
    })
    vectors.append(new_vector);
    if(index % 1000 == 0): print("vectorizing at sentence index "  +str(index));

## output data as csv
with open("vectors/"+input_mod+"-average-"+embeddings_choice+".csv", "w+") as file:
    writer = csv.writer(file);
    for i, data in enumerate(vectors):
        vector = [data["sentence_id"], data["essay_id"], data["essay_set"], data["score"]];
        vector.extend(data["data"]);
        if(i % 2000 == 0): print("writing sentence " + str(i));
        writer.writerow(vector);
