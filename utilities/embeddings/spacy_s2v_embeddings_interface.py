import sense2vec
# https://github.com/explosion/sense2vec

'''
model = sense2vec.load()
freq, query_vector = model["natural_language_processing|NOUN"]
model.most_similar(query_vector, n=3)
'''


model = False;
not_found_set = set();
def similarity_between_words(word_a, word_b):
    global model;
    global not_found_list;
    load_embeddings();
        
    # convert to unicode
    word_a = word_a.decode('utf-8',errors='ignore');
    word_b = word_b.decode('utf-8',errors='ignore');
        
    # grab vectors
    if(word_a not in model):
        #if(word_a not in not_found_set): print("(!) - " + word_a + " was not found");
        not_found_set.add(word_a);
        return False;
    if(word_b not in model):
        #if(word_b not in not_found_set): print("(!) - " + word_b + " was not found");
        not_found_set.add(word_b);
        return False;
    freq_a, vec_a = model[word_a];
    freq_b, vec_b = model[word_b];
    
    similarity =  model.data.similarity(vec_a, vec_b);
    #print(word_a + " dot " + word_b + " = " + str(similarity));
    return similarity;

def load_embeddings():
    global model;
    global not_found_list;
    if(model == False):
        print("(*) Loading sense2vec model for first time...");
        model = sense2vec.load(); #load it only when nessesary
        #print("Done loading sense2vec model");
    