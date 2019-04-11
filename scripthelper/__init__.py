import coloredlogs
import verboselogs
import logging
import argparse
import tqdm
import sys

progressbar = tqdm.tqdm

class TqdmLogHandler(logging.StreamHandler):
    def __init__(self):
        logging.StreamHandler.__init__(self)

    def emit(self, record):
        msg = self.format(record)
        tqdm.tqdm.write(msg)

def bootstrap_to_logger():
    verboselogs.install()
    if sys.platform == 'win32':
        # In Windows the default black is black, which is invisible on the default terminal.
        coloredlogs.DEFAULT_FIELD_STYLES['levelname'] = {'color': 'blue'}

    log_handler = TqdmLogHandler()
    log_handler.setFormatter(coloredlogs.ColoredFormatter('%(levelname)s %(message)s'))
    logger = logging.getLogger()
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)

    return get_logger()

def get_logger(name='__main__'):
    return verboselogs.VerboseLogger(name)

def _set_verbosity(verbosity):
    levels = [
        logging.ERROR,
        logging.WARNING,
        logging.INFO,
        logging.VERBOSE,
        logging.DEBUG,
        logging.SPAM,
    ]
    default_level = logging.INFO

    new_index = levels.index(default_level) + verbosity
    new_index = max(0, min(len(levels) - 1, new_index))
    log_level = levels[new_index]
    logging.getLogger().setLevel(log_level)

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action='count',
        help='Increase verbosity. Can be applied multiple times, like -vv')
parser.add_argument('-q', '--quiet', action='count',
        help='Decrease verbosity. Can be applied multiple times, like -qq')

def add_argument(*args, **kw):
    parser.add_argument(*args, **kw)

def parse_args():
    args = parser.parse_args()
    verbose_count = args.verbose or 0
    quiet_count = args.quiet or 0
    _set_verbosity(verbose_count - quiet_count)
    logging.getLogger(__name__).debug('Arguments: %s', args)
    return args

def bootstrap():
    logger = bootstrap_to_logger()
    parse_args()
    return logger

def bootstrap_args():
    logger = bootstrap_to_logger()
    args = parse_args()
    return logger, args
