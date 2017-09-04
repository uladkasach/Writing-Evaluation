import sys;
import numpy as np;
import json;
import string;
import embeddings;
import matplotlib.pyplot as plt;
import matplotlib.mlab as mlab;
import json;
import nltk;



source = "inputs/bigquery_10.json"
bool_remove_stopwords = False;
pos_tagged_words = True;
if(pos_tagged_words == True):
    embeddings.init("sense2vec");
else:
    embeddings.init("word2vec");


#similarity = embeddings.similarity("apple", "art");
#print(similarity);


def remove_stopwords(word_list):
    global bool_remove_stopwords;
    if(not bool_remove_stopwords): return word_list;
    stopwords = nltk.corpus.stopwords.words("english");
    striped_wordlist = [];
    for word in word_list:
        tokens = nltk.word_tokenize(word.lower());
        if(tokens[0] not in stopwords): striped_wordlist.append(word);
    return striped_wordlist;        
        
        
def split_sentences_by_delimeter(delimeter, sentences):
    fragments = [];
    for sentence in sentences:
        fragments.extend(sentence.split(delimeter));
    return fragments;
def find_sentences_by_spliting_periods_plus_heuristics(text):
    ## replace Mr. Mrs. Ms. Dr. w/ Mr_, Mrs_, Ms_, Dr_
    replacements = [
        ["Mr.", "Mr_"],
        ["mr.", "mr_"],
        ["Mrs.", "Mrs_"],
        ["mrs.", "mrs_"],
        ["Ms.", "Ms_"],
        ["ms.", "ms_"],
        ["Dr.", "Dr_"],
        ["dr.", "dr_"],
        ["Rev.", "Rev_"],
        ["rev.", "rev_"],
    ];
    for replacement_mapping in replacements:
        text = text.replace(replacement_mapping[0], replacement_mapping[1])
    
    ## split text by all periods
    potential_sentences = text.split(".");
    
    ## simple heuristic to remove "non-sentenses"
    ## if a part has less than 3 words, remove it. We define a word as an alpha string > 2 characters
    sentences = [];
    for potential_sentence in potential_sentences:
        potential_words = potential_sentence.split(" ");
        real_words = [];
        for potential_word in potential_words:
            letter_count = 0;
            not_word = False;
            for character in potential_word:
                if(character not in string.ascii_letters+"-,;:\"'_@"): not_word = True;
            if(not not_word and (potential_word == "a" or potential_word == "I" or len(potential_word) > 1)):  real_words.append(potential_word);
        if(len(real_words) > 3):
            sentences.append(" ".join(remove_stopwords(real_words))); 
    #print(sentences[:45]);
    #print("Sentence count : " + str(len(sentences)));
    
    ## return sentences
    sentences = sentences[15:-15]; ## skip first 15 sentenses and last 15 senteses
    
    final_sentences = [];
    ## reverse replacements
    for sentence in sentences:
        for replacement_mapping in replacements:
            sentence = sentence.replace(replacement_mapping[1], replacement_mapping[0])
        final_sentences.append(sentence);
        
    return final_sentences;

def get_border_words_from_segments(sentences):
    
    ## grab the 6 words (3 left of, 3 right of) the period
    sentence_borders = [];
    last_sentence = False;
    for sentence in sentences:
        this_sentence_border = [];
        if(last_sentence != False):
            this_sentence_border.extend(last_sentence.split(" ")[-3:]);
        this_sentence_border.extend(sentence.split(" ")[:3]);
        if(len(this_sentence_border) == 6): sentence_borders.append(this_sentence_border);
        last_sentence = sentence;
    
    ## return data
    return sentence_borders;

def calculate_consecutive_word_similarities_in_word_list(words):
    prior_word = False;
    similarities = [];
    word_pairs = [];
    for word in words:
        if(prior_word != False):
            similarities.append(embeddings.similarity(prior_word, word));
            word_pairs.append((prior_word + "," + word).ljust(18));
        prior_word = word;
    return [similarities, word_pairs];

def demonstrate_sentence_similarities(sentence):
    print(sentence);
    result = calculate_consecutive_word_similarities_in_word_list(sentence.split(" "))
    print(result[1]);
    print(result[0]);
    print (" ")

#demonstrate_sentence_similarities("the dog barked loudly at the mailman");
#demonstrate_sentence_similarities("the man barked nails at the wood");
#demonstrate_sentence_similarities("the dog hammered loudly into mailman");
#demonstrate_sentence_similarities("the man hammered nails into wood");
#demonstrate_sentence_similarities("the worker hammered nails into wood");
#demonstrate_sentence_similarities("the builder hammered nails into wood");


#demonstrate_sentence_similarities("it was more oftenly used");
#demonstrate_sentence_similarities("it was more often used");
#demonstrate_sentence_similarities("it was used more often");
#exit();


def convert_doc_to_text(source):
    f = open(source, 'r');
    text = [];
    for index, line in enumerate(f.readlines()):
        (index > 100): break;  
        text.append(line);
    text = "\n".join(text);
    f.close();
def calculate_similarities_for_text(input_text):
    similarities = dict({
        "_meta" : dict({
            "index" : index, 
        }),
        "consecutive" : [],
        "period" : [],
        "comma" : [],
        "semicolon" : [],
        "colon" : [],
    })
    
    
    ## get sentences 
    if(pos_tagged_words == False):
        # use a heuristic to avoid poor segmentation
        sentences = find_sentences_by_spliting_periods_plus_heuristics(input_text);
    else:
        split_sentences_by_delimeter(comma_delimeter, [input_text]);
        
    ## Get comma delimited fragments in sentences
    comma_delimeter = ",";
    if(pos_tagged_words == True): comma_delimeter += "|PUNCT";
    comma_fragments = split_sentences_by_delimeter(comma_delimeter, sentences);
    
    #print(json.dumps(sentences, indent=2));
    #print(json.dumps(comma_fragments, indent=2));
    #sentences = sentences[:10000]; # dev limit
    #print(sentences);
    
    
    ################################
    ## General Similarities
    ################################
    print("Calculating consecutive...");
    all_words_in_order = [];
    for sentence in sentences: 
        all_words_in_order.extend([word for word in sentence.split(" ")]);
        all_words_in_order.append("$PURPOSEFULL-SKIP-KEY$"); ## deliminate sentences
        all_words_in_order.append("$PURPOSEFULL-SKIP-KEY$"); ## deliminate sentences
    ##print(all_words_in_order);
    ##print(len(all_words_in_order))
    previous_word = False;
    for word in all_words_in_order:
        if(previous_word != False):
            this_similarity = embeddings.similarity(previous_word, word);
            # print(previous_word + " dot " + word + " = " + str(this_similarity));
            if(this_similarity != False): similarities["consecutive"].append(this_similarity);
        previous_word = word;
    
        
    ################################
    ## Border Statistics
    ################################
    print("Calculating borderwords...");

    period_borders = get_border_words_from_segments(sentences);
    for border_set in period_borders:
        this_similarity = embeddings.similarity(border_set[2], border_set[3]);
        if(this_similarity != False): similarities["period"].append(this_similarity);
    
    comma_borders = get_border_words_from_segments(comma_fragments);
    for border_set in comma_borders:
        this_similarity = embeddings.similarity(border_set[2], border_set[3]);
        if(this_similarity != False): similarities["comma"].append(this_similarity);
    
    
    return similarities;
    
## statistically assess similarities
## include mean and stdev





###################################################
## start calculating similarities
###################################################
all_similarities = [];
input_text = convert_doc_to_text(source);
all_similarities.append(calculate_similarities_for_text(input_text));



###################################################
## calculate statistics from similarities
###################################################
all_statistics = [];
for similarities in all_similarities:
    statistics = dict();
    desired_keys = ["consecutive", "period", "comma"] # "comma", "colon", "semicolon"];
    for desired_key in desired_keys:
        similarity_list = similarities[desired_key];
        #print(similarity_list);
        n = len(similarity_list);
        avg = np.mean(similarity_list);
        stdev = np.std(similarity_list);
        statistics[desired_key] = dict({
            "n" : n,
            "avg" : avg,
            "stdev" : stdev,
        });
    all_statistics.append(statistics);
print json.dumps(all_statistics, indent=2)
    
print ("Words not found = " + str(len(embeddings.not_found_list)))    
    
###################################################
## plot histograms of data
###################################################
fig, ax = plt.subplots(nrows=1, ncols=len(all_similarities))
for index in range(len(all_similarities)):
    similarities = all_similarities[index];
    statistics = all_statistics[index];
    metrics = (statistics.keys())
    this_axis = ax[index];

    data_list = [];
    weights = [];
    labels = [];
    for metric in metrics:
        this_list = similarities[metric];
        this_weight = np.ones_like(this_list)/float(len(this_list))
        data_list.append(this_list);
        weights.append(this_weight);
        labels.append(metric);

    num_bins = 30
    
    single_fig, single_ax = plt.subplots()
    # the histogram of the data
    colors = ['green', 'purple', 'lightblue'];
    colors = colors[:len(metrics)];
    n, bins, patches = single_ax.hist(data_list, num_bins, color=colors, weights=weights, label=labels)
    single_ax.legend(prop={'size': 10})
    n, bins, patches = this_axis.hist(data_list, num_bins, color=colors, weights=weights, label=labels)
    this_axis.legend(prop={'size': 10})
    
    
    single_fig.tight_layout();
    single_fig.savefig("results/figure_"+str(index)+".png"); 

# Tweak spacing to prevent clipping of ylabel
#fig.tight_layout()
#plt.show()


        