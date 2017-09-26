'''

required in each case
- for each sentence:
    - similarities across comma[s]
    - n'th order similaritie[s]
    - nth order parse tree similaritie[s]
    - sentence length
    - word length[s]

'''
import six
import logging
import numpy as np
import nltk;



###########################################################################
## import dependencies
###########################################################################
if __name__ == '__main__' and __package__ is None or True: ## enables imports of sibling "packages"
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
##########################
import utilities.plotting as plotting;
import utilities.embeddings.interface as embeddings; 

###########################################################################
## initialize dependencies
###########################################################################
embeddings.init("sense2vec"); ## always use sense2vec since it produces better seperation between similarities


def plot_metrics_on_histogram(metrics, title, normalized = False, num_bins = 30, colors = None): ## utility function
    return plotting.plot_metrics_on_histogram(metrics, title, normalized, num_bins, colors);

def similarity(word_a, word_b): ## utility function
    return embeddings.similarity(word_a, word_b);

nltk_stopwords = False;
def is_stop_word(token):
    global nltk_stopwords;
    if(nltk_stopwords == False): nltk_stopwords = nltk.corpus.stopwords.words("english");
    word_part = token.split("|")[0].decode('utf-8',errors='ignore'); ## since we assume we're dealing with sence2vec vectors 
    nltk_tokens = nltk.word_tokenize(word_part.lower());
    return nltk_tokens[0] in nltk_stopwords;

def split_sentence_into_tokens(sentence):
    sentence = sentence.split(" ");
    delimeters_to_remove = ["__DOCEND__"];
    sentence = [x for x in sentence if x.rstrip() != '' and x !='\n' and x.rstrip() not in delimeters_to_remove];
    return sentence;

def extract_sentence_information(sentence):
    ## ensure sentence is a string
    if isinstance(sentence, six.string_types):
        sentence = split_sentence_into_tokens(sentence);
    else:
        raise Exception("Sentence is not a string... Error");
        
    ## begin information object
    information = dict();
    
    ## calculate basic n'th order word similarities, up to 4th order
    information["similarities"] = dict();
    for i in range(5):
        information["similarities"]["d"+str(i)] = dict();
        information["similarities"]["d"+str(i)]["raw"] = calculate_nth_order_similarities(i, sentence); 
        information["similarities"]["d"+str(i)]["norm"] = normalize_information_list(information["similarities"]["d"+str(i)]["raw"]); 
        
        
    ## calculate scaled n'th order word similarities, up to 4th order
    information["backscaled_similarities"] = dict();
    for i in range(5):
        information["backscaled_similarities"]["d"+str(i)] = dict();
        information["backscaled_similarities"]["d"+str(i)]["raw"] = calculate_backscaled_nth_order_similarities(i, sentence); 
        information["backscaled_similarities"]["d"+str(i)]["norm"] = normalize_information_list(information["backscaled_similarities"]["d"+str(i)]["raw"]); 
    
        
    ## calculate parse_tree similarities
    #information["parse_tree_similarities"] = [];
    
    ## across punctuation statistics
    punctuation_choices = dict({
        "comma" : ",|PUNCT",
    });
    information["across_punctuation_similarities"] = dict();
    for punctuation in punctuation_choices.keys():
        information["across_punctuation_similarities"][punctuation] = dict();
        information["across_punctuation_similarities"][punctuation]["raw"] = calculate_similarities_across_punctuation(punctuation_choices[punctuation], sentence);
        information["across_punctuation_similarities"][punctuation]["norm"] = normalize_information_list(information["across_punctuation_similarities"][punctuation]["raw"]);
        
        
        
    ## calculate sentence length
    information["length"] = len(sentence);
    information["length_convinience"] = dict(); ## convinience way of accessing this len data
    information["length_convinience"]["raw"] = [len(sentence)];
    information["length_convinience"]["norm"] = normalize_information_list(information["length_convinience"]["raw"]);
    
    ## calculate word lengths
    information["word_lengths"] = dict();
    information["word_lengths"]["raw"] = [len(word.split("|")[0]) for word in sentence];
    information["word_lengths"]["norm"] = normalize_information_list(information["word_lengths"]["raw"]);
    
    ## return info
    return information;

def calculate_similarities_across_punctuation(delimeter, sentence):
    sentence = " ".join(sentence);
    sentence_parts = sentence.split(delimeter);
    sentence_parts = [part for part in sentence_parts if part.rstrip() != '' and part !='\n']; ## remote empty sentence parts
    similarities = calculate_similarities_across_borders(sentence_parts);
    return similarities;

def calculate_similarities_across_borders(parts):
    similarities = [];
    previous_part = False;
    for part in parts:
        if(previous_part != False):
            prior_word = split_sentence_into_tokens(previous_part)[-1];
            after_word = split_sentence_into_tokens(part)[0];
            similarity = embeddings.similarity(prior_word, after_word);
            if(similarity != False): similarities.append(similarity);
        previous_part = part;
    return similarities; 
    
def normalize_information_list(info):
    data = dict({
            "mean" : False,
            "stdev" : False,
            "max" : False,
            "min" : False,
     });
    
    if(len(info) == 0):   return data;
    
    data["mean"] = np.mean(info);
    data["stdev"] = np.std(info);
    data["max"] = np.max(info);
    data["min"] = np.min(info);
    
    return data;
        
def calculate_backscaled_nth_order_similarities(order, sentence):
    similarities = [];
    for i in range(len(sentence)):
        this_index = i;
        prev_index = i - 1;
        nth_order_back_index = prev_index - 1 - order; ## s.t. order 0 = -1/-2
        if(prev_index < 0): continue; 
        if(nth_order_back_index < 0): continue;
        this_word = sentence[this_index];
        prev_word = sentence[prev_index];
        nth_back_word = sentence[nth_order_back_index];
        similarity_top = embeddings.similarity(this_word, prev_word);
        similarity_bot = embeddings.similarity(this_word, nth_back_word);
        if(similarity_top != False and similarity_bot != False): similarities.append(similarity_top/float(similarity_bot));
    return similarities;

def calculate_nth_order_similarities(order, sentence):
    #print("calculating "+str(order)+"'th order statistics...");
    #print(sentence);
    similarities = [];
    for i in range(len(sentence)):
        this_index = i;
        nth_word_index = i + order + 1;
        #print("comparing word at " + str(this_index) + " vs word at " + str(nth_word_index));
        if(nth_word_index > len(sentence)-1): break; ## if nth word does not exist, break here.
        this_word = sentence[this_index];
        nth_word = sentence[nth_word_index];
        similarity = embeddings.similarity(this_word, nth_word);
        if(similarity != False): similarities.append(similarity);
    return similarities;