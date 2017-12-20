punct_vs_wordchoice 
    - analyzes consecutive and higher order word similarities -vs- across punctuation word similarities
    - enables analysis with both sence2vec and googlenews vectors
        
        
statistical_analysis
    - break documents down into sentences
    - calculate:
        - across punctuation similarity statistics
            - similarity across sentence ends
            - similarity across commas
        - intra-sentence similarity statistics
            - nth order similarities
            - nth order parse tree similarities
        - basic features
            - sentence length
            - word length
            
            
sentence_feature_extraction
    - tokenize sentences
    - extract features from sentences
        - word choice features
            - n'th order similarities
                - n'th order meaning:
                    - consecutive similarities
                    - first order similarities
                    - second ...
                    etc
            - nth order parse tree based similarities
            - note - all similaity metrics generated will be of variable length, and will need normalized
                - e.g., average, max, min, median, tf-idf weighted average
        - semantic features (converting sentence to vector)
            - compose vectors w/ average, max, min, median, tf-idf weighted average, parse tree based 
        - basic features    
            - sentence length
            - average word length
        
        
NOTE:
    required in each case
    - for each sentence:
        - similarities across comma[s]
        - n'th order similaritie[s]
        - nth order parse tree similaritie[s]
        - sentence length
        - word length[s]
        
        