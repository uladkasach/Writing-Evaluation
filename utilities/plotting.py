import numpy as np;
import matplotlib.pyplot as plt;

def plot_metrics_on_histogram(metrics, title, normalized = False, num_bins = 30, colors = None):

    data_list = [];
    weights = [];
    labels = [];
    for metric in sorted(metrics.keys()):
        this_list = metrics[metric];
        print("metric : " + metric + " -> " + str(len(this_list)))

        this_weight = np.ones_like(this_list)
        if(normalized): this_weight = this_weight/float(len(this_list)) ## normalized so that all bars add to one
        
        data_list.append(this_list);
        weights.append(this_weight);
        labels.append(metric);
        
        
    #colors = ['green', '#dbf8ff', 'white'];
    #colors = colors[:len(metrics)];
    this_fig, this_axis = plt.subplots()
    this_axis.hist(data_list, num_bins, color=colors, weights=weights, label=labels, range=(-2, 10)) #, range=(-0.2, 1)
    this_axis.legend(prop={'size': 10})

    plt.title(title);
    this_fig.tight_layout();
    this_fig.savefig("results/"+title+".png"); 
    