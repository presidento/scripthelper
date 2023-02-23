DEFAULT_VERSION := "3.8"
SUPPORTED_VERSIONS := "3.7 3.8 3.9 3.10 3.11"

set shell := ["powershell", "-nop", "-c"]

# Bootstrap with all supported Python versions
bootstrap: && compile-readme
    @foreach ($version in ('{{ SUPPORTED_VERSIONS }}' -split '\s+')) { just bootstrap-with "$version" }
    & ".{{ DEFAULT_VERSION }}.venv\Scripts\python.exe" -m pip install mypy setuptools wheel build twine --quiet --upgrade

# Set up Python environment with specified Python version
bootstrap-with VERSION:
    If (-not (Test-Path .{{ VERSION }}.venv)) { py -{{ VERSION }} -m venv .{{ VERSION }}.venv }
    & ".{{ VERSION }}.venv\Scripts\python.exe" -m pip install pip --quiet --upgrade
    & ".{{ VERSION }}.venv\Scripts\python.exe" -m pip install -e . --upgrade --upgrade-strategy eager

# Compile README.md
compile-readme:
    & ".{{ DEFAULT_VERSION }}.venv\Scripts\python.exe" compile-readme.py

# Check static typing
mypy:
    just clean
    & ".{{ DEFAULT_VERSION }}.venv\Scripts\mypy.exe" src

# Test with all supported Python versions
test: mypy
    @foreach ($version in ('{{ SUPPORTED_VERSIONS }}' -split '\s+')) { just test-with "$version" }

# Run the tests with specified Python version
test-with VERSION:
    & ".{{ VERSION }}.venv\Scripts\python.exe" .\test_examples.py

# Remove compiled assets
clean:
    -Remove-Item -Recurse -Force -ErrorAction Ignore build
    -Remove-Item -Recurse -Force -ErrorAction Ignore dist

# Build the whole project, create a release
build: clean bootstrap test compile-readme
    & ".{{ DEFAULT_VERSION }}.venv\Scripts\python.exe" -m build

# Upload the release to PyPi
upload:
    & ".{{ DEFAULT_VERSION }}.venv\Scripts\python.exe" -m twine upload dist/*
