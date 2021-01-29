import setuptools
import pathlib
import re

with open("README.md", "r") as fh:
    long_description = ""
    for line in fh:
        match = re.match(r"See \[(.*)\]\(\1\)", line)
        if match:
            filename = match.group(1)
            long_description += f"{filename}:\n"
            long_description += "```python\n"
            long_description += pathlib.Path(filename).read_text()
            long_description += "```\n"
        else:
            long_description += line

setuptools.setup(
    name="scripthelper",
    version="21.2.1",
    scripts=[],
    author="Máté Farkas",
    author_email="fm@farkas-mate.hu",
    description="Helper module for creating simple Python 3 scripts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/presidento/scripthelper",
    packages=["scripthelper"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "tqdm >= 4.31.1",
        "coloredlogs >= 10.0",
        "verboselogs >= 1.7",
        "traceback_with_variables >= 2.0.1",
        "prettyprinter >= 0.18.0",
    ],
)
