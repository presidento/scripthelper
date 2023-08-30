#!/usr/bin/env python3
import scripthelper

scripthelper.bootstrap()

scripthelper.warn("This user warning will be captured.")

this_variable = "will be displayed in stack trace"
as_well_as = "the other variables"
raise RuntimeError("This exception should be handled.")
