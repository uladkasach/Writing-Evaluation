
import numpy as np;

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
