from spacy.en import English

nlp = False;
def build_doc(passage):
    global nlp;
    if(nlp == False):
        print("(*) loading spacy english for first time...");
        nlp = English()
    if isinstance(passage, str): passage = passage.decode('utf-8',errors='ignore');
    doc = nlp(passage);
    return doc;
    
def split_passage_by_sentences(passage):
    doc = build_doc(passage);
    sentences = [sent.string.strip() for sent in doc.sents]
    return sentences;
    