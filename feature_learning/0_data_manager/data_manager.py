'''
    This object is responsible for:
        1. accessing data from folds (test, train, dev);
        2. converting between normalized and raw essay scores
        3. defining a vocabulary based on the training set
'''


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
