#!/usr/bin/env python3
import scripthelper

scripthelper.add_argument('-n', '--name', help='Name to greet')
logger, args = scripthelper.bootstrap_args()

if args.name:
    logger.debug('Name was provided')
    logger.info(f'Hello {args.name}')
else:
    logger.warning('Name was not provided')
