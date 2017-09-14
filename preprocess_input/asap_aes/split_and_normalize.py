## this script splits the asap_aes dataset and normalizes the scores

import csv
import math

## read all lines
header_list = None;
data_list = [];
with open("source/asap_aes.csv", "rb") as f:
    reader = csv.reader(f)
    for i, line in enumerate(reader):
        if(i == 0): 
            header_list = line;
        else:
            data_list.append(line);

        #if(i>10): break;
        if(i % 1000 == 0): print("reading line " + str(i))
                

## group by essay set
essay_set_index = header_list.index("essay_set");
essay_sets = dict();
for i, line in enumerate(data_list):
    this_set_index = line[essay_set_index];
    if(this_set_index not in essay_sets): essay_sets[this_set_index] = [];
    essay_sets[this_set_index].append(line);
    if(i % 1000 == 0): print("grouping line " + str(i))
    

## find max score for each dataset
def find_max_score_in_set(essay_set):
    score_index = header_list.index("domain1_score");
    max_score = 0;
    for i, line in enumerate(essay_set):
        this_score = (line[score_index]);
        if(this_score == ""): continue;
        this_score = int(this_score);
        print(this_score);
        if(this_score > max_score): max_score = this_score;
    return max_score;
max_scores = dict();
for essay_set_key in essay_sets.keys():
    print("finding max score for " + essay_set_key);
    max_scores[essay_set_key] = find_max_score_in_set(essay_sets[essay_set_key]);
print("max_scores:");
print(max_scores);

## Normalize score of each dataset out of max score and strip irrelevant information (lines 3+)
def normalize_scores_in_set(essay_set, max_score):
    score_index = header_list.index("domain1_score");
    normalized_essay_set = [];
    for i, line in enumerate(essay_set):
        normalized_line = line[:3];
        this_score = line[score_index];
        if(this_score == ""): continue;
        normalized_score = int(this_score)/float(max_score);
        normalized_score = math.ceil(normalized_score * 100.0) / 100.0;
        normalized_line.append(normalized_score);
        normalized_line[2], normalized_line[3] = normalized_line[3], normalized_line[2] # puts score value before essay text
        print(normalized_score);
        normalized_essay_set.append(normalized_line);
        
    return normalized_essay_set;
normalized_essay_sets = dict();
for essay_set_key in essay_sets.keys():
    print("normalizing " + essay_set_key);
    normalized_essay_sets[essay_set_key] = normalize_scores_in_set(essay_sets[essay_set_key], max_scores[essay_set_key]);
#print(normalized_essay_sets);

## save essay sets in distinct files and save one with all
def save_this_normalized_essay_set(essay_set, set_key):
    with open("essay_sets/essay_set_"+str(set_key)+".csv", "w+") as file:
        writer = csv.writer(file);
        for line in essay_set:
            writer.writerow(line); 
all_sets = [];
for essay_set_key in normalized_essay_sets.keys():
    print("recording " + essay_set_key);
    this_essay_set = normalized_essay_sets[essay_set_key];
    save_this_normalized_essay_set(this_essay_set, essay_set_key);
    all_sets.extend(this_essay_set);
print("recording " + "all");
save_this_normalized_essay_set(all_sets, "all");