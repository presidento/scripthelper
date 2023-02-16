import setuptools
import pathlib
import re

REPOSITORY_WEB_URL = "https://github.com/presidento/scripthelper/blob/master"

def long_description():
    with open("README.md", "r") as fh:
        description = ""
        for line in fh:
            match = re.match(r"See \[(.*)\]\(\1\)", line)
            if match:
                filename = match.group(1)
                description += f"[{filename}]({REPOSITORY_WEB_URL}/{filename}):\n\n"
                description += "```python\n"
                description += pathlib.Path(filename).read_text()
                description += "```\n"
            elif "[pypi](" not in line:
                description += line
        return description

setuptools.setup(
    name="scripthelper",
    version="23.01",
    scripts=[],
    author="Máté Farkas",
    author_email="fm@farkas-mate.hu",
    description="Helper module for creating simple Python scripts",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/presidento/scripthelper",
    packages=["scripthelper"],
    package_data={"scripthelper": ["py.typed"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    install_requires=[
        "tqdm >= 4.31.1",
        "coloredlogs >= 10.0",
        "verboselogs >= 1.7",
        "traceback_with_variables >= 2.0.1",
        "prettyprinter >= 0.18.0",
        "persistedstate >= 22.2"
    ],
)
