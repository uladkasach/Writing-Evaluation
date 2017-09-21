###########################################################################
## import dependencies
###########################################################################
if __name__ == '__main__' and __package__ is None or True: ## enables imports of sibling "packages" and "parent"
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    
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
        #if (index > 10): break;  
        docs.append(line.rstrip());
    f.close();
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
    for i in range(4):
        stats["intra_sentence"]["d"+str(i)] = [];
        
    stats["punctuation"] = dict();
    stats["punctuation"]["period"] = [];
    stats["punctuation"]["comma"] = [];
    
    stats["basic"] = dict();
    stats["basic"]["word_length"] = [];
    stats["basic"]["sentence_length"] = [];
    for sentence_list in lists:
        for sentence in sentence_list:
            information = feature_extraction.extract_sentence_information(sentence);
            
            ## intra-sentence word similarity
            for i in range(4):
                stats["intra_sentence"]["d"+str(i)].extend(information["similarities"]["d"+str(i)]["raw"]);
                
            ## across comma similarity
            stats["punctuation"]["comma"].extend(information["across_punctuation_similarities"]["comma"]["raw"]);
            
            ## basic stats
            stats["basic"]["word_length"].extend(information["word_lengths"]["raw"]);
            stats["basic"]["sentence_length"].extend([information["length"]]);
    return stats;
            


    
def plot_statistics_as_histograms(base_title, stats):
    ## intra-sentence word similarity
    plotting.plot_metrics_on_histogram(stats["intra_sentence"], base_title+"-intra_sentence", normalized = True);
    
    
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


