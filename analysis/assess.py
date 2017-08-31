import sys;
import numpy as np;
import json;
import string;
from gensim.models import Word2Vec;

source = "inputs/bigquery_10.json"
vector_source = "inputs/GoogleNews-vectors-negative300.csv"



def find_sentences_spliting_periods(text):
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
                if(character not in string.ascii_letters+"-,\"'_@"): not_word = True;
            if(not not_word and (potential_word == "a" or potential_word == "I" or len(potential_word) > 1)):  real_words.append(potential_word);
        if(len(real_words) > 3): sentences.append(" ".join(real_words)); 
    #print(sentences[:45]);
    #print("Sentence count : " + str(len(sentences)));
    
    ## return sentences
    return sentences;

def get_border_words_for_periods(text):
        
    ## get sentenses from text
    sentences = find_sentences_spliting_periods(text);
    # print(sentences[:15]);
    sentences = sentences[15:-15]; ## skip first 15 sentenses and last 15 senteses
    
    
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


## load word vectors
model = Word2Vec.load(vector_source)
print(model.similarity('france', 'spain'));
exit();

## start calculating similarities
period_border_window_1_similarities = [];
f = open(source, 'r');
for line in f.readlines():
    ## convert line into json
    json_data = line; 
    d = json.loads(json_data)
    
    ## get borders for periods
    period_borders = get_border_words_for_periods(d["BookMeta_FullText"]);
    
    ## display
    print(period_borders[:16]);
    
    ## calculate cosine similarities between immediate border words
    for border_set in period_borders:
        period_border_window_1_similarities.append(find_similarity_between(border_set[2], border_set[3]));
    
    ## break - for dev mode
    break;
    
## statistically assess similarities
## include mean and stdev
    