'''
    This object/package is responsible for:
        1. accessing data from folds (test, train, dev);
        2. converting between normalized and raw essay scores
        3. defining a vocabulary based on the training set
'''
import csv;
import logging

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
            if(i % 1000 == 0): print("reading line " + str(i))
    return data_list;

def build_vocab(header, data, options_dict):
    

def get_data_for_fold(fold_base_path, bool_overwrite_pickle): ## bool_overwrite_pickle enables the automatic cache to be overwritten
    print("retreive dataset from fold base name " + fold_base_path);

    ## retreive raw data
    header = "essay_id,essay_set,essay,rater1_domain1,rater2_domain1,rater3_domain1,domain1_score,rater1_domain2,rater2_domain2,domain2_score,rater1_trait1,rater1_trait2,rater1_trait3,rater1_trait4,rater1_trait5,rater1_trait6,rater2_trait1,rater2_trait2,rater2_trait3,rater2_trait4,rater2_trait5,rater2_trait6,rater3_trait1,rater3_trait2,rater3_trait3,rater3_trait4,rater3_trait5,rater3_trait6";
    header = header.split(","); ## TODO - retreive header from a file (it may change if we make the create_folds.py functionality more advanced or deal with different data)
    raw_data = dict({
        #"train" : retreive_data_from_fold_part(fold_base_name, "train"),
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
    options_dict = dict({
        "to_lower": False,
        "vocab_size" : False,
    });
    vocab = build_vocab(raw_data[header], raw_data[train], options_dict);

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
