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

logger = logging.getLogger(__name__)

score_ranges_by_essay_set = {
	1: (2,12),
	2: (1,6), # note, this only utilizes the first score domain.
	3: (0,3),
	4: (0,3),
	5: (0,4),
	6: (0,4),
	7: (0,30),
	8: (0,60)
}

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
    ##    b. tokenize text
    ##  2. score processing
    ##    a. normalize scores
    ##  3. strip irrelevant fields

    ## 1.a. build vocab based on training data (use nltk)
    logger.info('    building vocabulary from training data...');
    options_dict = dict({
        "to_lower": False,
        "vocab_size" : False,
    });
    options_encoding = hashlib.sha1(json.dumps(options_dict, sort_keys=True)).hexdigest()  ## used to encode selected options into filename: ensures that if options are changed we use a cache for that option set
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
        vocab, statistics = build_vocab(raw_data["header"], raw_data["train"], options_dict);
        logger.info('        caching vocab....');
        utils.cache.save_to_cache(cleaned_file_name + "-" + options_encoding, [vocab, statistics]);

    logger.info('        %i total words, %i unique words' % statistics);
    print ("here i am!");
    print(vocab["the"]);


    '''
    def get_data(paths, prompt_id, vocab_size, maxlen, tokenize_text=True, to_lower=True, sort_by_len=False, vocab_path=None, score_index=6):
    	train_path, dev_path, test_path = paths[0], paths[1], paths[2]

    	if not vocab_path:
    		vocab = create_vocab(train_path, prompt_id, maxlen, vocab_size, tokenize_text, to_lower)
    		if len(vocab) < vocab_size:
    			logger.warning('The vocabualry includes only %i words (less than %i)' % (len(vocab), vocab_size))
    		else:
    			assert vocab_size == 0 or len(vocab) == vocab_size
    	else:
    		vocab = load_vocab(vocab_path)
    		if len(vocab) != vocab_size:
    			logger.warning('The vocabualry includes %i words which is different from given: %i' % (len(vocab), vocab_size))
    	logger.info('  Vocab size: %i' % (len(vocab)))

    	train_x, train_y, train_prompts, train_maxlen = read_dataset(train_path, prompt_id, maxlen, vocab, tokenize_text, to_lower)
    	dev_x, dev_y, dev_prompts, dev_maxlen = read_dataset(dev_path, prompt_id, 0, vocab, tokenize_text, to_lower)
    	test_x, test_y, test_prompts, test_maxlen = read_dataset(test_path, prompt_id, 0, vocab, tokenize_text, to_lower)

    	overal_maxlen = max(train_maxlen, dev_maxlen, test_maxlen)
    '''
