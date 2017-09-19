# merge all essays from essay set X with score > Y


import csv

essay_set_identifier = "all";
threshold_score = 0.2;
threshold_type = "higher";

## read all lines
header_list = ["essay_id", "essay_set", "score", "essay"];
data_list = [];
with open("essay_sets/essay_set_"+essay_set_identifier+".csv", "rb") as f:
    reader = csv.reader(f)
    for i, line in enumerate(reader):
        data_list.append(line);
        #if(i>10): break;
        if(i % 1000 == 0): print("reading line " + str(i))
            
## grab all essays w/ score > threshold_score
essays = [];
score_index = header_list.index("score");
essay_index = header_list.index("essay");
for i, line in enumerate(data_list):
    if(float(line[score_index]) >= threshold_score and threshold_type == "lower"): essays.append(line[essay_index]);
    if(float(line[score_index]) <= threshold_score and threshold_type == "higher"): essays.append(line[essay_index]);
    if(i % 1000 == 0): print("checking line " + str(i))
print("found a total of " + str(len(essays)) + " w/ score not " + threshold_type + " than " + str(threshold_score));    
    
## output file w/ all text merged together and delimited by "\n");
with open("text_by_score/set_"+essay_set_identifier+"_not"+threshold_type+"_thres_"+str(threshold_score)+".txt", "w+") as file: 
    for i, essay in enumerate(essays):
        if(i % 1000 == 0): print("writing essay " + str(i));
        file.write(essay + "\n");