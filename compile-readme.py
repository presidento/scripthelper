#!/usr/bin/env python3
import pathlib
import re

REPOSITORY_WEB_URL = "https://github.com/presidento/scripthelper/blob/master"


with open("README.compiled.md", "w", encoding="utf-8") as out_file:
    with open("README.md", "r", encoding="utf-8") as in_file:
        for line in in_file:
            match = re.match(r"See \[(.*)\]\(\1\)", line)
            if match:
                filename = match.group(1)
                out_file.write(f"[{filename}]({REPOSITORY_WEB_URL}/{filename}):\n\n")
                out_file.write("```python\n")
                out_file.write(pathlib.Path(filename).read_text())
                out_file.write("```\n")
            elif "[pypi](" not in line:
                out_file.write(line)
