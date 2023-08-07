#!/usr/bin/env python3
import scripthelper

scripthelper.bootstrap()

for _ in range(10):
    scripthelper.warning_once("Item #12 has some errors")
