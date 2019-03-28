#!/usr/bin/env python3
import scripthelper

logger = scripthelper.bootstrap_to_logger()

scripthelper.add_argument('-n', '--name', help='Name to greet')
args = scripthelper.parse_args()

if args.name:
    logger.debug('Name was provided')
    logger.info(f'Hello {args.name}')
else:
    logger.warning('Name was not provided')
