DEFAULT_VERSION := "3.7"
SUPPORTED_VERSIONS := "3.6 3.7 3.8 3.9 3.10"

set shell := ["powershell", "-nop", "-c"]

# Bootstrap with all supported Python versions
bootstrap:
    @foreach ($version in ('{{ SUPPORTED_VERSIONS }}' -split '\s+')) { just bootstrap-with "$version" }

# Setting up Python environment with specified Python version
bootstrap-with VERSION:
    If (-not (Test-Path .{{ VERSION }}.venv)) { py -{{ VERSION }} -m venv .{{ VERSION }}.venv }
    & ".{{ VERSION }}.venv\Scripts\python.exe" -m pip install pip wheel --quiet --upgrade
    & ".{{ VERSION }}.venv\Scripts\python.exe" -m pip install . --upgrade

# Test with all supported Python versions
test:
    @foreach ($version in ('{{ SUPPORTED_VERSIONS }}' -split '\s+')) { just test-with "$version" }

# Run the tests with specified Python version
test-with VERSION:
    & ".{{ VERSION }}.venv\Scripts\python.exe" .\test_examples.py

clean:
    -Remove-Item -Recurse -Force -ErrorAction Ignore build
    -Remove-Item -Recurse -Force -ErrorAction Ignore dist

build: clean bootstrap test
    & ".{{ DEFAULT_VERSION }}.venv\Scripts\python.exe" -m pip install --upgrade setuptools wheel pip twine
    & ".{{ DEFAULT_VERSION }}.venv\Scripts\python.exe" setup.py sdist bdist_wheel

upload:
    & ".{{ DEFAULT_VERSION }}.venv\Scripts\python.exe" -m twine upload dist/*

