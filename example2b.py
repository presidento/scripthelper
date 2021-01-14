#!/usr/bin/env python3
import scripthelper

scripthelper.add_argument("--name", default="World")
logger = scripthelper.bootstrap()
name = scripthelper.args.name

logger.info(f"Hello {name}")
