import logging

def initialize( out_dir, bool_debug_mode ):
    logger = logging.getLogger();
    logger.setLevel(logging.INFO);
    if(bool_debug_mode): logger.setLevel(logging.DEBUG); ## if debug mode selected, overwrite default info mode

    ## configure console output
    console_format = BColors.OKGREEN + '[%(levelname)s]' + BColors.ENDC + ' (%(name)s) %(message)s'
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter(console_format))
    logger.addHandler(console)

    ## configure file output
    file_format = '[%(levelname)s] (%(name)s) %(message)s'
    log_file = logging.FileHandler(out_dir + '/debug.log', mode='w')
    log_file.setLevel(logging.DEBUG)
    log_file.setFormatter(logging.Formatter(file_format))
    logger.addHandler(log_file)


class BColors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	WHITE = '\033[37m'
	YELLOW = '\033[33m'
	GREEN = '\033[32m'
	BLUE = '\033[34m'
	CYAN = '\033[36m'
	RED = '\033[31m'
	MAGENTA = '\033[35m'
	BLACK = '\033[30m'
	BHEADER = BOLD + '\033[95m'
	BOKBLUE = BOLD + '\033[94m'
	BOKGREEN = BOLD + '\033[92m'
	BWARNING = BOLD + '\033[93m'
	BFAIL = BOLD + '\033[91m'
	BUNDERLINE = BOLD + '\033[4m'
	BWHITE = BOLD + '\033[37m'
	BYELLOW = BOLD + '\033[33m'
	BGREEN = BOLD + '\033[32m'
	BBLUE = BOLD + '\033[34m'
	BCYAN = BOLD + '\033[36m'
	BRED = BOLD + '\033[31m'
	BMAGENTA = BOLD + '\033[35m'
	BBLACK = BOLD + '\033[30m'

	@staticmethod
	def cleared(s):
		return re.sub("\033\[[0-9][0-9]?m", "", s)
