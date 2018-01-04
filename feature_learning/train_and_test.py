'''
    This script contains the main controlling logic for this feature learning based AES model
'''

import argparse
import logging;
import _utilities as utils

logger = logging.getLogger(__name__); ## setup logging


## define and parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_base", dest="input_base", type=str, metavar='<str>', required=True, help="The path and base name of the fold combination to train, tune, and test on. (e.g., ./0_data_manager/folds/fold_sets_3456.comb_0)")
parser.add_argument("-o", "--output_dir", dest="output_dir", type=str, metavar='<str>', required=False, default="./output/", help="The path to the output directory. (e.g., ./output/)")
parser.add_argument("-d", "--debug_mode", dest="bool_debug_mode", action='store_true', help="If true, logging is conducted at DEBUG level")
args = parser.parse_args()

## validate arguments


## basic configurations
utils.basic.mkdir_p(args.output_dir + "/preds"); ## ensure directory down to output_dir+'/preds' exists
utils.logger.initialize(args.output_dir, args.bool_debug_mode); ## initialize logger and ensure info output is recorded
