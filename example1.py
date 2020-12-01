#!/usr/bin/env python3
import scripthelper

logger = scripthelper.bootstrap()

logger.critical("critical message")
logger.error("error message")
logger.warning("warning message")
logger.info("info message")
logger.verbose("verbose message")
logger.debug("debug message")
logger.spam("spam message")
