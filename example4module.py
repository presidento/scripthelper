#!/usr/bin/env python3
import scripthelper

logger = scripthelper.get_logger(__name__)


def do_the_things():
    logger.verbose("Calling logger.verbose raises an exception if it does not work.")
    logger.info("Hello from a module.")
