"""Framework for small scripts in Python 3

You'll get the whole environment by importing just
one file, and you can start working immediately.

The output will be colored with support of multiple
log levels, easy-to-add command line arguments, etc."""
import argparse
import inspect
import logging
import logging.handlers
import pathlib
import sys
import warnings

import coloredlogs
import colorful
import prettyprinter
import tqdm
import verboselogs
from traceback_with_variables.core import ColorSchemes, Format, iter_exc_lines

_with_colors = None

logger = logging.getLogger(__name__)

__all__ = [
    # Logging
    "getLogger",
    "CRITICAL",
    "ERROR",
    "WARNING",
    "INFO",
    "VERBOSE",
    "DEBUG",
    "SPAM",
    # Argument parsing and bootstrap
    "bootstrap",
    "bootstrap_args",
    "add_arguments",
    "args",
    # Progressbar
    "progressbar",
    # For debugging
    "pprint",
    "pp",
    "warn",
]

CRITICAL = logging.CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
INFO = logging.INFO
VERBOSE = verboselogs.VERBOSE
DEBUG = logging.DEBUG
SPAM = verboselogs.SPAM
warn = warnings.warn


class CustomLogFormatter(coloredlogs.ColoredFormatter):
    def __init__(self, format_str, *, colors):
        self.colors = colors
        super().__init__(
            format_str,
            level_styles=self._coloredlogs_styles(),
            field_styles=self._coloredlogs_styles(),
        )

    def _coloredlogs_styles(self):
        if self.colors:
            return None  # Default value
        else:
            return {}  # Disable coloring

    def formatException(self, stack_info):
        if self.colors:
            color_scheme = ColorSchemes.common
        else:
            color_scheme = ColorSchemes.none

        return "\n".join(
            iter_exc_lines(
                e=stack_info[1],
                num_skipped_frames=1,
                fmt=Format(color_scheme=color_scheme),
            )
        )


class ConsoleLogHandler(logging.StreamHandler):
    def __init__(self):
        logging.StreamHandler.__init__(self)
        self.setFormatter(
            CustomLogFormatter("%(levelname)s %(message)s", colors=_with_colors)
        )

    def emit(self, record):
        msg = self.format(record)
        tqdm.tqdm.write(msg)


def _exception_handler(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    message = f"Uncaught {exc_type.__name__}: {exc_value}"
    logger.critical(message, exc_info=exc_value)


def _setup_logger(console_log_level):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        prettyprinter.install_extras()
    verboselogs.install()
    if sys.platform == "win32":
        # In Windows the default black is black, which is invisible on the default terminal.
        coloredlogs.DEFAULT_FIELD_STYLES["levelname"] = {"color": "blue"}

    root_logger = logging.getLogger()
    root_logger.setLevel(min(console_log_level, logging.DEBUG))

    console_log_handler = ConsoleLogHandler()
    console_log_handler.setLevel(console_log_level)
    root_logger.addHandler(console_log_handler)

    sys.excepthook = _exception_handler
    logging.captureWarnings(True)


def _log_level_from_verbosity(console_verbosity):
    levels = [
        logging.ERROR,
        logging.WARNING,
        logging.INFO,
        logging.VERBOSE,
        logging.DEBUG,
        logging.SPAM,
    ]
    default_level = logging.INFO

    new_index = levels.index(default_level) + console_verbosity
    new_index = max(0, min(len(levels) - 1, new_index))
    log_level = levels[new_index]
    return log_level


########################################################################################v


def getLogger(name="__main__"):
    """Return a verbose logger for a module

    It is an alias for verboselogs.VerboseLogger.
    Can be used as the logging.getLogger() method.
    Extends built-in logger with levels: verbose, spam
    """
    return verboselogs.VerboseLogger(name)


def get_logger(name="__main__"):
    warnings.warn(
        "get_logger is deprecated in favor of getLogger. Will be removed in 2022.",
        category=DeprecationWarning,
    )
    return getLogger(name)


args = None  # Will be set during bootstrap

parser = argparse.ArgumentParser()
parser.add_argument(
    "-v",
    "--verbose",
    action="count",
    help="Increase verbosity. Can be applied multiple times, like -vv",
)
parser.add_argument(
    "-q",
    "--quiet",
    action="count",
    help="Decrease verbosity. Can be applied multiple times, like -qq",
)
parser.add_argument(
    "--colors",
    action="store_true",
    default=None,
    help="Force set colored output",
)
parser.add_argument(
    "--no-colors",
    action="store_false",
    dest="colors",
    help="Force set non-colored output",
)


def add_argument(*args, **kw):
    """See: ArgumentParser.add_argument()"""
    parser.add_argument(*args, **kw)


def setup_file_logging(*, level="INFO", filename=None):
    """Setups logging to file

    The default filename is the name of the main script.
    It uses RotatingFileHandler."""
    if filename is None:
        caller_module = inspect.getmodule(inspect.stack()[1][0])
        filename = pathlib.Path(caller_module.__file__).with_suffix(".log")

    file_log_handler = logging.handlers.RotatingFileHandler(
        filename, encoding="utf-8", maxBytes=10 * 1024 * 1024, backupCount=9
    )
    formatter = CustomLogFormatter(
        "%(asctime)s %(levelname)s %(message)s", colors=False
    )
    file_log_handler.setFormatter(formatter)
    file_log_handler.setLevel(level)
    logging.getLogger().addHandler(file_log_handler)


progressbar = tqdm.tqdm


def pprint(*args, **kwargs):
    """PrettyPrint with or without colors"""
    if _with_colors:
        prettyprinter.cpprint(*args, **kwargs)
    else:
        prettyprinter.pprint(*args, **kwargs)


pp = pprint


def bootstrap_args():
    """Bootstraps the framework

    returns (logger, args)
        The logger for main scripts
        And the parsed argument"""
    global args
    global _with_colors

    args = parser.parse_args()

    if args.colors is None:
        _with_colors = sys.stdout.isatty()
    else:
        _with_colors = args.colors
        if args.colors:
            # Hack for pretty printer on force colors
            colorful.colorful.use_16_ansi_colors()

    console_verbosity = (args.verbose or 0) - (args.quiet or 0)
    console_log_level = _log_level_from_verbosity(console_verbosity)
    _setup_logger(console_log_level)

    logger.debug(f"Arguments: {args}")

    return getLogger(), args


def bootstrap():
    """Bootstraps the framework

    returns logger - the logger for the main script"""
    return bootstrap_args()[0]
