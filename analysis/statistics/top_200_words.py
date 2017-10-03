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
import numpy as np;
import matplotlib.pyplot as plt;
import collections; 
import pickle

'''
goal, 
    plot similarities for words surrounding top 200 words 
'''




def remove_junk_tokens(tokens, bool_stopwords_are_junk=True, load_from_pickle = False, save_to_pickle = True, cache_path="results/.cache/clean_tokens.pkl"):
    ## load from pickle if desired
    if(load_from_pickle):
        print("(pkl) loading from " + cache_path)
        return pickle.load( open( cache_path, "rb" ) );
    
    striped_tokens = [];
    total_token_count = len(tokens);
    for index, token in enumerate(tokens):
        if(index%5000 == 0): print("removing stopwords, index:" + str(index) + " : " + str(index/float(total_token_count)) + "%");
            
        pos_part = token.split("|")[1];
        if(pos_part == "PUNCT"): continue; ## skip punctuation, they're not even words
        if(bool_stopwords_are_junk and feature_extraction.is_stop_word(token)): continue;
        striped_tokens.append(token);
        
    ## save to pickle
    if(save_to_pickle):
        pickle.dump( striped_tokens, open( cache_path, "wb" ) )
    return striped_tokens;        



def build_fulltext_from_file(source_file):
    print(source_file);
    ## To Do, handle document_delimeter != newline
    f = open(source_file, 'r');
    docs = [];
    for index, line in enumerate(f.readlines()):
        #if (index > 10): break;  
        docs.append(line.rstrip());
    f.close();
    
    text = " __DOCEND__ ".join(docs);
    
    return text;


def calculate_top_words(tokens, number_of_most_common_to_return=200, load_from_pickle = False):
    ## remove stopwords and punct from topwords calculation
    tokens = remove_junk_tokens(tokens, load_from_pickle=load_from_pickle);
    
    ## calculate most common words out of clean tokens
    frequencies = collections.Counter(tokens);
    #print("Most common 200:");
    print(frequencies.most_common(200))
    return [freq_tuple[0] for freq_tuple in frequencies.most_common(number_of_most_common_to_return)];

def find_indices_of_top_words(top_words, tokens, load_from_pickle = False, save_to_pickle = True, cache_path="results/.cache/topword_indicies.pkl"):
    ## load from pickle if desired
    if(load_from_pickle):
        print("(pkl) loading from " + cache_path)
        return pickle.load( open( cache_path, "rb" ) );
    
    ## calculate indicies at which the words are found
    indices = [];
    for i, x in enumerate(tokens):
        if (i %2000 == 0): print("at index " + str(i) + " in searching for topwords");
        if x in top_words: indices.append(i);
            
    ## save to pickle
    if(save_to_pickle):
        pickle.dump( indices, open( cache_path, "wb" ) )
    return indices;
    
def calculate_similarities_for_top_words(indices, tokens, load_from_pickle = False, save_to_pickle = True, cache_path="results/.cache/similarities.pkl"):
    if(load_from_pickle):
        print("(pkl) loading from " + cache_path)
        return pickle.load( open( cache_path, "rb" ) )
    
    stats = dict({
        "all":[],
        "prev":[],
        "next":[],
        "words":dict(),
    });
    ## for each index, get word in front and behind and compare to target word. Record similarity under target word's dict. Also, record similarity under an "all" dict.
    total_indices = (len(indices));
    min_index = 0;
    max_index = len(tokens);
    for i, index in enumerate(indices):
        if (i %2000 == 0): print("at index " + str(i) + " of " + str(total_indices) + " in calcing stats");
        target_word = tokens[index];
        if(target_word not in stats["words"]): stats["words"][target_word] = [];
        prev_word = False;
        next_word = False;
        prev_index = index - 1;
        next_index = index + 1;
        if(prev_index >= min_index): prev_word = tokens[prev_index];
        if(next_index <= max_index): next_word = tokens[next_index];
        if(prev_word != False): 
            prev_sim = feature_extraction.similarity(target_word, prev_word);
            if(prev_sim != False):
                stats["words"][target_word].append(prev_sim);
                stats["all"].append(prev_sim);
                stats["prev"].append(prev_sim);
        if(next_word != False): 
            next_sim = feature_extraction.similarity(target_word, next_word);
            if(next_sim != False):
                stats["words"][target_word].append(next_sim);
                stats["all"].append(next_sim);
                stats["next"].append(next_sim);

    ## save to pickle
    if(save_to_pickle):
        pickle.dump( stats, open( cache_path, "wb" ) )
    return stats;
    
    
def plot_similarities_as_histograms(base_title, similarities):  
    basics = dict({
        "all" : similarities["all"],
        "next" : similarities["next"],
        "prev" : similarities["prev"],
    });
    plotting.plot_metrics_on_histogram(basics, base_title+"-basics", normalized = True);
    
@plac.annotations(
    source_file=("Path to source file"),
)
def main(source_file):
    base_file_name = ".".join(source_file.split("/")[-1].split(".")[:-1]); # retreive file name w/o extension
    
    print("getting text from file...");
    text = build_fulltext_from_file(source_file);
    
    print("breakup text into word tokens");
    tokens = feature_extraction.split_sentence_into_tokens(text);
    
    print("calculating top words");
    top_words = calculate_top_words(tokens, load_from_pickle = True);
    
    print("calculating top word indicies")
    top_word_indices = find_indices_of_top_words(top_words, tokens, load_from_pickle = True);
    
    print("calculating similarities for top words...");
    similarities = calculate_similarities_for_top_words(top_word_indices, tokens, load_from_pickle = True);   
    
    print("plot similarities");
    plot_similarities_as_histograms("top200-"+base_file_name, similarities);
    
    
    
    
    
if __name__ == '__main__':
    plac.call(main)



