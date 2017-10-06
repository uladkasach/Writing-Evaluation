import sys;
import numpy as np;
import re;


## this file contains many helpful functions for dealing with word vectors and utilizes the googlenews vectors
vector_source = "inputs/GoogleNews-vectors-negative300.csv"
bool_load_into_ram = True
embedding_dictionary = False;
dev_word_limit = 200000;

def extract_word_and_vector_from_line(line):
    parts = line.rstrip().split(" ");
    this_word = parts[0];
    this_vector = [float(j) for j in parts[1:]];
    return [this_word, this_vector];



def return_embedding_dictionary(source):
    embedding_dictionary = dict();
    global dev_word_limit;

    ## load lines
    with open(source) as file:
        if(True): #devmode
            lines = [];
            with open(vector_source) as file:
                index = -1;
                for line in file:
                    index += 1;
                    lines.append(line);
                    if(index > dev_word_limit): break;
        else:
            lines = file.readlines();

    ## build dictionary
    for index, line in enumerate(lines):
        result = extract_word_and_vector_from_line(line);
        this_word = result[0];
        this_vector = result[1];
        embedding_dictionary[this_word] = this_vector;
        if(index % 10000 == 0): print("At wordvector " + str(index));

    ## return dictionary
    return embedding_dictionary;

not_found_set = set();
def find_word_vector(word):
    if(word == "$PURPOSEFULL-SKIP-KEY$"): return False;

    global not_found_set;
    global vector_source;
    global bool_load_into_ram;
    global embedding_dictionary;
    if bool_load_into_ram:
        if(embedding_dictionary == False):
            print("Loading embeddings dictionary");
            embedding_dictionary = return_embedding_dictionary(vector_source)
        if word in embedding_dictionary:
            return embedding_dictionary[word];
        else:
            not_found_set.add(word);
            return False;

    else:
        with open(vector_source) as file:
            index = -1;
            for line in file:
                index += 1;
                result = extract_word_and_vector_from_line(line);
                this_word = result[0];
                this_vector = result[1];

                if(word == this_word):
                    return this_vector;

                if(index > 100000):
                    not_found_set.add(word);
                    #print("could not find word " + word);
                    return False; ## giveup here for testing speed's sake


    return vector;

def calculate_cosine_similarity_between_vectors(vec_a, vec_b):
    '''
    A dot B = |A||B|cosine(theta)
    return cosine(theta)
    '''
    if(len(vec_a) != len(vec_b)):
        print("Length of Vector A and Vector B are not equal \n ");
        return -1;
    cos = np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))
    return cos;

def similarity_between_words(word_a, word_b):
    word_a = re.sub(r'[^a-zA-Z]', '', word_a) # remove nonalphanumberic
    word_b = re.sub(r'[^a-zA-Z]', '', word_b) # remove nonalphanumberic

    vector_a = find_word_vector(word_a);
    vector_b = find_word_vector(word_b);
    if(vector_a == False or vector_b == False): return False;
    return calculate_cosine_similarity_between_vectors(vector_a, vector_b);
