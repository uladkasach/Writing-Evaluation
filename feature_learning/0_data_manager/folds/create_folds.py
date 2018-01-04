#!/usr/bin/env python

## Script used to create folds from the ASAP-AES dataset

import argparse
import sys
import os
import csv
import math
import random

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input-file', dest='input_file', required=True, help='Input CSV file')
parser.add_argument('-f', '--folds', dest='folds_count', default=5, help='Number of Folds')
parser.add_argument('-s', '--sets', dest='sets_to_use', default=12345678, help='Which essay sets to use (default="12345678", i.e., all)')
args = parser.parse_args()


## train, tune, test sets

def load_header_and_data_from_CSV(input_file): ## retreive list of essays and header list from input file
    header_list = None;
    data_list = [];
    with open(input_file, "rb") as f:
        reader = csv.reader(f); ## note, this automatically converts lines into lists
        for i, line in enumerate(reader):
            if(i == 0):
                header_list = line;
            else:
                data_list.append(line[:2]);
            #if(i>10): break; ## dev artifact
            if(i % 1000 == 0): print("reading line " + str(i))
    return header_list, data_list;

def group_essays_by_essay_set(data_list, header_list): ## group essays by essay set id
    ## group by essay set
    essay_set_index = header_list.index("essay_set");
    essay_sets = dict();
    for i, line in enumerate(data_list):
        this_set_index = line[essay_set_index]; ## get the essay set id of the essay
        if(this_set_index not in essay_sets): essay_sets[this_set_index] = []; ## if this is the first essay in that essay set, create that essay set list
        essay_sets[this_set_index].append(line); ## append the essay to the appropriate essay set
        if(i % 1000 == 0): print("grouping line " + str(i))
    return essay_sets;


def split_into_folds(data_list):
    elements_per_fold = math.ceil(len(data_list)/float(args.folds_count)); ## note, since we ceil() the last fold will have less than the rest
    folds = dict();
    for index, essay in enumerate(data_list):
        fold_id = int(math.floor(index / elements_per_fold)); # i.e., if elements_per_fold = 10: index(5) => fold_id(0), index(25) => fold_id(2)
        if(fold_id not in folds): folds[fold_id] = []; # if this fold id was not yet used, define the holder in the dictionary
        folds[fold_id].append(essay);
    return folds;

def check_and_clean_set_selection_argument(sets_to_use):
    sets_to_use = str(sets_to_use);
    sets = [];
    valid_sets = [1,2,3,4,5,6,7,8]
    for character in sets_to_use:
        desired_set = int(character);
        assert(desired_set in valid_sets);
        sets.append(desired_set);
    return sets;

def record_folds(folds):
    ## record train, tune, and test segmentations upon the folds
    ##      note, in reality there are folds * (folds - 1) possible combinations when using one fold for test, one for tune, and the rest for train.
    ##      since this is an excessive ammount (e.g., 20 for 5 folds), pick the fold before the test fold to be the tune fold
    set_selection_string = "".join([str(i) for i in args.sets_to_use]);
    for test_index in range(args.folds_count):
        tune_index = test_index - 1; ## fold before test is tune
        if(tune_index < 0): tune_index += args.folds_count; ## ensure its within range

        ## define the files to write to
        fold_combo_name = "fold_sets_" + set_selection_string + ".comb_" + str(test_index);
        file_paths_to_write_to = dict({
            "train" : fold_combo_name + ".train.csv",
            "tune" : fold_combo_name + ".tune.csv",
            "test" : fold_combo_name + ".test.csv",
        })

        ## remove the files if they already exist
        for key in file_paths_to_write_to:
            try:
                os.remove(file_paths_to_write_to[key])
            except OSError:
                pass

        print("Writing fold combination: " + fold_combo_name);
        ## write the appropriate folds to each file
        for key in folds:
            if(key == test_index):
                file_key = "test";
            elif(key == tune_index):
                file_key = "tune";
            else:
                file_key = "train";
            print(" `-> " + file_key + " for index " + str(key));
            file_path_to_write_to = file_paths_to_write_to[file_key];
            with open(file_path_to_write_to, "a+") as file:
                writer = csv.writer(file);
                for line in folds[key]:
                    writer.writerow(line);


def main():
    args.sets_to_use = check_and_clean_set_selection_argument(args.sets_to_use);
    print("Loading data from " + args.input_file + " and sorting it into " + str(args.folds_count) + " folds...");
    print("  `-> utilizing essay sets " + str(args.sets_to_use));

    ## load data
    header_list, data_list = load_header_and_data_from_CSV(args.input_file);

    ## filter by essay set if desired
    if(len(args.sets_to_use) < 8): ## redefine data_list to only use the requested essay sets
        essay_sets = group_essays_by_essay_set(data_list, header_list);
        print(essay_sets.keys())
        requested_data = [];
        for set_id in args.sets_to_use:
            requested_data.extend(essay_sets[str(set_id)]); ## only append lines from requested essay sets
        data_list = random.sample(requested_data, len(requested_data)); ## return the shuffled data and use that as new datalist


    ## split into k folds
    folds = split_into_folds(data_list);
    print(folds.keys())
    print(len(folds[2]));
    print(len(folds[3]));

    ## record train, tune, and test combinations of these folds
    record_folds(folds);

if __name__ == "__main__":
    main();

'''

the_data = [];
the_labels = [];
f = open(DATA_SOURCE, 'r');
lines = f.readlines();
items_per_fold = int(len(lines) / FOLDS);

## create files in which folds will be held
files = [];
for i in range(FOLDS):
    files.append(dict({"test" : open("folds/" + DATA_SOURCE+".fold_"+str(i)+"_test", "w+"), "train" : open("folds/" + DATA_SOURCE+".fold_"+str(i)+"_train", "w+")}));
for line_index, line in enumerate(lines):
    if(line.rstrip() == ""): continue;
    for file_index, a_file in enumerate(files):
        ## first 50 go in test of fold_1 if items per fold is 50, else go in train
        #print("new-----");
        #print("f_i : ", file_index);
        #print("l_i : ", line_index);
        #print("l_i = ", line_index, " -> ", np.floor(line_index / items_per_fold) );
        #line = str(line_index);
        test_class = int(np.floor(line_index / items_per_fold));
        #print("test_class : ", test_class);
        if(test_class == file_index):
            a_file["test"].write(line);
        else:
            a_file["train"].write(line);

f.close();
#print(the_data);
#print(len(the_data));
##print("End loading data...");
print("End.");


def extract_based_on_ids(dataset, id_file):
	lines = []
	with open(id_file) as f:
		for line in f:
			id = line.strip()
			try:
				lines.append(dataset[id])
			except:
				print >> sys.stederr, 'ERROR: Invalid ID %s in %s' % (id, id_file)
	return lines

def create_dataset(lines, output_fname):
	f_write = open(output_fname, 'w')
	f_write.write(dataset['header'])
	for line in lines:
		f_write.write(line.decode('cp1252', 'replace').encode('utf-8'))

def collect_dataset(input_file):
	dataset = dict()
	lcount = 0
	with open(input_file) as f:
		for line in f:
			lcount += 1
			if lcount == 1:
				dataset['header'] = line
				continue
			parts = line.split('\t')
			assert len(parts) >= 6, 'ERROR: ' + line
			dataset[parts[0]] = line
	return dataset

dataset = collect_dataset(args.input_file)
for fold_idx in xrange(0, 5):
	for dataset_type in ['dev', 'test', 'train']:
		lines = extract_based_on_ids(dataset, 'fold_%d/%s_ids.txt' % (fold_idx, dataset_type))
		create_dataset(lines, 'processed/fold_%d/%s.tsv' % (fold_idx, dataset_type))

'''
