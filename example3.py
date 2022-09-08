#!/usr/bin/env python3
import scripthelper
import time

logger = scripthelper.bootstrap()

logger.info("Doing the calculations...")
for i in scripthelper.progressbar(range(100)):
    if i % 20 == 0:
        logger.verbose(f"Iteration {i}")
    if i % 5 == 0:
        logger.debug(f"Iteration {i}")
    if logger.isEnabledFor(scripthelper.SPAM):
        logger.spam(f"Iteration {i}")
    time.sleep(0.01)
logger.info("Done")
