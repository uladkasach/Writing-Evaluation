
import load_data
import save_data


##########################################################################
## Load Inputs and HPs
##########################################################################
#########################################################
## Update data to arguments
#########################################################
if('name' in arguments):
    delta_mod = arguments['name'];
else:
    print("name is required. Error.");
    exit();
if('source_mod' in arguments):
    source_mod = arguments['source_mod'];
    TRAIN_SOURCE = '../../1_split_data/results/' + source_mod +'_train.csv';
    TEST_SOURCE = '../../1_split_data/results/' + source_mod +'_test.csv';
else:
    print("source_mod is required. Error.");
    exit();
if('rtrue' in arguments): R_True = float(arguments['rtrue']);
if('batch_size' in arguments): batch_size = int(arguments['batch_size']);
if('learning_rate' in arguments): learning_rate = float(arguments['learning_rate']);
if('n_hidden_1' in arguments): n_hidden_1 = int(arguments['n_hidden_1']);
if('n_hidden_2' in arguments): n_hidden_2 = int(arguments['n_hidden_2']);
if('epochs' in arguments): EPOCHS = int(arguments['epochs']);
if('classifier_choice' in arguments):  classifier_choice = (arguments['classifier_choice']);
if('save_training' in arguments and arguments['save_training'] == "true"): save_training = True;



##########################################################################
## Define Model Structure
##########################################################################
###################################
## Data Source Variables / Ops
###################################
feature_batch, label_batch, key_batch = load_data.return_regular_batch([TRAIN_SOURCE], batch_size);
feature_count = feature_batch.shape[1];
label_count = label_batch.shape[1];

###################################
# Network Parameters
###################################
n_input = feature_count
n_classes = label_count

###################################
# tf Graph input
###################################
x = tf.placeholder(tf.float32, [None, feature_count]) ## Features
y = tf.placeholder(tf.float32, [None, label_count]) ## True Values


###################################
# Create model
###################################
def multilayer_perceptron(x, weights, biases):
    # Hidden layer with RELU activation
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    layer_1 = tf.nn.relu(layer_1)
    # Hidden layer with RELU activation
    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    layer_2 = tf.nn.relu(layer_2)
    # Output layer with linear activation
    out_layer = tf.matmul(layer_2, weights['out']) + biases['out']
    return out_layer


###################################
# Store layers weight & bias
###################################
weights = {
    'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])),
    'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_hidden_2, n_classes]))
}
biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'b2': tf.Variable(tf.random_normal([n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_classes]))
}


###################################
# Construct model
###################################
pred = multilayer_perceptron(x, weights, biases)
perc_pred = tf.nn.softmax(pred);
#########
# Define loss and optimizer
##########
class_weights =  tf.constant([R_False, R_True], shape=[2, 1], dtype='float'); #42k total data points, 38k neg, 480 pos
weight_per_label = tf.matmul(y, class_weights);
preweight_cost = tf.nn.softmax_cross_entropy_with_logits(pred, y);
cost_vector = (tf.mul(tf.transpose(weight_per_label), preweight_cost));
cost = tf.reduce_mean(cost_vector);
train_step = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)


################################
## Define Evaluation Graph
################################
max_pred = tf.argmax(pred,1);
correct_prediction = tf.equal(tf.argmax(pred,1), tf.argmax(y,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))


###############################
## Define Initialization function for variables/ops
###############################
init = tf.global_variables_initializer() ## initialization operation




##########################################################################################
## Train and Classify
##########################################################################################
with tf.Session() as sess:
    sess.run(init);

    #################################################################
    ## Train Model
    #################################################################
    # Start populating the filename queue.
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord)

    #for i in range(1200):
        # Retrieve a single instance:
    #print(col1);
    #print(sess.run([results]))
    #print(example);


    epochs = EPOCHS;
    display_ratio = 200;

    ## for tracking cost,acc per epoch
    training_progress = pd.DataFrame(columns =  ["epoch", "cost", "accuracy"]);

    for i in range(epochs):
        batch_feature, batch_label, batch_key = load_data.return_regular_batch([TRAIN_SOURCE], batch_size);

        if(i == 0):
            start_time = time.time()
            print ('Init Cost : ', end = '');
            print (sess.run(cost, feed_dict={x: batch_feature, y : batch_label}));

        if(i % (epochs/display_ratio) == 0 and i != 0):
            end_time = time.time();
            print ('Epoch %6d' % i, end = '');
            print(' ... cost : ', end = '');
            this_cost = (sess.run(cost, feed_dict={x: batch_feature, y : batch_label}));
            print ('%10f' % this_cost, end = '');
            print (',  acc : ', end = '');
            this_acc = (sess.run(accuracy, feed_dict={x: batch_feature, y : batch_label}))
            print ('%10f' % this_acc, end = '');
            #print(' - lr : ', end = '');
            #print ('%10f' % sess.run(learning_rate), end = '');
            print (',  dt : ', end = '');
            delta_t = end_time - start_time;
            print ('%10f' % delta_t, end = '');
            print('');

            #print("Pred -vs- Label:");
            #print(sess.run(pred[0:10],  feed_dict={x: batch_feature, y : batch_label}));
            #print(batch_label[0:10]);

            training_progress.loc[i] = [i, this_cost, this_acc];
            start_time = time.time()

        sess.run(train_step, feed_dict={x: batch_feature, y : batch_label})

    print ('Final Cost : ', end = '');
    final_cost_found = sess.run(cost, feed_dict={x: batch_feature, y : batch_label});
    print (final_cost_found);
    print ('Final Learning Rate : ', end = '');
    #print (sess.run(learning_rate));
    sumacc = 0;
    for i in range(10):
        batch_feature, batch_label, batch_key = load_data.return_regular_batch([TRAIN_SOURCE], batch_size);
        predictions = (sess.run(perc_pred, feed_dict={x: batch_feature, y : batch_label}))
        max_predictions = (sess.run(max_pred, feed_dict={x: batch_feature, y : batch_label}))
        acc = (sess.run(accuracy, feed_dict={x: batch_feature, y : batch_label}))
        ## print(acc);
        sumacc += acc;
    sumacc = sumacc/10;
    print ('Average Acc : ', end = '');
    print (sumacc);

    coord.request_stop()
    coord.join(threads)




    #################################################################
    ## Classify and Record
    #################################################################
    if(save_training):
        #########
        ## Training Batch
        #########
        batch_feature, batch_label, batch_key = load_data.return_regular_batch([TRAIN_SOURCE], -1);
        print(batch_feature.shape);
        print(batch_label.shape);
        print(len(batch_key));
        predictions = (sess.run(perc_pred, feed_dict={x: batch_feature}))
        max_predictions = (sess.run(max_pred, feed_dict={x: batch_feature}))
        classification_df = pd.DataFrame();
        classification_df["is_plant"] = np.array((batch_label[:, 1]), 'int');
        classification_df["pred_plant"] = max_predictions;
        classification_df["key"] = batch_key;
        classification_df["pred_0"] = predictions[:, 0];
        classification_df["pred_1"] = predictions[:, 1];
        save_data.save_classification(classification_df, delta_mod = delta_mod+'_train');

    #########
    ## Testing Batch
    #########
    batch_feature, batch_label, batch_key = load_data.return_regular_batch([TEST_SOURCE], -1);
    predictions = (sess.run(perc_pred, feed_dict={x: batch_feature}))
    max_predictions = (sess.run(max_pred, feed_dict={x: batch_feature}))
    classification_df = pd.DataFrame();
    classification_df["is_plant"] = np.array((batch_label[:, 1]), 'int');
    classification_df["pred_plant"] = max_predictions;
    classification_df["key"] = batch_key;
    classification_df["pred_0"] = predictions[:, 0];
    classification_df["pred_1"] = predictions[:, 1];
    save_data.save_classification(classification_df, delta_mod = delta_mod+'_test');

    #################################
    ## Save Hyperparameter config
    #################################
    epochs = EPOCHS;
    rtrue = R_True;
    hyperstring = "";
    hyperparamlist = ['delta_mod', 'source_mod',  'epochs',  'batch_size', 'learning_rate', 'n_hidden_1', 'n_hidden_2',  'rtrue' , 'final_cost_found', 'classifier_choice'];
    for name in hyperparamlist:
        name_of_var = name;
        val_of_var = eval(name);
        hyperstring += name_of_var + " : " + str(val_of_var) + "\n";

    myfile = open("results/"+delta_mod+"_z_hyperparams.txt", "w+");
    myfile.write(hyperstring);
    myfile.close();
    print("Hyperparameters written.");
