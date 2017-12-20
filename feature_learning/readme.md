### Based on `[9] A Neural Approach to Automated Essay Scoring` from the literature review
- http://www.aclweb.org/old_anthology/D/D16/D16-1193.pdf
- Kaveh Taghipour and Hwee Tou Ng
    - singapore
- 2016

### Questions to answer:
1. to what extent does appending quality hand crafted features (from other literature reviews) increase the performance of the architecture
    - additionally:
        - Which specific features are not captured by the architecture?
        - Why could this be?
        - What could be done to capture these features?

2. would utilizing pre-trained word embeddings as the initial lookup table improve model performance? (i.e., transfer learning)

### Steps:
1. recreate FL and prediction architecture defined in literature
2. evaluate question 1
    - include as inputs the handcrafted features throughout different areas of the pipeline
3. evaluate question 2
