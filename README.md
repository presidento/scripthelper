# scripthelper

Helper module for simple command line Python scripts

## Basic usage

```python
import scripthelper

logger = scripthelper.bootstrap()

logger.critical('critical message')
logger.error('error message')
logger.warning('warning message')
logger.info('info message')
logger.verbose('verbose message')
logger.debug('debug message')
logger.spam('spam message')
```

It just works, and adds `--verbose` and `--quiet` command line options, too.

## Adding other command line parameters

```python
import scripthelper

scripthelper.add_argument('-n', '--name', help='Name to greet')
logger, args = scripthelper.bootstrap_args()

if args.name:
    logger.debug('Name was provided')
    logger.info(f'Hello {args.name}')
else:
    logger.warning('Name was not provided')
```

## Progressbar works with logging, too

```python
import scripthelper
import time

logger = scripthelper.bootstrap()

logger.info('Doing the calculations...')
for i in scripthelper.progressbar(range(200)):
    if i % 20 == 0:
        logger.verbose(f'Iteration {i}')
    if i % 5 == 0:
        logger.debug(f'Iteration {i}')
    logger.spam(f'Iteration {i}')
    time.sleep(0.05)
logger.info('Done')
```

## You can easily preserve logs in files

```python
import scripthelper

logger = scripthelper.bootstrap()
scripthelper.setup_file_logging()

logger.warning('warning message')
logger.info('info message')
logger.debug('debug message')
```

## It handles exceptions, warnings

```python
import scripthelper
import warnings

scripthelper.bootstrap()

warnings.warn("This user warning should be captured.")
raise RuntimeError("This exception should be handled.")
```
