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


header_list = ["essay_id", "essay_set", "score", "text"];
def load_sentences(input_loc):
    ## read all lines
    data_list = [];
    with open(input_loc, "rb") as f:
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            data_list.append(line);
            #if(i>10): break;
            if(i % 1000 == 0): print("reading line " + str(i))
    return data_list;



def vectorize_sentence(sentence, aggregate_types = ["MAX"]):
    print(sentence);
    
    ## ensure type is valid
    for a_type in aggregate_types:
        assert a_type in ["MAX", "MIN", "AVG", "STD"];
        
    ## extract information
    info = feature_extraction.extract_sentence_information(sentence);
    
    ## build dict of normed data
    data = dict();
    
    ## append basic data
    basic_similarities = info["similarities"];
    for sim_type in basic_similarities.keys():
        normed_data = basic_similarities[sim_type]["norm"];
        data[sim_type] = normed_data;
        
    ## create vector of data from aggragate_types selected
    print(sorted(data.keys()));
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
sentences = load_sentences("inputs/sentences_of_set_all.csv");
vectors = [];
for index, sentence in enumerate(sentences):
    data_vec = vectorize_sentence(sentence[header_list.index("text")]);
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
with open("vectors/vectors_of_set_all.csv", "w+") as file:
    writer = csv.writer(file);
    for i, data in enumerate(vectors):
        vector = [data["sentence_id"], data["essay_id"], data["essay_set"], data["score"]];
        vector.extend(data["data"]);
        if(i % 200 == 0): print("writing sentence " + str(i));
        writer.writerow(vector); 
    
