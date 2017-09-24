from spacy.en import English

nlp = False;
def split_passage_by_sentences(passage):
    global nlp; 
    if(nlp == False): nlp = English()
    if isinstance(passage, str): passage = passage.decode('utf-8',errors='ignore');
    doc = nlp(passage);
    sentences = [sent.string.strip() for sent in doc.sents]
    return sentences;
    