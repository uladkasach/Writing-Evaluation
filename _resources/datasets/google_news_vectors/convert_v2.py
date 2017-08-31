from gensim.models.keyedvectors import KeyedVectors;

word_vectors = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
word_vectors.save_word2vec_format('GoogleNews-vectors-negative300.csv', binary=False)
