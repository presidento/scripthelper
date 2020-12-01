import coloredlogs
import verboselogs
import logging
import logging.handlers
import argparse
import tqdm
import sys
import inspect
import pathlib
import warnings
from traceback_with_variables.color import supports_ansi, choose_color_scheme
from traceback_with_variables.core import iter_tb_lines, ColorScheme, ColorSchemes

progressbar = tqdm.tqdm
console_log_handler = None

logger = logging.getLogger(__name__)


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

        lines = []
        for line in iter_tb_lines(
            e=stack_info[1],
            tb=stack_info[2],
            num_skipped_frames=1,
            color_scheme=color_scheme,
        ):
            lines.append(line)
        return "\n".join(lines)


class ConsoleLogHandler(logging.StreamHandler):
    def __init__(self):
        logging.StreamHandler.__init__(self)
        self.setFormatter(
            CustomLogFormatter(
                "%(levelname)s %(message)s", colors=supports_ansi(sys.stdout)
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
    logger.critical(message, exc_info=exc_value)


def bootstrap_to_logger(log_file=None):
    global console_log_handler
    verboselogs.install()
    if sys.platform == "win32":
        # In Windows the default black is black, which is invisible on the default terminal.
        coloredlogs.DEFAULT_FIELD_STYLES["levelname"] = {"color": "blue"}

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    console_log_handler = ConsoleLogHandler()
    logger.addHandler(console_log_handler)

    sys.excepthook = _exception_handler
    logging.captureWarnings(True)

    if log_file:
        warnings.warn(
            'The "log_file" parameter is deprecated. Use "setup_file_logging" method instead.',
            DeprecationWarning,
        )
        setup_file_logging(level=logging.DEBUG, log_file=log_file)

    return get_logger()


def get_logger(name="__main__"):
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
    if log_level < logging.DEBUG:
        logging.getLogger().setLevel(log_level)
    console_log_handler.setLevel(log_level)


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


def setup_file_logging(*, level="INFO", filename=None):
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


def add_argument(*args, **kw):
    parser.add_argument(*args, **kw)


def parse_args():
    args = parser.parse_args()
    verbose_count = args.verbose or 0
    quiet_count = args.quiet or 0
    _set_verbosity(verbose_count - quiet_count)
    logging.getLogger(__name__).debug("Arguments: %s", args)
    return args


def bootstrap(log_file=None):
    logger = bootstrap_to_logger(log_file)
    parse_args()
    return logger


def bootstrap_args(log_file=None):
    logger = bootstrap_to_logger(log_file)
    args = parse_args()
    return logger, args
