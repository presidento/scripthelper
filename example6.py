#!/usr/bin/env python3
import scripthelper
import warnings

scripthelper.bootstrap()

warnings.warn("This user warning should be captured.")
raise RuntimeError("This exception should be handled.")
