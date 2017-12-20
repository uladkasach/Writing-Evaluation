#### Data and Data Pre-processing
Source: ASAP-AES dataset
    - essay id, essay_set_id, text, [...non-normalized-scores...]
    - some scores graded out of 12, some out of more, some out of less
Pre-processing
    - normalize scores from 0 to 1
        - creates a more continuous label to predict

#### Vectorization Methods
(note, for each method vectorization can be conducted with essay fragments or sentence fragments)

1. baselines
    1. tf-idf -> SVD : LSA (baseline)
    2. wordvector averages (baseline 2)
2. syntactic hypothesis
    1. intra-sentence similarities
        - up to 5th order
    2. across punctuation similarity
        - commas
        - period / sentence end
    3. parse_tree similarity statistics
        - Adj-N
        - Adv-V
3. vector-cluster based vectors
    - takes prior vectors and clusters them, then generates results based on the cluster data
    1. k-sparce
    2. k-dense


#### Statistical Analysis of Syntactic Hypothesis features
Before testing the vectors the features were analyzed to see whether the values they produced between good essays (80%+) and bad essays (40%-) differed. It was also relevant to note whether or not the metrics themselves differed on a given dataset (recorded different information) or whether they were highly correlated.

1. intra-sentence-similarities

2. across punctuation

3. parse_tree
(!) note significant difference between metrics, however.

#### Regression Results
1. baselines
2. syntactic hypothesises
3. vector-cluster augmentation


#### Possible forward directions
- test syntactic hypothesis with embeddings that better capture syntax
    - http://www.cs.cmu.edu/~lingwang/papers/naacl2015.pdf
- consider methods to take advantage of the parse_tree similarity statistic metrics
    - due to the strong difference between the two measures
- learn features for each type of essay (good, bad, neutral) individually
    - paper 1 (wordvector autoencoder)
    - autoencoder of other features
- attempt to understand why clusters for lsa are more seperated in terms of score than semantic clusters but still perform equally or worse. See https://github.com/uladkasach/Writing-Evaluation/issues/39#issuecomment-344960505
