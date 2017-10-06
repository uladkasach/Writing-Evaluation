import sense2vec
# https://github.com/explosion/sense2vec

'''
model = sense2vec.load()
freq, query_vector = model["natural_language_processing|NOUN"]
model.most_similar(query_vector, n=3)
'''


model = False;
def similarity_between_words(word_a, word_b):
    global model;
    load_embeddings();

    vec_a = get_vector_for(word_a);
    vec_b = get_vector_for(word_b);
    if(vec_a == False or vec_b == False): return False;

    similarity =  model.data.similarity(vec_a, vec_b);
    #print(word_a + " dot " + word_b + " = " + str(similarity));
    return similarity;

not_found_set = set();
def get_vector_for(word):
    global model;
    load_embeddings();

    global not_found_set;
    word_a = word.decode('utf-8',errors='ignore'); ## convert to unicode

    if(word_a not in model): ## ensure its in the model
        #if(word_a not in not_found_set): print("(!) - " + word_a + " was not found");
        not_found_set.add(word_a);
        return False;

    freq_a, vec_a = model[word_a];
    return vec_a;



def load_embeddings():
    global model;
    global not_found_list;
    if(model == False):
        print("(*) Loading sense2vec model for first time...");
        model = sense2vec.load(); #load it only when nessesary
        #print("Done loading sense2vec model");
