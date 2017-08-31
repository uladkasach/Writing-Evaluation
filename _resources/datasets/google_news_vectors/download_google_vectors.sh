#!/bin/bash

#/var/www/git/Plants/NLP/word2vec/features/embed_import/download_google_vectors.sh

cd /var/www/git/Plants/NLP/word2vec/features/embed_import/;
rm GoogleNews-vectors-negative300.bin.gz;
#wget https://doc-0g-8s-docs.googleusercontent.com/docs/securesc/ha0ro937gcuc7l7deffksulhg5h7mbp1/o2tin09msf2l8dqq8qqfl8cuth1r0vun/1491688800000/06848720943842814915/*/0B7XkCwpI5KDYNlNUTTlSS21pQmM;
wget https://s3.amazonaws.com/mordecai-geo/GoogleNews-vectors-negative300.bin.gz
gunzip -k GoogleNews-vectors-negative300.bin.gz;
#mv 0B7XkCwpI5KDYNlNUTTlSS21pQmM GoogleNews-vectors-negative300.bin;
#sudo pip3 install gensim; # installs it incase it is not there, incease its already there nothing happens.
python3 convert_v2.py;
cp GoogleNews-vectors-negative300.csv /var/www/git/NLP/Word-Subject-Classification/2_classify/0_data_source/GoogleNews-vectors-negative300.csv;