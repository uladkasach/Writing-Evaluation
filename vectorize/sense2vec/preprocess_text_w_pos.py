'''
Usage:

python preprocess_text_w_pos.py -b inputs outputs

where inputs and outputs are directories

'''



from __future__ import print_function, unicode_literals, division
import io
import bz2
import logging
from toolz import partition
from os import path
import os
import re

import spacy
import spacy.en
from preshed.counter import PreshCounter
from spacy.tokens.doc import Doc

from joblib import Parallel, delayed
import plac
try:
    import ujson as json
except ImportError:
    import json


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


def load_and_transform(batch_id, in_loc, out_dir):
    
    
    out_loc = path.join(out_dir, '%d.txt' % batch_id)
    if path.exists(out_loc):
        print("Overwriting existing file");
    print('Batch', batch_id)
    print("loading spacy...");
    nlp = spacy.load('en')
    #nlp = spacy.en.English(parser=False, tagger=False, matcher=False, entity=False)
    
    
    print("opening files...");
    with io.open(out_loc, 'w', encoding='utf8') as out_file:
        with io.open(in_loc, 'rb') as in_file:
            for byte_string in Doc.read_bytes(in_file):
                print("decoding the strings...")
                doc = nlp((byte_string).decode('utf-8',errors='ignore'));
                #doc = Doc(nlp.vocab).from_bytes(byte_string)
                #print(doc);
                print("Length of doc : " + str(doc.__len__()));

                #for word in doc:
                #    print(word.text, word.lemma, word.lemma_, word.tag, word.tag_, word.pos, word.pos_)
                
                doc.is_parsed = True
                print("transforming and writing document...");
                out_file.write(transform_doc(doc)) 



def transform_doc(doc):
    for index, ent in enumerate(doc.ents):
        ent.merge(ent.root.tag_, ent.text, LABELS[ent.label_])
        if index % 100 == 0: print ("enumerating at entity index " + str(index));
    #for np in doc.noun_chunks:
    #    while len(np) > 1 and np[0].dep_ not in ('advmod', 'amod', 'compound'):
    #        np = np[1:]
    #    np.merge(np.root.tag_, np.text, np.root.ent_type_)
    strings = []
    for index, sent in enumerate(doc.sents):
        if sent.text.strip():
            strings.append(' '.join(represent_word(w) for w in sent if not w.is_space))
        if index % 100 == 0: print ("converting at sentence index " + str(index));
    if strings:
        return '\n'.join(strings) + '\n'
    else:
        return ''


def represent_word(word):
    if word.like_url:
        return '%%URL|X'
    text = re.sub(r'\s', '_', word.text)
    tag = LABELS.get(word.ent_type_, word.pos_)
    if not tag:
        tag = '?'
    return text + '|' + tag


@plac.annotations(
    in_loc=("Location of input file"),
    out_dir=("Location of output dir"),
    n_workers=("Number of workers", "option", "n", int),
    load_parses=("Load parses from binary", "flag", "b"),
)
def main(in_loc, out_dir, n_workers=4, load_parses=False):
    load_and_transform(2, in_loc, out_dir)

if __name__ == '__main__':
    plac.call(main)
