from spacy.en import English
import re

LABELS = {
    'ENT': 'ENT',
    'PERSON': 'ENT',
    'NORP': 'ENT',
    'FAC': 'ENT',
    'ORG': 'ENT',
    'GPE': 'ENT',
    'LOC': 'ENT',
    'LAW': 'ENT',
    'PRODUCT': 'ENT',
    'EVENT': 'ENT',
    'WORK_OF_ART': 'ENT',
    'LANGUAGE': 'ENT',
    'DATE': 'DATE',
    'TIME': 'TIME',
    'PERCENT': 'PERCENT',
    'MONEY': 'MONEY',
    'QUANTITY': 'QUANTITY',
    'ORDINAL': 'ORDINAL',
    'CARDINAL': 'CARDINAL'
}



nlp = False;
def tag_words_in_sense2vec_format(passage):
    global nlp; 
    if(nlp == False): nlp = English()
    if isinstance(passage, str): passage = passage.decode('utf-8',errors='ignore');
    doc = nlp(passage);
    strings = transform_doc(doc);
    if strings:
        return '\n'.join(strings) + '\n'
    else:
        return ''
    
def transform_doc(doc):
    doc = preprocess_doc(doc, bool_loud = True);
    strings = []
    for index, sent in enumerate(doc.sents):
        if sent.text.strip():
            strings.append(' '.join(represent_word(w) for w in sent if not w.is_space))
        if index % 100 == 0: print ("converting at sentence index " + str(index));
    return strings;

def preprocess_doc(doc, bool_loud = False):
    for index, ent in enumerate(doc.ents):
        ent.merge(ent.root.tag_, ent.text, LABELS[ent.label_].decode('utf-8',errors='ignore'))
        if index % 100 == 0 and bool_loud: print ("enumerating at entity index " + str(index));
    #for np in doc.noun_chunks:
    #    while len(np) > 1 and np[0].dep_ not in ('advmod', 'amod', 'compound'):
    #        np = np[1:]
    #    np.merge(np.root.tag_, np.text, np.root.ent_type_)
    return doc;

def represent_word(word):
    if word.like_url:
        return '%%URL|X'
    text = re.sub(r'\s', '_', word.text)
    tag = LABELS.get(word.ent_type_, word.pos_)
    if not tag:
        tag = '?'
    return text + '|' + tag
