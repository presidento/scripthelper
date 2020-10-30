import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='scripthelper',  
    version='1.7',
    scripts=[],
    author='Máté Farkas',
    author_email='fm@farkas-mate.hu',
    description='Helper module for creating simple Python 3 scripts',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/presidento/scripthelper",
    packages=['scripthelper'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "tqdm >= 4.31.1",
        "coloredlogs >= 10.0",
        "verboselogs >= 1.7",
    ],
 )