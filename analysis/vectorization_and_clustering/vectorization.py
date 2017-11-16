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
import pickle;  # for caching
import plac;


header_list = ["essay_id", "essay_set", "score", "text"];
def load_fragments(input_loc):
    ## read all lines
    data_list = [];
    with open(input_loc, "rb") as f:
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            data_list.append(line);
            #if(i>10): break;
            if(i % 1000 == 0): print("reading line " + str(i))
    return data_list;


KEYS_PRINTED = False;
def vectorize_sentence(sentence, aggregate_types = ["MAX"], include_data=["SIM"]):

    ## ensure choices are valid
    for a_type in aggregate_types:
        assert a_type in ["MAX", "MIN", "MEAN", "STDEV"];
    for a_type in include_data:
        assert a_type in ["SIM", "PUNCT", "LEN", "PARSE"];

    ## determine which parts to compute (speeds up process)
    parse_tree_selected = "PARSE" in include_data;
    chosen_list = dict({
        "basic_similarities":"SIM" in include_data,
        "backscaled_similarities":False,
        "across_punctuation_similarities":"PUNCT" in include_data,
        "parse_tree" : "PARSE" in include_data,
        "semantic" : False,
        "basic" : False,
    });


    ## extract information
    info = feature_extraction.extract_sentence_information(sentence, chosen_list);

    ## build dict of normed data
    data = dict();

    ## append basic data
    if("SIM" in include_data):
        basic_similarities = info["similarities"];
        for sim_type in basic_similarities.keys():
            normed_data = basic_similarities[sim_type]["norm"];
            data[sim_type] = normed_data;

    ## append word length
    if("LEN" in include_data):
        data["length_convinience"] = info["length_convinience"]["norm"];
        data["word_lengths"] = info["word_lengths"]["norm"];

    ## append punctuation
    if("PUNCT" in include_data):
        basic_similarities = info["across_punctuation_similarities"];
        for sim_type in basic_similarities.keys():
            normed_data = basic_similarities[sim_type]["norm"];
            data[sim_type] = normed_data;

    ## append parse_data
    if("PARSE" in include_data):
        parse_data = info["parse_tree"];
        for sim_type in parse_data.keys():
            normed_data = parse_data[sim_type]["norm"];
            data[sim_type] = normed_data;


    ## create vector of data from aggragate_types selected
    global KEYS_PRINTED;
    if(KEYS_PRINTED == False):
        print(sorted(data.keys()));
        KEYS_PRINTED = True;
    vector = [];
    if("MAX" in aggregate_types): vector.extend([data[data_type]["max"] for data_type in sorted(data.keys())])
    if("MIN" in aggregate_types): vector.extend([data[data_type]["min"] for data_type in sorted(data.keys())])
    if("MEAN" in aggregate_types): vector.extend([data[data_type]["mean"] for data_type in sorted(data.keys())])
    if("STDEV" in aggregate_types): vector.extend([data[data_type]["stdev"] for data_type in sorted(data.keys())])


    ## for each value, if it is false, replace it with a 0;
    for index, value in enumerate(vector):
        if(value == False): vector[index] = 0;

    return vector;

## build vector data
def build_vectors(sentences, vectorization_data_types, metrics_to_include):
    vectors = [];
    for index, sentence in enumerate(sentences):
        data_vec = vectorize_sentence(sentence[header_list.index("text")], vectorization_data_types, metrics_to_include);
        new_vector = dict({
            "sentence_id": index,
            "essay_id": sentence[header_list.index("essay_id")],
            "essay_set": sentence[header_list.index("essay_set")],
            "score": sentence[header_list.index("score")],
            "data": data_vec,
        })
        vectors.append(new_vector);
        if(index % 1000 == 0): print("vectorizing at sentence index "  +str(index));
    return vectors;


## output data as csv
def record_vectors(vectors, file_name):
    with open("vectors/"+file_name+".csv", "w+") as file:
        writer = csv.writer(file);
        for i, data in enumerate(vectors):
            vector = [data["sentence_id"], data["essay_id"], data["essay_set"], data["score"]];
            vector.extend(data["data"]);
            if(i % 2000 == 0): print("writing sentence " + str(i));
            writer.writerow(vector);



@plac.annotations(
    source_file=("Path to source file"),
)
def main(source_file):
    base_file_name = ".".join(source_file.split("/")[-1].split(".")[:-1]); # retreive file name w/o extension

    ## define vector options in hardcoded manner
    vectorization_data_types=["MEAN", "STDEV"];
    metrics_to_include=["SIM","PUNCT","LEN", "PARSE"];

    ## load fragments
    fragments = load_fragments("inputs/sentences_of_set_all.csv");

    ## generate vectors for each fragment
    vectors = build_vectors(fragments, vectorization_data_types, metrics_to_include);

    ## save vectors
    file_name = base_file_name + "-" + "_".join(metrics_to_include)+"-"+"_".join(vectorization_data_types);
    record_vectors(vectors, file_name);

if __name__ == '__main__':
    plac.call(main)
