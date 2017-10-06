###########################################################################
## import dependencies
###########################################################################
if __name__ == '__main__' and __package__ is None or True: 
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__))))) ## enables importing of parent sibling
    sys.path.insert(0,'..') ## enables importing from parent dir
    
import utilities.plotting as plotting;
import feature_extraction;
import plac;
import spacy;
import numpy as np;
import matplotlib.pyplot as plt;

'''
goal: 
    plot histograms of sentence information for statistical analysis 

requirements:
calc stats:
    - intra-sentence similarity statistics
        - nth order similarities
        - nth order parse tree similarities
    - across punctuation similarity statistics
        - similarity across sentence ends
        - similarity across commas
    - basic features
        - sentence length
        - word length
'''



def get_docs_from_file(source_file, document_delimeter):
    print(source_file);
    ## To Do, handle document_delimeter != newline
    f = open(source_file, 'r');
    docs = [];
    for index, line in enumerate(f.readlines()):
        if (index > 20000 and False): 
            print("DEV LOADING LIMIT REACHED, CONTINUING ON");
            break;  
        docs.append(line.rstrip());
    f.close();
    print("total loaded : " + str(len(docs)));
    return docs;

def convert_docs_to_sentence_lists(docs):
    sentence_lists = [];
    for doc in docs:
        sentence_lists.append(doc.split(".|PUNCT"));
    return sentence_lists;

def calculate_statistics_for_sentence_lists(lists):
    print("calculating statistics");
    stats = dict();
    
    stats["intra_sentence"] = dict();
    for i in range(5):
        stats["intra_sentence"]["d"+str(i)] = [];
        
        
    stats["backscaled_intra_sentence"] = dict();
    for i in range(5):
        stats["backscaled_intra_sentence"]["d"+str(i)] = [];
        
    stats["punctuation"] = dict();
    stats["punctuation"]["period"] = [];
    stats["punctuation"]["comma"] = [];
    
    stats["basic"] = dict();
    stats["basic"]["word_length"] = [];
    stats["basic"]["sentence_length"] = [];
    
    stats["parse_tree"] = dict();
    for key in ["V-N", "N-N", "N-ADJ", "V-ADV"]:
        stats["parse_tree"][key] = [];
    index = -1;
    for sentence_list in lists:
        for sentence in sentence_list:
            index += 1;
            if(index % 1000 ==0): print("at index " + str(index));
            information = feature_extraction.extract_sentence_information(sentence, bool_syntax_tree_data = True);
            
            ## intra-sentence word similarity
            for i in range(5):
                stats["intra_sentence"]["d"+str(i)].extend(information["similarities"]["d"+str(i)]["raw"]);
                
            for i in range(5):
                stats["backscaled_intra_sentence"]["d"+str(i)].extend(information["backscaled_similarities"]["d"+str(i)]["raw"]);
                
            ## across comma similarity
            stats["punctuation"]["comma"].extend(information["across_punctuation_similarities"]["comma"]["raw"]);
            
            ## basic stats
            stats["basic"]["word_length"].extend(information["word_lengths"]["raw"]);
            stats["basic"]["sentence_length"].extend([information["length"]]);
            
            ## syntactic
            for key in ["V-N", "N-N", "N-ADJ", "V-ADV"]:
                data = information["parse_tree"][key]["raw"];
                stats["parse_tree"][key].extend(data);
            
    return stats;
            


    
def plot_statistics_as_histograms(base_title, stats):
    ## intra-sentence word similarity
    #plotting.plot_metrics_on_histogram(stats["intra_sentence"], base_title+"-intra_sentence", normalized = True);
    #plotting.plot_metrics_on_histogram(stats["backscaled_intra_sentence"], base_title+"-backscaled", normalized = True);
    plotting.plot_metrics_on_histogram(stats["parse_tree"], base_title+"-parse_tree", normalized = True);
    
    #plot_metrics_on_histogram(stats["intra-sentence"]);


@plac.annotations(
    source_file=("Path to source file"),
    document_delimeter=("How documents are delimited in input file. Defaults to newline"),
)
def main(source_file, document_delimeter = "newline"):
    base_file_name = ".".join(source_file.split("/")[-1].split(".")[:-1]); # retreive file name w/o extension
    
    print("getting docs from file...");
    docs = get_docs_from_file(source_file, document_delimeter);
    print("converting docs to sentence lists...");
    sent_lists = convert_docs_to_sentence_lists(docs);
    print("calculating stats for sentence lists...");
    stats = calculate_statistics_for_sentence_lists(sent_lists);    
    plot_statistics_as_histograms(base_file_name, stats);
    
    
    
    
    
if __name__ == '__main__':
    plac.call(main)



