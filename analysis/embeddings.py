import google_embeddings_interface;
import sense2vec

'''
freq, query_vector = model["natural_language_processing|NOUN"]
model.most_similar(query_vector, n=3)
'''

## define embeddings selection
embeddings_choice = False;
def init(choice):
    global embeddings_choice;
    global sense2vec_model;
    if(choice == "word2vec"):
        embeddings_choice == "GOOGLE";
    elif(choice == "sense2vec"):
        embeddings_choice == "SPACY";
    else:
        print("Error - embeddings choice was invalid");
        
        
sense2vec_model = False;
def similarity(word_a, word_b):
    global embeddings_choice;
    if(embeddings_choice == False): return print("Error - embeddings has not been initialized. (run embeddings.init(...))");
    if(embeddings_choice == "GOOGLE"):
        return google_embeddings_interface.similarity_between_words(word_a, word_b);
    
    if (embeddings_choice == "SPACY"):
        global sense2vec_model;
        if(sense2vec_model == False):
            sense2vec_model = sense2vec.load(); #load it only when nessesary
        return "";
    