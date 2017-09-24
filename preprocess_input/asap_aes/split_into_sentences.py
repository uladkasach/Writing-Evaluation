from __future__ import unicode_literals, print_function
import csv

'''

split essays into sentences, 
- [SCORE, ESSAY_ID, ESSAY_SET_ID, ESSAY_TEXT]
record as csv

'''

###########################################################################
## import dependencies
###########################################################################
if __name__ == '__main__' and __package__ is None or True: ## enables imports of sibling "packages"
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
import utilities.plotting as plotting;
##########################
import utilities.spacy as spacy_utils; 

essay_set_identifier = "all";




## read all lines
header_list = ["essay_id", "essay_set", "score", "essay"];
data_list = [];
with open("essay_sets/essay_set_"+essay_set_identifier+".csv", "rb") as f:
    reader = csv.reader(f)
    for i, line in enumerate(reader):
        data_list.append(line);
        #if(i>10): break;
        if(i % 1000 == 0): print("reading line " + str(i))
            
            
            
## Split each essay by sentences. Then tag each word. Utilize spacy for this.
data = [];
essay_index = header_list.index("essay");
for i, this_essay in enumerate(data_list):
    essay = this_essay[essay_index];
    print(essay);
    sentences_for_essay = spacy_utils.general.split_passage_by_sentences(essay);
    for sentence in sentences_for_essay:
        tagged_text = spacy_utils.sense2vec.tag_words_in_sense2vec_format(sentence);
        this_sentence_data = dict({
            "essay_id": this_essay[header_list.index("essay_id")],
            "essay_set": this_essay[header_list.index("essay_set")],
            "score": this_essay[header_list.index("score")],
            "text": tagged_text,
        })
        print(this_sentence_data);
        data.append(this_sentence_data);
    if(i % 1000 == 0): print("splitting essay at index " + str(i))
print("found a total of " + str(len(data)) + " sentences");    

## output data as csv
with open("sentences/sentences_of_set_"+essay_set_identifier+".csv", "w+") as file:
    writer = csv.writer(file);
    for i, sentence in enumerate(data):
        if(i % 200 == 0): print("writing sentence " + str(i));
        data_list = [sentence["essay_id"], sentence["essay_set"], sentence["score"], sentence["text"].encode('ascii', 'ignore').rstrip()]
        writer.writerow(data_list); 