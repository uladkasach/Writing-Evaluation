'''
import ..utilities.embeddings.interface as embeddings
'''

import google_embeddings_interface;
import spacy_s2v_embeddings_interface;


## define embeddings selection
embeddings_choice = False;
def init(choice):
    global embeddings_choice;
    global sense2vec_model;
    if(choice == "word2vec"):
        embeddings_choice = "GOOGLE";
    elif(choice == "sense2vec"):
        embeddings_choice = "SPACY";
    else:
        print("Error - embeddings choice was invalid");
        
def load_embeddings():
    global embeddings_choice;
    if(embeddings_choice == False):
        print("Error - embeddings has not been initialized. (run embeddings.init(...))");
        exit();
    if (embeddings_choice == "SPACY"):
        return spacy_s2v_embeddings_interface.load_embeddings();
    
    
        
def similarity(word_a, word_b):
    global embeddings_choice;
    if(embeddings_choice == False):
        print("Error - embeddings has not been initialized. (run embeddings.init(...))");
        exit();
    if(embeddings_choice == "GOOGLE"):
        return google_embeddings_interface.similarity_between_words(word_a, word_b);
    
    if (embeddings_choice == "SPACY"):
        return spacy_s2v_embeddings_interface.similarity_between_words(word_a, word_b);
    
def retreive_not_found():
    if(embeddings_choice == "GOOGLE"):
        return list(google_embeddings_interface.not_found_set);
    else:
        return list(spacy_s2v_embeddings_interface.not_found_set);