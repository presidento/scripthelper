#!/usr/bin/env python3
import scripthelper
import warnings

scripthelper.bootstrap()


def uncaught_exception_test():
    this_variable = "will be displayed in stack trace"
    as_well_as = "the other variables"
    raise RuntimeError("This exception should be handled.")


warnings.warn("This user warning will be captured.")
uncaught_exception_test()
