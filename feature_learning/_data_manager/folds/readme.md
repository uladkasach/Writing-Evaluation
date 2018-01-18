As can be seen in the summary_description.png image ( see directory  `../raw/`) the essays can be grouped as persuasive (1&2), source (3-6), and narrative (7&8). It is easy to see even from just the word counts that these different types are more similar to them selfs than others. Therefore it makes sense to train the feature learning algorithm on each separately.

In the future, perhaps a transfer learning approach can be utilized in that the model is fine tuned on each respective set later on.


Example usage:
```
python create_folds.py -i ../raw/training_set_rel3.csv -s 3456
```
