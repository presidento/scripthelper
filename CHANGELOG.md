## 24.1

- Add Python 3.13 support

## 23.5

- Show the name of the logger in the log messages (can be very helpful if you use libraries which logs too much)

## 23.4

- Use `stackprinter` module instead of `traceback_with_variables` to have pretty stack traces for unhandled exceptions
- Allow to disable displaying variables in stack traces (`--disable-traceback-variables` command line argument)
- Add Python 3.12 support

## 23.3

- Add `warning_once` function
- Remove Python 3.7 support
- Use pyproject.toml
- New version format: "{YEAR:2d}.{PATCH}"

## 23.02

- Add persisted state handler

## 23.01

- Add `initialize` method for bootstrap & return args
- Remove Python 3.6 support
- Remove deprecated `get_logger` function. (Use `getLogger` instead.)
- New version format: "{YEAR:2d}.{PATCH:2d}"

## 22.09.1

- Disable progressbar dynamically on non-tty stderr
- Mark Python 3.11 compatible
- Mark package typed

## 21.10.1

- Make Python 3.10 compatible

## 21.2.1

- Add `warn` (`warnings.warn`)
- Add loglevel constants
- Make compatible with Python 3.7, 3.8, 3.9
- Add docstrings

## 21.1.1

- Make `scripthelper.args` public.
- Upgrade `traceback_with_variables` dependency
- Small bugfixes
- New version format: "{YEAR}.{MONTH}.{PATCH}"

## 1.9 / 2020-12-12

- Add colored pretty printer support
- Add `getLogger` method, use that by default instead of `get_logger`

## 1.8 / 2020-12-01

- Display variables in stacktrace, using `traceback_with_variables` module.

## 1.7 / 2020-10-21

- Use `RotatingFileHandler` instead of simple `FileHandler`

## 1.6 / 2020-10-21

- Handle uncaught exceptions, warnings

## 1.5 / 2020-07-21

- Explicitly set utf-8 encoding for logging file handler

## 1.4 / 2020-04-27

- Add `setup_file_logging` method
- Deprecate `log_file` parameter

## 1.3 / 2020-04-20

- Add `log_file` parameter to bootstrap methods

## 1.2 / 2019-04-11

- Add `get_logger` method, which returns a `VerboseLogger` instance

## 1.1 / 2019-04-03

- Add `bootstrap_args` method if you want to handle custom arguments

## 1.0 / 2019-03-28

First release