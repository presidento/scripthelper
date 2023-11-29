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
from typing import Optional, Tuple

import coloredlogs
import persistedstate
import prettyprinter
import stackprinter
import tqdm
from colorful import colorful  # type: ignore

_with_colors = None
_with_traceback_variables = True

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
    "warning_once",
    # Warning
    "warn",
    # Argument parsing and bootstrap
    "bootstrap",
    "bootstrap_args",
    "initialize",
    "add_arguments",
    "setup_file_logging",
    "args",
    "parser",
    # Progressbar
    "progressbar",
    # For debugging
    "pprint",
    "pp",
]

CRITICAL = logging.CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
INFO = logging.INFO
VERBOSE = (logging.INFO + logging.DEBUG) // 2
DEBUG = logging.DEBUG
SPAM = logging.DEBUG // 2
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
        if _with_traceback_variables:
            show_variables = "like_source"
        else:
            show_variables = False

        if self.colors:
            color_scheme = "darkbg3"
        else:
            color_scheme = "plaintext"

        return stackprinter.format(
            stack_info, style=color_scheme, show_vals=show_variables
        )


class ConsoleLogHandler(logging.StreamHandler):
    def __init__(self):
        logging.StreamHandler.__init__(self)
        self.setFormatter(
            CustomLogFormatter(
                "%(levelname)s %(name)s %(message)s", colors=_with_colors
            )
        )

    def emit(self, record):
        msg = self.format(record)
        tqdm.tqdm.write(msg)


def _exception_handler(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    message = f"Uncaught {exc_type.__name__}: {exc_value}"
    getLogger().critical(message, exc_info=exc_value)


class MoreLevelsLogger(logging.getLoggerClass()):  # type: ignore
    def __init__(self, *args, **kw):
        logging.Logger.__init__(self, *args, **kw)
        self.parent = logging.getLogger()

    def spam(self, msg, *args, **kw):
        if self.isEnabledFor(SPAM):
            self._log(SPAM, msg, args, **kw, stacklevel=2)

    def verbose(self, msg, *args, **kw):
        if self.isEnabledFor(VERBOSE):
            self._log(VERBOSE, msg, args, **kw, stacklevel=2)


def _setup_logger(console_log_level):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        prettyprinter.install_extras()

    logging.setLoggerClass(MoreLevelsLogger)
    logging.addLevelName(VERBOSE, "VERBOSE")
    logging.addLevelName(SPAM, "SPAM")

    if sys.platform == "win32":
        # In Windows the default black is black, which is invisible on the default terminal.
        coloredlogs.DEFAULT_FIELD_STYLES["levelname"] = {"color": "blue"}
    coloredlogs.DEFAULT_FIELD_STYLES["name"] = {"color": "cyan", "faint": True}

    root_logger = logging.getLogger()
    root_logger.setLevel(min(console_log_level, logging.DEBUG))

    console_log_handler = ConsoleLogHandler()
    console_log_handler.setLevel(console_log_level)
    root_logger.addHandler(console_log_handler)

    sys.excepthook = _exception_handler
    logging.captureWarnings(True)


def _log_level_from_verbosity(console_verbosity):
    levels = [
        ERROR,
        WARNING,
        INFO,
        VERBOSE,
        DEBUG,
        SPAM,
    ]
    default_level = INFO

    new_index = levels.index(default_level) + console_verbosity
    new_index = max(0, min(len(levels) - 1, new_index))
    log_level = levels[new_index]
    return log_level


########################################################################################v


def getLogger(name: Optional[str] = None) -> MoreLevelsLogger:
    """Return a verbose logger for a module

    It is an alias for MoreLevelsLogger.
    Can be used as the logging.getLogger() method.
    Extends built-in logger with levels: verbose, spam
    """
    logger = MoreLevelsLogger(name)
    if name is None:
        caller_file = None
        this_file = pathlib.Path(__file__).absolute()
        for frame in inspect.stack():
            caller_file = pathlib.Path(frame.filename).absolute()
            if caller_file != this_file:
                logger.name = caller_file.stem
                break
    return logger


_WARNING_ONCE_CACHE = set()


def warning_once(msg, *args, **kwargs):
    """Issue a warning only once

    Only the first call will be logged with the same message."""
    if msg in _WARNING_ONCE_CACHE:
        return
    _WARNING_ONCE_CACHE.add(msg)
    getLogger().warning(msg, *args, **kwargs)


args: argparse.Namespace  # Parsed arguments, will be set during bootstrap

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
parser.add_argument(
    "--disable-traceback-variables",
    action="store_true",
    help="Do not display variables in traceback context",
)


def add_argument(*args, **kw) -> None:
    """See: ArgumentParser.add_argument()"""
    parser.add_argument(*args, **kw)


def setup_file_logging(*, level: str = "INFO", filename: Optional[str] = None) -> None:
    """Setups logging to file

    The default filename is the name of the main script.
    It uses RotatingFileHandler."""
    if filename is None:
        caller_module = inspect.getmodule(inspect.stack()[1][0])
        module_file: str = caller_module.__file__  # type:ignore
        filename = pathlib.Path(module_file).with_suffix(".log").as_posix()

    file_log_handler = logging.handlers.RotatingFileHandler(
        filename, encoding="utf-8", maxBytes=10 * 1024 * 1024, backupCount=9
    )
    formatter = CustomLogFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s", colors=False
    )
    file_log_handler.setFormatter(formatter)
    file_log_handler.setLevel(level)
    logging.getLogger().addHandler(file_log_handler)


def progressbar(*args, disable=None, **kwargs):
    """See tqdm.tqdm

    The default value for 'disable' is None, meaning
        - enable progressbar on terminals
        - disable progressbar on non-tty
    (checking the type of stderr)"""
    kwargs["disable"] = disable
    return tqdm.tqdm(*args, **kwargs)


def pprint(*args, **kwargs) -> None:
    """PrettyPrint with or without colors"""
    if _with_colors:
        prettyprinter.cpprint(*args, **kwargs)
    else:
        prettyprinter.pprint(*args, **kwargs)


pp = pprint


class PersistedState(persistedstate.PersistedState):
    def __init__(self, _filename=None, **kwargs):
        filename = _filename
        if filename is None:
            caller_module = inspect.getmodule(inspect.stack()[1][0])
            module_file: str = caller_module.__file__  # type:ignore
            filename = pathlib.Path(module_file).with_suffix(".state").as_posix()
        return super().__init__(filename, **kwargs)


def bootstrap_args() -> Tuple[MoreLevelsLogger, argparse.Namespace]:
    """Bootstraps the framework

    returns (logger, args)
        The logger for main scripts
        And the parsed argument"""
    global args
    global _with_colors
    global _with_traceback_variables

    args = parser.parse_args()

    if args.colors is None:
        _with_colors = sys.stdout.isatty()
    else:
        _with_colors = args.colors
        if args.colors:
            # Hack for pretty printer on force colors
            colorful.use_16_ansi_colors()

    _with_traceback_variables = not args.disable_traceback_variables
    console_verbosity = (args.verbose or 0) - (args.quiet or 0)
    console_log_level = _log_level_from_verbosity(console_verbosity)
    _setup_logger(console_log_level)

    logger = getLogger()
    logger.debug(f"Arguments: {args}")
    return logger, args


def bootstrap() -> MoreLevelsLogger:
    """Bootstraps the framework

    returns logger - the logger for the main script"""
    return bootstrap_args()[0]


def initialize() -> argparse.Namespace:
    """Bootstraps the framework

    return args - the parsed arguments"""
    return bootstrap_args()[1]
