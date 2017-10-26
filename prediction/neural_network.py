###########################################################
## Modules for Training
############################################################
import tensorflow as tf
import numpy as np
import pandas as pd
import sys
import os
import time

import plac;
import csv;
import json;


class Batch_and_Shuffler:
    def __init__(self, labels, features):
        self.features = features;
        self.labels = labels;
        self.index = 0;
        self.shuffle_data();

    def shuffle_data(self):
        #print("Shuffling data!");
        # shuffles data while keeping labels and features in order with eachother

        data = self.features;
        labels = self.labels;

        idx = np.arange(0 , len(data))
        np.random.shuffle(idx)
        data_shuffle = [data[ i] for i in idx]
        labels_shuffle = [labels[ i] for i in idx]

        self.features = data_shuffle;
        self.labels = labels_shuffle;

    def get_new_batch(self, batch_size = 128):
        features = [];
        labels = [];
        while(len(labels) < batch_size):
            if(self.index >= len(self.labels)):
                self.shuffle_data(); ## shuffle data if we get to end of data
                self.index = 0;
            features.append(self.features[self.index]);
            labels.append(self.labels[self.index]);
            self.index += 1;
        return labels, features;

    def get_all(self):
        self.shuffle_data();
        return self.labels, self.features;


class Neural_Network_Model:
    ## TODO - handle arbitrary len hidden layers in a better way, perhaps try Keras so as to not recreate the wheel, https://machinelearningmastery.com/regression-tutorial-keras-deep-learning-library-python/
    def __init__(self, n_hidden_1, n_hidden_2):
        self.method = "REGRESSION";
        self.nodes = dict({
            "h1" : n_hidden_1,
            "h2" : n_hidden_2,
        });

    def multilayer_perceptron_calculations(self, x, weights, biases): ## this function conducts the actual calculations required for the neural entwork
        # Hidden layer with RELU activation
        layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
        layer_1 = tf.nn.relu(layer_1)
        # Hidden layer with RELU activation
        layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
        layer_2 = tf.nn.relu(layer_2)
        # Output layer with linear activation
        out_layer = tf.matmul(layer_2, weights['out']) + biases['out']
        return out_layer

    def build_graph_and_start_session(self, n_classes, n_input, learning_rate = 0.5):
        ###################################
        # tf Graph input
        ###################################
        x = tf.placeholder(tf.float32, [None, n_input]) ## Features
        y = tf.placeholder(tf.float32, [None, n_classes]) ## True Values

        ###################################
        # Define weight matricies & bias vectors for each layer
        ###################################
        weights = {
            'h1': tf.Variable(tf.random_normal([n_input, self.nodes["h1"]])),
            'h2': tf.Variable(tf.random_normal([self.nodes["h1"], self.nodes["h2"]])),
            'out': tf.Variable(tf.random_normal([self.nodes["h2"], n_classes]))
        }
        biases = {
            'b1': tf.Variable(tf.random_normal([self.nodes["h1"]])),
            'b2': tf.Variable(tf.random_normal([self.nodes["h2"]])),
            'out': tf.Variable(tf.random_normal([n_classes]))
        }

        ###################################
        # Construct model
        ###################################
        pred = self.multilayer_perceptron_calculations(x, weights, biases)
        ## perc_pred = tf.nn.softmax(pred); softmax not needed for regression

        #########
        # Define loss and optimizer
        ##########
        cost = tf.sqrt(tf.reduce_mean(tf.square(tf.subtract(pred, y)))) ## RMSE
        train_step = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost) ## ADAM optimizer for learning


        ##########
        ## define graph initialization
        ##########
        init = tf.global_variables_initializer() ##  Define Initialization function for variables/ops

        ##########
        ## define and cache the session
        ##########
        sess = tf.Session();
        sess.run(init);

        self.graph = dict({
            "x": x,
            "y": y,
            "weights": weights,
            "biases": biases,
            "pred": pred,
            "cost": cost,
            "train_step": train_step,
            "session" : sess,
        })
        return True;



    def predict(self, features):
        return False; ## TODO - just return the pred graph

    def test(self, labels, features):
        cost = self.graph["cost"];
        x = self.graph["x"];
        y = self.graph["y"];
        sess = self.graph["session"];

        print("RMSE for test data :", end = '');
        final_cost_found = sess.run(cost, feed_dict={x: features, y : labels});
        print (final_cost_found);



    def train(self, labels, features, epochs = 100, njobs = 1):
        ###################################
        # Build Graph and Initialize Session
        ###################################
        feature_count = features.shape[1];
        label_count = labels.shape[1] if len(labels.shape) > 1 else 1;
        self.build_graph_and_start_session(label_count, feature_count);

        ###################################
        # define data handler
        ###################################
        training_data_handler = Batch_and_Shuffler(labels, features);

        #################################################################
        ## Train Model
        #################################################################
        cost = self.graph["cost"];
        train_step = self.graph["train_step"];
        x = self.graph["x"];
        y = self.graph["y"];
        sess = self.graph["session"];

        display_ratio = 200;

        for i in range(epochs):
            batch_labels, batch_features = training_data_handler.get_new_batch(batch_size = 2000);

            if(i == 0):
                start_time = time.time()
                print ('Init Cost : ', end = '');
                print (sess.run(cost, feed_dict={x: batch_features, y : batch_labels}));

            if(i % (epochs/display_ratio) == 0 and i != 0):
                end_time = time.time();
                print ('Epoch %6d' % i, end = '');

                print(' ... cost : ', end = '');
                this_cost = (sess.run(cost, feed_dict={x: batch_features, y : batch_labels}));
                print ('%10f' % this_cost, end = '');

                print (',  = RMSE  : ', end = '');

                print (',  dt : ', end = '');
                delta_t = end_time - start_time;
                print ('%10f' % delta_t, end = '');

                print('');

                #print("Pred -vs- Label:");
                #print(sess.run(pred[0:10],  feed_dict={x: batch_feature, y : batch_label}));
                #print(batch_label[0:10]);

                start_time = time.time()

            sess.run(train_step, feed_dict={x: batch_features, y : batch_labels})

        print ('Final Cost : ', end = '');
        batch_labels, batch_features = training_data_handler.get_all();
        final_cost_found = sess.run(cost, feed_dict={x: batch_features, y : batch_labels});
        print (final_cost_found);



def load_data(source_file):
    ## read all lines
    features = [];
    labels = [];
    header_list = ["essay_id", "essay_set", "score"]
    with open(source_file, "r") as f:
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            #if(i>10000): break;
            these_features = line[3:]; ## 3 labels, rest is features
            this_label = [line[2]]; ## score
            #print(this_label);
            #print(these_features);
            features.append(these_features);
            labels.append(this_label);
            if(i % 1000 == 0): print("reading line " + str(i))
            #if(i>1000): break;
    return labels, features;



@plac.annotations(
    source_file=("Path to source file"),
    n_jobs=("Number of Jobs (Default : 1)", "option", "k", int),
    n_hidden_1=("Number of nodes in hidden layer 1 (Default: 10)", "option", "n1", int),
    n_hidden_2=("Number of nodes in hidden layer 2 (Default: 1)", "option", "n2", int),
    epochs = ("Number of epochs to train (Default: 100)", "option", "e", int)
)
def main(source_file, n_jobs, n_hidden_1, n_hidden_2, epochs):
    ## define defaults
    if(n_jobs is None): n_jobs = 1;
    if(n_hidden_1 is None): n_hidden_1 = 10;
    if(n_hidden_2 is None): n_hidden_2 = 1;
    if(epochs is None): epochs = 10;

    base_file_name = ".".join(source_file.split("/")[-1].split(".")[:-1]); # retreive file name w/o extension

    ## load data
    print("loading data...");
    labels, features = load_data(source_file);
    labels = np.array(labels);
    features = np.array(features);
    total_count = len(labels);

    ## split data naively
    print("splitting data into test and train...");
    train_count = int(total_count*3/float(4));
    train_labels = labels[:train_count];
    test_labels = labels[train_count:];
    train_features = features[:train_count];
    test_features = features[train_count:];
    print(epochs);

    print("training model on training data...");
    model = Neural_Network_Model(n_hidden_2, n_hidden_1)
    model.train(train_labels, train_features, epochs = epochs);

    print("evaluating model on test data...")
    print(test_labels.shape)
    model.test(test_labels, test_features);


if __name__ == '__main__':
    plac.call(main)
