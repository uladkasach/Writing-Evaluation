'''
    This object/package is responsible for:
        1. accessing data from folds (test, train, dev);
        2. converting between normalized and raw essay scores
        3. defining a vocabulary based on the training set
'''
import csv;
import logging;
import nltk;
import re;
import operator;
import _utilities as utils;
import hashlib;
import json;
import collections;
import numpy as np;

logger = logging.getLogger(__name__)

score_ranges_by_essay_set = { ## this defines the range of domain_1 scores for each essay set
	1: (2,12),
	2: (1,6),
	3: (0,3),
	4: (0,3),
	5: (0,4),
	6: (0,4),
	7: (0,30),
	8: (0,60)
}

def convert_scores_to(to_what, orig_scores, essay_sets):
    def to_raw(orig_score, scale, base):
		return orig_score * scale + base ## orig_score * scale - base
    def to_norm(orig_score, scale, base):
        return (orig_score - base) / float(scale);
    def convert_this_score(orig_score, essay_set):
        assert essay_set in score_ranges_by_essay_set; ## ensure essay_set is valid
    	low, high = score_ranges_by_essay_set[essay_set];
        scale = high - low;
        base = low;
        assert to_what in ["raw", "norm"]; ## ensure to_what is valid
        if(to_what == "raw"):
            score = to_raw(orig_score, scale, base);
            assert score >= low and score <= high; ## ensure that final score is valid logically
        elif(to_what == "norm"):
            score = to_norm(orig_score, scale, base);
            assert score >= 0 and score <= 1;
        return score;

    ## normalize the input
    assert type(orig_scores) in {int, float, np.ndarray, list}; ## ensure that orig_score is either a float or a list of floats
    assert type(essay_sets) in {int, np.ndarray, list}; ## ensure that essay set is either an int or a list of ints
    originally_single_value = False;
    if(type(essay_sets) == int): ## if its a single element, then cast both into a list to interpret in a general way
        orig_scores = [orig_scores];
        essay_sets = [essay_sets];
        originally_single_value = True;
    orig_scores = np.array(orig_scores); ## ensure orig_scores are  np.array
    essay_sets = np.array(essay_sets); ## ensure essay_set are np.array
    assert orig_scores.shape[0] == essay_sets.shape[0] ## ensure scores and essay_set ids are same size
    data_matrix = np.column_stack([orig_scores, essay_sets]); ## convert into "tuples" on each row of a n by 2 matrix

    ## generate list of converted scores
    scores = [];
    for row in data_matrix:
        orig_score, essay_set = row;
        score = convert_this_score(orig_score, essay_set);
        logger.debug(score);
        scores.append(score);

    ## return data
    if(originally_single_value): ## ensure that if only one score was provided originally (not a list) to output a socre, not a list
        scores = scores[0];
    return scores;



def retreive_data_from_fold_part(fold_base_path, part_type):
    input_file = fold_base_path+"."+part_type+".csv";

    header_list = None;
    data_list = [];
    with open(input_file, "rb") as f:
        reader = csv.reader(f); ## note, this automatically converts lines into lists
        for i, line in enumerate(reader):
            data_list.append(line);
            if(i % 1000 == 0): logger.debug("reading line " + str(i))
    return data_list;


def tokenize(string):
    string = string.decode('utf-8').strip();
    tokens = nltk.word_tokenize(string);
    print_output = False;
    for index, token in enumerate(tokens):
    	if token == '@' and (index+1) < len(tokens):
            tokens[index+1] = '@' + re.sub('[0-9]+.*', '', tokens[index+1]) ## strings like "@NUM2" are cast into tokens "@", "NUM2" and should be recast into "@NUM".
            tokens.pop(index)
    return tokens
def build_vocab(header, dataset, options_dict):
    total_words, unique_words = 0, 0;
    word_freqs = dict();

    for index, essay_data in enumerate(dataset):
        content = essay_data[header.index("essay")];
        if(options_dict["to_lower"]): content = content.lower();
        tokens = tokenize(content); ## tokenize the essay content string
        for word in tokens: ## count statistics and build frequency dict
            if(word not in word_freqs):
                word_freqs[word] = 0;
                unique_words += 1;
            word_freqs[word] += 1;
            total_words += 1;
        if(index % 1000 == 0): logger.debug("vocabing line " + str(index));


    sorted_word_freqs = sorted(word_freqs.items(), key=operator.itemgetter(1), reverse=True) ## sort the frequency dict into tuple with frequency descending

    vocab = {'<pad>':0, '<unk>':1, '<num>':2}
    base_vocab_length = len(vocab);
    for index, tuple in enumerate(sorted_word_freqs): ## add each word to vocab dictionary, define its unique id by order in sorted word freqs list
        word, _ = tuple;
        vocab[word] = index + base_vocab_length;

    statistics = (total_words, unique_words);

    return vocab, statistics;
def generate_vocab(raw_data, fold_base_path, bool_overwrite_pickle): ## either builds or retreives from cache
    ## 1.a. build vocab based on training data (use nltk)

    text_options_dict = dict({ ## TODO - implement to_lower and vocab size functionality. Will need to reflect to_lower in cleanse_raw_data tokenization
        "to_lower": False,
        "vocab_size" : False,
    });

    logger.info('    building vocabulary from training data...');
    options_encoding = hashlib.sha1(json.dumps(text_options_dict, sort_keys=True)).hexdigest()  ## used to encode selected options into filename: ensures that if options are changed we use a cache for that option set
    cleaned_file_name = fold_base_path.replace("/", "__");

    create_vocab = False; ## evaluate whether or not to create the vocab or just load it from cache
    if(bool_overwrite_pickle):
        create_vocab = True;
    else:
        try:
            vocab, statistics = utils.cache.retreive_from_cache(cleaned_file_name + "-" + options_encoding);
        except IOError:
            logger.info('        vocab does not exist in cache...');
            create_vocab = True;

    if(create_vocab): ## create the vocab if needed based on previous logic
        logger.info('        creating vocab...')
        vocab, statistics = build_vocab(raw_data["header"], raw_data["train"], text_options_dict);
        logger.info('        caching vocab....');
        utils.cache.save_to_cache(cleaned_file_name + "-" + options_encoding, [vocab, statistics]);

    logger.info('        %i total words, %i unique words' % statistics);
    return vocab;

def cleanse_this_essay(essay_data, header, vocab):
    ## initialize cleansed data w/ base data
    essay_id = int(essay_data[header.index("essay_id")]);
    essay_set = int(essay_data[header.index("essay_set")]);
    cleansed_data = dict({
        "essay_id" : essay_id,
        "essay_set": essay_set,
    })

    ## 2.a tokenize text (based on vocab);
    stats = dict({
        "total" : 0,
        "num" : 0,
        "unk" : 0,
    })
    raw_text = essay_data[header.index("essay")];
    tokenized_text_pre_vocab = tokenize(raw_text);
    tokenized_indicies = [];
    for token in tokenized_text_pre_vocab:
        if token.replace('.','',1).isdigit():## if the token is a number, replace it with index of <num>
            tokenized_indicies.append(vocab["<num>"]);
            stats["num"] += 1;
        elif token in vocab: ## else if its in vocabulary, replace with index (put after number check since we dont remove number tokens in vocabulary building as it would require us to check if its numeric twise)
            tokenized_indicies.append(vocab[token]);
        else:
            tokenized_indicies.append(vocab["<unk>"]);
            stats["unk"] += 1;
        stats["total"] += 1;
    cleansed_data["essay_tokens"] = tokenized_indicies;

    ## 2.b normalize scores
    raw_score = float(essay_data[header.index("domain1_score")]); ## use domain1_score as score for essay
    normalized_score = convert_scores_to("norm", raw_score, essay_set);
    cleansed_data["raw_score"] = raw_score;
    cleansed_data["norm_score"] = normalized_score;

    return cleansed_data, stats;

def cleanse_raw_data(dataset, header, vocab, type):
    logger.info("    cleansing raw " + type + " data (tokenization and score normalization)... ")
    ## cleanse each essay data
    stats = dict({
        "total" : 1,
        "num" : 1,
        "unk" : 1,
    })
    cleansed_data = [];
    for essay_data in dataset:
        this_cleansed_data, these_stats = cleanse_this_essay(essay_data, header, vocab);
        cleansed_data.append(this_cleansed_data);
        stats = dict(collections.Counter(stats)+collections.Counter(these_stats)); ## sum stats and these stats by key,  https://stackoverflow.com/a/30950164/3068233

    logger.info('        <num> hit rate: %d (%.2f%%), <unk> hit rate: %d (%.2f%%), of %d' % (stats["num"], 100*stats["num"]/float(stats["total"]), stats["unk"], 100*stats["unk"]/float(stats["total"]), stats["total"]))

    return cleansed_data;

def get_data_for_fold(fold_base_path, bool_overwrite_pickle): ## bool_overwrite_pickle enables the automatic cache to be overwritten
    print("retreive dataset from fold base name " + fold_base_path);
    logger.info('Retreiving dataset from fold base path ' + fold_base_path);

    ## retreive raw data
    logger.info('    loading raw data...');
    header = "essay_id,essay_set,essay,rater1_domain1,rater2_domain1,rater3_domain1,domain1_score,rater1_domain2,rater2_domain2,domain2_score,rater1_trait1,rater1_trait2,rater1_trait3,rater1_trait4,rater1_trait5,rater1_trait6,rater2_trait1,rater2_trait2,rater2_trait3,rater2_trait4,rater2_trait5,rater2_trait6,rater3_trait1,rater3_trait2,rater3_trait3,rater3_trait4,rater3_trait5,rater3_trait6";
    header = header.split(","); ## TODO - retreive header from a file (it may change if we make the create_folds.py functionality more advanced or deal with different data)
    raw_data = dict({
        "train" : retreive_data_from_fold_part(fold_base_path, "train"),
        "tune" : retreive_data_from_fold_part(fold_base_path, "tune"),
        "test" : retreive_data_from_fold_part(fold_base_path, "test"),
        "header" : header,
    })

    ## process data:
    ##  1. text processing:
    ##    a. build vocabulary based on training data
    ##  2. build cleaned data
    ##    a. tokenize text (based on vocab)
    ##    b. normalize scores

    ## 1. text processing
    vocab = generate_vocab(raw_data, fold_base_path, bool_overwrite_pickle);

    ## 2. build cleaned data
    cleaned_data = dict({
        "train" : cleanse_raw_data(raw_data["train"], raw_data["header"], vocab, "train"),
        "tune" : cleanse_raw_data(raw_data["tune"], raw_data["header"], vocab, "tune"),
        "test" : cleanse_raw_data(raw_data["test"], raw_data["header"], vocab, "test"),
        "header" : ["essay_id", "essay_set", "essay_tokens", "raw_score", "normalized_score"],
    })

    return cleaned_data;
