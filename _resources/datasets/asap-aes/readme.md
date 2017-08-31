https://www.kaggle.com/c/asap-aes/data

:Code for evaluation metric and benchmarks = https://github.com/benhamner/asap-aes



For this competition, there are eight essay sets. Each of the sets of essays was generated from a single prompt. Selected essays range from an average length of 150 to 550 words per response. Some of the essays are dependent upon source information and others are not. All responses were written by students ranging in grade levels from Grade 7 to Grade 10. All essays were hand graded and were double-scored. Each of the eight data sets has its own unique characteristics. The variability is intended to test the limits of your scoring engine's capabilities.

The training data is provided in three formats: a tab-separated value (TSV) file, a Microsoft Excel 2010 spreadsheet, and a Microsoft Excel 2003 spreadsheet.  The current release of the training data contains essay sets 1-6.  Sets 7-8 will be released on February 10, 2012.  Each of these files contains 28 columns:

essay_id: A unique identifier for each individual student essay
essay_set: 1-8, an id for each set of essays
essay: The ascii text of a student's response
rater1_domain1: Rater 1's domain 1 score; all essays have this
rater2_domain1: Rater 2's domain 1 score; all essays have this
rater3_domain1: Rater 3's domain 1 score; only some essays in set 8 have this.
domain1_score: Resolved score between the raters; all essays have this
rater1_domain2: Rater 1's domain 2 score; only essays in set 2 have this
rater2_domain2: Rater 2's domain 2 score; only essays in set 2 have this
domain2_score: Resolved score between the raters; only essays in set 2 have this
rater1_trait1 score - rater3_trait6 score: trait scores for sets 7-8
 

The validation set and the test set will not be released until February 10, 2012 and April 23, 2012, respectively. The validation and test files each have 6 columns:
 

essay_id: A unique identifier for each individual student essay
essay_set: 1-8, an id for each set of essays
essay: The ascii text of a student's response
domain1_predictionid: A unique prediction_id that corresponds to the predicted_score on the essay for domain 1; all essays have this
domain2_predictionid: A unique prediction_id that corresponds to the predicted_score on the essay for domain 2; only essays in set 2 have this
 

The sample submission files will be released along with their corresponding (validation and test) data sets. The sample submission files have 5 columns:
 

prediction_id: A unique identifier for the score prediction, corresponding to the domain1_predictionid or domain2_predictionid columns
essay_id: A unique identifier for each individual student essay
essay_set: 1-8, an id for each set of essays
prediction_weight: This identifies how the prediction is weighted when the mean of the transformed quadratic weighted kappas is taken.  For essay set 2, which is scored in two domains, this is 0.5 so that each essay contributes equally to the final score.  For the remaining essay sets, this is 1.0.
predicted_score: This is the score output by your automated essay scoring engine for the specific essay and domain
 

In addition, a Microsoft Word 2010 Readme file describes each essay set. The Readme file contains the prompt that the essays in the data file were generated from. If applicable, the Readme file also includes the source information for essays that required students to read and respond to an excerpt.
6 of the 8 essay sets were transcribed, and may contain transcription errors. The instructions for transcribers are included in the Essay_Set_Descriptions.zip file. There are cases in the training set that contain ???, "illegible", or "not legible" on some words. You may choose to discard them if you wish, and essays with illegible words will not be present in the validation or test sets.
Anonymization

We have made an effort to remove personally identifying information from the essays using the Named Entity Recognizer (NER) from the Stanford Natural Language Processing group and a variety of other approaches. The relevant entities are identified in the text and then replaced with a string such as "@PERSON1."

The entitities identified by NER are: "PERSON", "ORGANIZATION", "LOCATION", "DATE", "TIME", "MONEY", "PERCENT"

Other replacements made: "MONTH" (any month name not tagged as a date by the NER), "EMAIL" (anything that looks like an e-mail address), "NUM" (word containing digits or non-alphanumeric symbols), and "CAPS" (any capitalized word that doesn't begin a sentence, except in essays where more than 20% of the characters are capitalized letters), "DR" (any word following "Dr." with or without the period, with any capitalization, that doesn't fall into any of the above), "CITY" and "STATE" (various cities and states).

Here are some hypothetical examples of replacements made:

"I attend Springfield School..." --> "...I attend @ORGANIZATION1"
"once my family took my on a trip to Springfield." --> "once my family took me on a trip to @LOCATION1"
"John Doe is a person, and so is Jane Doe. But if I talk about Mr. Doe, I can't tell that's the same person." --> "...@PERSON1 is a person, and so is @PERSON2. But if you talk about @PERSON3, I can't tell that's the same person."
"...my phone number is 555-2106" --> "...my phone number is @NUM1"
Any words appearing in the prompt or source material for the corresponding essay set were white-listed and not anonymized.
