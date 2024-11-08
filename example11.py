#!/usr/bin/env python3
import example4module
import scripthelper

scripthelper.bootstrap()
scripthelper.supress_info_logs("example4module")
example4module.do_the_things()
