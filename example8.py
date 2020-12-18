#!/usr/bin/env python3
import scripthelper

logger = scripthelper.bootstrap()

logger.info("Testing --colors and --no-colors options")
scripthelper.pp([True, "string", 1234])
raise Exception("Unhandled Exception")
