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
import utilities.spacy as spacy_util;

###########################################################################
## initialize dependencies
###########################################################################
loaded_embeddings_choice = "sense2vec";
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

def extract_sentence_information(sentence, chosen_list = "ALL", embeddings_choice="sense2vec"):
    assert(embeddings_choice == loaded_embeddings_choice);

    ## parse options
    compute_options = dict({
        "basic_similarities":False,
        "backscaled_similarities":False,
        "across_punctuation_similarities":False,
        "parse_tree" : False,
        "semantic" : False,
    });
    if (chosen_list == "ALL"):
        for key in compute_options.keys():
            compute_options[key] = True; ## compute all
    else:
        for key in chosen_list:
            assert(key in compute_options.keys());
            compute_options[key] = True;

    ## ensure sentence is a string
    if isinstance(sentence, six.string_types):
        sentence = split_sentence_into_tokens(sentence);
    else:
        raise Exception("Sentence is not a string... Error");

    ## strip tags if needed
    if(embeddings_choice == "word2vec" and loaded_embeddings_choice == "word2vec"):
        sentence = remove_tags_and_stringify_sentence(sentence);

    ## begin information object
    information = dict();

    if(compute_options["basic_similarities"]):
        ## calculate basic n'th order word similarities, up to 4th order
        information["similarities"] = dict();
        for i in range(5):
            information["similarities"]["d"+str(i)] = dict();
            information["similarities"]["d"+str(i)]["raw"] = calculate_nth_order_similarities(i, sentence);
            information["similarities"]["d"+str(i)]["norm"] = normalize_information_list(information["similarities"]["d"+str(i)]["raw"]);

    if(compute_options["backscaled_similarities"]):
        ## calculate scaled n'th order word similarities, up to 4th order
        information["backscaled_similarities"] = dict();
        for i in range(5):
            information["backscaled_similarities"]["d"+str(i)] = dict();
            information["backscaled_similarities"]["d"+str(i)]["raw"] = calculate_backscaled_nth_order_similarities(i, sentence);
            information["backscaled_similarities"]["d"+str(i)]["norm"] = normalize_information_list(information["backscaled_similarities"]["d"+str(i)]["raw"]);


    ## calculate parse_tree similarities
    #information["parse_tree_similarities"] = [];

    if(compute_options["across_punctuation_similarities"]):
        ## across punctuation statistics
        punctuation_choices = dict({
            "comma" : ",|PUNCT",
        });
        information["across_punctuation_similarities"] = dict();
        for punctuation in punctuation_choices.keys():
            information["across_punctuation_similarities"][punctuation] = dict();
            information["across_punctuation_similarities"][punctuation]["raw"] = calculate_similarities_across_punctuation(punctuation_choices[punctuation], sentence);
            information["across_punctuation_similarities"][punctuation]["norm"] = normalize_information_list(information["across_punctuation_similarities"][punctuation]["raw"]);

    if(compute_options["parse_tree"]):
        ## calculate syntax tree based similarities for lexically significant word pairs
        parse_choices = [
            ("V-N", ["VERB"], ["NOUN", "PRON"]),
            ("N-ADJ", ["NOUN", "PRON"], ["ADJ"]),
            ("V-ADV", ["VERB"], ["ADV"]),
            #("V-V", ["VERB"], ["VERB"]),
            ("N-N", ["NOUN", "PRON"], ["NOUN", "PRON"]),
        ]
        information["parse_tree"] = dict();
        for choice in parse_choices:
            information["parse_tree"][choice[0]] = dict();
            information["parse_tree"][choice[0]]["raw"] = calculate_similarities_for_parse_tree_pairs(sentence, type_a = choice[0], type_b = choice[1]);
            information["parse_tree"][choice[0]]["norm"] = normalize_information_list(information["parse_tree"][choice[0]]["raw"]);


    ## calculate sentence length
    information["length"] = len(sentence);
    information["length_convinience"] = dict(); ## convinience way of accessing this len data
    information["length_convinience"]["raw"] = [len(sentence)];
    information["length_convinience"]["norm"] = normalize_information_list(information["length_convinience"]["raw"]);

    ## calculate word lengths
    information["word_lengths"] = dict();
    information["word_lengths"]["raw"] = [len(word.split("|")[0]) for word in sentence];
    information["word_lengths"]["norm"] = normalize_information_list(information["word_lengths"]["raw"]);

    if(compute_options["semantic"]):
        ## semantic, note since semantic data is a vector representation of the word, statistical analysis (norm) is not defined or conducted
        information["semantic"] = dict();
        information["semantic"]["average"] = compute_average_word_vector(sentence);

    ## return info
    return information;

def compute_average_word_vector(sentence, normalize=True):
    vectors = [];
    for word in sentence:
        vector = embeddings.vector(word);
        if(type(vector) is not bool):
            vectors.append(vector);
    if(len(vectors) == 0): return False;
    vectors = np.array(vectors);
    average = np.mean(vectors, axis=0);

    if(normalize):
        average = average / (np.dot(average, average));
        
    average = average.tolist();


    return average;

'''
sentence = "Dear|VERB Local_Newspaper|ENT ,|PUNCT  I|PRON have|VERB found|VERB that|ADP many|ADJ experts|NOUN say|VERB that|ADP computers|NOUN do|VERB not|ADV benifit|VERB our|ADJ society|NOUN .|PUNCT";
sentence = split_sentence_into_tokens(sentence);
compute_average_word_vector(sentence);
'''


def remove_tags_and_stringify_sentence(sentence, bool_return_parts = False):
    string = "";
    string_parts = [];
    for tagged_word in sentence:
        parts = tagged_word.split("|");
        if(len(parts) < 2): continue;

        tag = parts[1];
        word = parts[0];

        if(tag != "PUNCT" and len(string) != 0):
            string += " ";
        string += word;
        string_parts.append(word);
    if(bool_return_parts == True):
        return string_parts;
    else:
        return string;



'''
    Compute pair similarity for each word for relevant pairs of  immediate child level. See ticket https://github.com/uladkasach/Writing-Evaluation/issues/18 for more info
    For example, for noun-verbs in "Dear Local_Newspaper, I have found that many experts say that computers do not benifit our society."
    compare:
        (Local_Newspaper, Found)
        (I, Found)
        (Experts, Say)
        (Computers, Benefit)
        (Benefit, Society)
'''
def map_original_tokens_to_doced_tokens(orig_list, doc_list):
    ## must map indicies of sent to indicies of sentence -> go through in order string and match word+POS of each,
    ##      note that you may need to skip a word in either set to catch up as doc may do the following :  I|PRON 've|VERB -> I 've -> I|PRON '|PUNCT ve|PRON
    ##      note, this is only required since we dont pass the original sentence with the tagged sentence. If we did, we would get the same result.

    mapping = dict();
    next_orig_mapped_start_index = 0;
    ## find the original_tagged_word that this token corresponds to
    for token in (doc_list):
        mapped_this_word = False;
        #print("doc index : " + str(token.i));
        target_word_tagged = spacy_util.sense2vec.represent_word(token);
        for orig_index in range(next_orig_mapped_start_index, len(orig_list)):
            tagged_word = orig_list[orig_index];
            #print(" -> " + str(target_word) + "|" + str(target_pos) + " -vs- " + str(word) + "|" + str(pos));
            if(target_word_tagged == tagged_word):
                #print("    `-> match!");
                mapping[token.i] = orig_index;
                next_orig_mapped_start_index = orig_index + 1;
                mapped_this_word = True;
                break; ## found the word, move on
        #if(not mapped_this_word): print("Word " + (target_word_tagged) + " was not matched");
    return mapping;


cached_parse_tree_similarity_sentence_data = dict({ "sentence": False, "doc_list" : False, "index_mapping" : False});
def calculate_similarities_for_parse_tree_pairs(sentence, type_a = ["VERB"], type_b = ["NOUN", "PRON"]):
    global cached_parse_tree_similarity_sentence_data;
    sentence_list = sentence;

    if(sentence == cached_parse_tree_similarity_sentence_data["sentence"]):
        doc_list = cached_parse_tree_similarity_sentence_data["doc_list"];
        index_mapping = cached_parse_tree_similarity_sentence_data["index_mapping"];
    else:
        ## tokenize the sentence w/ spacy to get tree structure
        parsable_untagged_sentence = remove_tags_and_stringify_sentence(sentence);
        doc = spacy_util.general.build_doc(parsable_untagged_sentence);
        doc = spacy_util.sense2vec.preprocess_doc(doc);
        sents = [sent for sent in doc.sents];
        sent = sents[0];
        doc_list = [x for x in sent];

        ## map the doc list to the sentence list (accounts for differences in labeling and tokenization caused by text original text not being availible)
        index_mapping = map_original_tokens_to_doced_tokens(sentence_list, doc_list);

        ## display for debugging
        #spacy_util.parse_tree.show_tree_for_sentence(sent);

        cached_parse_tree_similarity_sentence_data = dict({
            "sentence": sentence, "doc_list" : doc_list, "index_mapping" : index_mapping
        })

    ## for each doc list token, if it is of type_a or type_b, compute similarities of its immediate children of oposite_type
    embeddings.load_embeddings(); ## makes debugging output cleaner
    similarities = [];
    for token in doc_list:
        if(token.pos_ in type_a):
            target_type = type_b;
        elif(token.pos_ in type_b):
            target_type = type_a;
        else:
            continue; ## we dont care about this word
        if(token.i not in index_mapping): continue; ## token was not mapped, can not be compared.
        orig_token_word = sentence_list[index_mapping[token.i]];
        #print("type match: " + token.text + "|" + token.pos_ + " ( " + orig_token_word + " )")
        for child in token.children:
            if(child.pos_ in target_type):
                if(child.i not in index_mapping): continue; ## child was not mapped, can not be compared.
                orig_child_word = sentence_list[index_mapping[child.i]];
                this_similarity = embeddings.similarity(orig_child_word, orig_token_word);
                #print(" `-> child : " + child.text + "|" + child.pos_ + " ( " + orig_child_word + " ), similarity : " + str(this_similarity));
                #print("(^) " + orig_token_word + " dot " + orig_child_word + " = " + str(this_similarity));
                if(this_similarity is not False): similarities.append(this_similarity);

    return similarities;

'''
#sentence = "Dear|NOUN local|ADJ newspaper|NOUN ,|PUNCT I|PRON 've|VERB heard|VERB that|ADP not|ADV many|ADJ people|NOUN think|VERB computers|NOUN benefit|VERB society|NOUN .|PUNCT I|PRON disagree|VERB with|ADP that|DET .|PUNCT";
sentence = "Dear|VERB Local_Newspaper|ENT ,|PUNCT  I|PRON have|VERB found|VERB that|ADP many|ADJ experts|NOUN say|VERB that|ADP computers|NOUN do|VERB not|ADV benifit|VERB our|ADJ society|NOUN .|PUNCT";
sentence = split_sentence_into_tokens(sentence);
print(calculate_similarities_for_parse_tree_pairs(sentence));
exit();
'''



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
            "n" : 0,
            "mean" : False,
            "stdev" : False,
            "max" : False,
            "min" : False,
     });

    if(len(info) == 0):   return data;

    data["n"] = len(info);
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
