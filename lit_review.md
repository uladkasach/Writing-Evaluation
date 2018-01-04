
#### [1] Handbook of Automated Essay Evaluation: Current Applications and New Directions
- Overview book on AES techniques
- https://books.google.com/books?id=SvNnPeYAUPcC&dq=Asap+aes+essay+scoring&lr=
- Authors: Mark D. Shermis, Jill Burstein

#### [2] Flexible Domain Adaptation for Automated Essay Scoring Using Correlated Linear Regression
- http://www.aclweb.org/anthology/D15-1049
- Problem: Performance across prompt domains is poor, and good performance requires manual grading of new prompts (Expensive)
- Solution: domain adaptation. includes new domain adaptation technique: Bayesian linear ridge regression
- Shown: competitive results for domain adaptation
- references [1] as a good resource
- lit review (**problem approaches**):
    - regression interpretation
        - PEG (Page, 1994) lots of features + regression
        - e-rater (Attali and Burstein, 2004) uses NLP to generate smaller # of complex features + step wise regression
    - classification interpretation
        -  (Larkey,1998)
        -  (Rudner and Liang, 2002) - Bayesian models for classification, treates AES as text classification problem
        - Intelligent Essay Assessor (Landauer et al., 1998) uses  Latent Semantic Analysis (LSA) to measure similarity between essays
    - performance ranking interpretation
        - (Yannakoudakis et al., 2011)
        - (Chen and He, 2013).
- This work
    - **problem approach: regression**
    - regression interpretation: *"We use regression
    because the range of scores of the essays
    could be very large and a classification approach
    does not work well in this case. It also allows us to
    model essay scores as continuous values and scale
    them easily in the case of different score ranges
    between the source essay prompt and the target essay
    prompt"*
        - i.e. scores can have a more continuous nature
- **Features** used:
    - "simple" : "e.g., word length, essay length, etc"
    - "complex" : "e.g., grammatical errors"
    - generated by EASE - winners of the AES-ASAP competition
        - https://github.com/edx/ease
        - NLTK for POS tagging and stemming
            - tags generated on gramatically correct text provided externally
            - *"The POS tag sequences not included in the correct
            POS tags are considered as bad POS."*
        - aspell for spellchecking
        - WordNet for synonmys
        - skikit-learn for unigram and bigram features
    - all features outlined in table 1
- **Dataset**: AES-ASAP
    - note the features/properties of each prompt type
- **Eval Metric**: Quadratic weighted Kappa (QWK)
- Bayesian linear ridge regression: domain adaptation / transfer learning specific.

#### [3] When “the state of the art” is counting words
http://lesperelman.com/wp-content/uploads/2015/09/Perelman-State-of-the-Art-is-Counting-Words.pdf

demonstrates that the "state of the art" (2014) in aes systems consistently overweigh wordcount as a feature, in comparison to human scorers, particularly pointint out [4]'s conclusions as incorrect

Points of interest:
- Motivation for AES comes from increased focus of standardized testing w/ essays
- presents 3 data sources

#### [4] State-of-the-art automated essay scoring: Competition, results, and future directions from a United States demonstration
- https://assets.documentcloud.org/documents/1094637/shermis-aw-final.pdf
- Author: Mark D. Shermis (same as [1])
    - dept's of education and psychology
- references [1]
- evaluates performance of several different "state of the art" AES systems
- no analysis of algorithms or ml methods

#### [5] A Ranked-Based Learning Approach to Automated Essay Scoring
- http://ieeexplore.ieee.org/abstract/document/6382855/
    - no pdf
- Authors:  Hongbo Chen ;  Ben He ;  Tiejian Luo ;  Baobin Li
    - Beijing
- 2012
- "Lit Review" techniques applied
    - K-nearest-neighbor (KNN)
    - multiple linear regression
- approaches problem as ranking Problem
- states that performance exceeds traditional ml approaches
- feature extraction and scoring details in pdf (claimed)
    - **could be relevant**


#### [6] An Integrated Framework for the Grading of Freeform Responses
- https://linc.mit.edu/linc2013/proceedings/Session3/Session3Mit-Par.pdf
- Authors: Piotr F. Mitros, Vikas Paruchuri, John Rogosic, Diana Huang
    - EECS MIT
- Application/Motivation: essay scoring for MOOCS
- involves self assessment, peer assessment, and AI assessment
- mentions:
    - iterative improvement of model when people label predictions it was not confident about
- utilizes AES developed by the VikP & jman team for AES competition on kaggle
    - https://www.kaggle.com/c/asap-aes

#### [7] Effective sampling for large-scale automated writing evaluation systems
- Nicholas Dronen, Peter W. Foltz, and Kyle Habermehl
    - Boulder, CO
- *"show how to minimize training set
sizes while maximizing predictive performance, thereby reducing cost without unduly
sacrificing accuracy."*
- **dataset eda**: does good job describing kaggle dataset
- **modeling: regression - for training example selection**
- regression modeling approach
    - regularized regression rather than ordinary least squares
- idea: find m out of n essays that maxmimize performance of training when labeled and trained upon
    - effective sampling of training data
    - fundamental idea: the greater the distance between the x values, the greater the probability that the model will perform almost as well as one trained with all of the data.

#### [8] Task-Independent Features for Automated Essay Grading
- http://www.aclweb.org/anthology/W/W15/W15-06.pdf#page=240
- Torsten Zesch Michael Wojatzki
- problem: supervised learning makes it complicated to transfer a system trained on one task to another
- solution: find features not dependent on essay task + useful for transfer learning
- points out degree of dependency of features on task domain in aes
    - strongly dependent:  detect important words or topics (Chen and He, 2013)
    - not very dependent: number of words in the essay(Östling, 2013; Lei et al., 2014), usage of connectors (Burstein and Chodorow, 1999; Lei et al., 2014)
- Tests hypothesis that task-independent features can capture most of the inportant information, evaluates how much information is lost w/ task-independent features
- Main Relevancy **evaluates features**
- ** Features ** Discusses "state of the art" features and labels task dependent/independent
    - Length Features:
        - essay length  (Mahana et al., 2012; Chen and He, 2013; Östling, 2013; Lei et al., 2014),  (Shermis and Burstein,2002).
        - avg sentence and word length ((Attali and Burstein, 2006; Mahana et al., 2012; Chen and He, 2013; Östling, 2013).)
    - Occurrence Features:
        - punctuation (Mahana et al. (2012))
        - formal references ((Bergler, 2006)), (Krestel et al. (2008))
        - core concepts (Foltz et al., 1999).
    -  Syntax Features
        - ((Burstein et al., 1998).),
        - distinct trees to all trees ratios (Chen and He (2013),)
        - average tree depth (Chen and He (2013),)
        - clauses (subordinate, causal and temporal clauses)
            -  (Burstein et al., 1998; Chen and He, 2013; Lei et al., 2014).
    - Style Features
        - relative ratio of POS tag usage (Östling (2013)) for writer preference
        - formality of writing feature ((Heylighen and Dewaele, 2002)) (**interesting**)
        - "type-token-ratio" for distinguishing rich -vs- poor vocabulary (Chen and He (2013))
        - word knowledge: correlates word knowledge to frequency (Breland et al. (1994))
    - Cohesion Features
    -  Coherence Features
    - Error Features
    -  Readability Features
    -  Task-Similarity Features
    - Set-Dependent Features
- ** Datasets**
    - ASAP-AES (kaggle)
        - good description of the essay prompts
    - german essayset
- **performance measure** : quadratic weighted kappa
- *** (!) a big takeaway idea*** : opinion -vs- source based prompts have different transferability measures

#### [9] A Neural Approach to Automated Essay Scoring
- http://www.aclweb.org/old_anthology/D/D16/D16-1193.pdf
- Kaveh Taghipour and Hwee Tou Ng
    - singapore
- 2016
- problem: most AES systems rely on ad-hoc created features
    - not scalable, expensive
- solution: recurrent neural network to learn relationship without feature engineering
- NN's: *"based on continuous-space representation of the input and non-linear functions"*
- *"SENNA (Collobert et al., 2011) and neural machine
translation (Bahdanau et al., 2015) are two notable
examples in natural language processing that operate
without any external task-specific knowledge"*
- leverage " modeling capacity and generalizability" of neural networks
- Benefit: this model LEARNS features (Representations) rather than having carefully crafted features it trains on
- Acheives state of the art performance
    - example code is available
- references [8] for description of handcrafted features used in state of art so far
- uses **recurrent neural network** to: 1. learn features, 2. score - simultaneously
- Model structure
    - input: sequence of one hot vectors
    - lookup table layer (converts one hots into word vectors) -- *learned*
    - OPTIONAL - convolution layer after "lookup table layer"
        - *note potential problem* - convolution eliminates sequence information
            - e.g., it'll pick out features regardless of their position in the input
        - their idea: can generate n-grams and capture context
    - recurrent layer
        - encodes full essay
        - keeps intermediate steps as well
        - attempted regular RNN, Gated, and LSTM: LSTM had best performance
    - mean over time layer
        - utilizes both the final and intermediate steps of the LSTM
            - increases performance (*intersting*)
        - outputs a vector representation of the essay
    - linear layer w/ sigmoid activation
        - regression
- training
    - minimize MSE
    - RMSProp optimization algorithm
    - dropout regularization to avoid overfitting    
    - clip the gradient if norm past threshold
    - no early stopping
- Evaluation   
    - pick model with best QWK and score the dev set
    - Compares results with EASE (state of the art for AES-ASAP dataset, won competition, other papers do similar)
- results  
    - beats EASE w/ statistical significance by significant margin
- additionally experiemented with "ATTENTION" layer


#### [10] Automated Essay Grading Using Machine Learning
- https://pdfs.semanticscholar.org/100a/d305019abc9510687339eabb5097a3a70caf.pdf
- Manvi Mahana, Mishel Johns, Ashwin Apte
    - Stanford Students
- handcrafted features
- linear regression applied on features
- forward feature selection algorithm to find best combination of features

#### [11] Automatically Scoring Freshman Writing: A Preliminary Investigation
- https://www.aclweb.org/anthology/W/W15/W15-0629.pdf
- Courtney Napoles and Chris Callison-Burch
    - U of Penn and John Hopkins
- new dataset
    - Freshman Writing Corpus (FWC)
- multi-task learning focus
- gender bias removal
- transfer leraning component
- **features**: hand made
    - Surface features, Structural features, Lexical features, Syntactic features, Grammatical features


#### [12] The Joint Student Response Analysis and Recognizing Textual Entailment Challenge: making sense of student responses in educational applications
- http://www.cse.unt.edu/~nielsen/papers/JLRE16_JointSRAandRTEChallenge.pdf
- focuses on more challenging short answer area where semantics are more important

#### [13] The Eras and Trends of Automatic Short Answer Grading
- Steven Burrows Iryna Gurevych Benno Stein
- https://link.springer.com/article/10.1007/s40593-014-0026-8
- 2014 book over AES

#### [14] Constrained Multi-Task Learning for Automated Essay Scoring
- 2016
- addresses training of a general model that performs well across domains (across different prompts)
- ** features ** : hand crafted
    - 1. word unigrams, bigrams, and trigrams 2. POS (part-of-speech) counts 3. essay length (as the number of unique words) 4. GRs (grammatical relations) 5. max-word length and min-sentence length 6. the presence of cohesive devices 7. an estimated error rate
    - "those identified in previous works"  (Yannakoudakis et al., 2011; Phandi et al., 2015)