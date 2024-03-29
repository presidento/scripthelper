# scripthelper

Helper module for simple command line Python scripts.

The documentation with inline examples can be found in [pypi](https://pypi.org/project/scripthelper/).

## Basic usage

See [example1.py](example1.py)

It just works. Try `--verbose` and `--quiet`  command line options, too.
It uses colored log messages on a terminal.
See `--help` for more information.

## Adding other command line parameters

See [example2.py](example2.py)

For bigger scripts it is good idea to have the logger at the very beginning, and encapsulate the argument parsing phase, which is typically in the main function:

See [example2b.py](example2b.py)

## Progressbar works with logging, too

See [example3.py](example3.py)

It is automatically disabled on non-tty `stderr` by default.

## Extended log levels can be used in modules

See [example4.py](example4.py)

See [example4module.py](example4module.py)

## You can easily preserve logs in files

See [example5.py](example5.py)

## It handles exceptions, warnings

See [example6.py](example6.py)

The local variables will be displayed in stack trace, for example:

```
WARNING example6.py:6: UserWarning: This user warning will be captured.
  scripthelper.warn("This user warning will be captured.")

CRITICAL Uncaught RuntimeError: This exception should be handled.
File "example6.py", line 10, in <module>
    6    scripthelper.warn("This user warning will be captured.")
    7
    8    this_variable = "will be displayed in stack trace"
    9    as_well_as = "the other variables"
--> 10   raise RuntimeError("This exception should be handled.")
    ..................................................
     this_variable = 'will be displayed in stack trace'
     as_well_as = 'the other variables'
    ..................................................
```

## Has built-in colored pretty printer

See [example7.py](example7.py)

## Has built-in persisted state handler

The state is persisted immediately in the background in YAML. Mutable objects (`list`, `dict`) also can be used.

See [example9.py](example9.py)

```
$ python3 example9.py
INFO example9 Processing item #1
INFO example9 - Element 1

$ python3 example9.py
INFO example9 Processing item #2
INFO example9 - Element 1
INFO example9 - Element 2

$ python3 example9.py
INFO example9 Processing item #3
INFO example9 - Element 2
INFO example9 - Element 3
```

## Helps issuing a warning only once

See [example10.py](example10.py)

