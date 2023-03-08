set shell := ["nu", "-c"]

DEFAULT_VERSION := "3.8"
SUPPORTED_VERSIONS := "['3.7' '3.8' '3.9' '3.10' '3.11']"
PYTHON_EXECUTABLE := if os_family() == "windows" { "Scripts/python.exe" } else { "bin/python3" }
SYSTEM_PYTHON_PREFIX := if os_family() == "windows" { "py -" } else { "python" }

# Bootstrap with all supported Python versions
bootstrap:
    touch README.compiled.md
    for version in {{ SUPPORTED_VERSIONS }} { just bootstrap-with $version }
    just python {{ DEFAULT_VERSION }} -m pip install mypy build twine --quiet --upgrade

# Set up Python environment with specified Python version
bootstrap-with VERSION:
    if not (".{{ VERSION }}.{{ os_family() }}.venv" | path exists) { {{ SYSTEM_PYTHON_PREFIX }}{{ VERSION }} -m venv .{{ VERSION }}.{{ os_family() }}.venv }
    just python {{ VERSION }} -m pip install pip mypy setuptools wheel twine --quiet --upgrade
    just python {{ VERSION }} -m pip install -e . --upgrade --upgrade-strategy eager

# Compile README.md
compile-readme:
    just python {{ DEFAULT_VERSION }} compile-readme.py

# Run a specific Python interpreter
python VERSION *ARGS:
    @^".{{ VERSION }}.{{ os_family() }}.venv/{{ PYTHON_EXECUTABLE }}" {{ ARGS }}

# Check static typing
mypy:
    just clean
    just python {{ DEFAULT_VERSION }} -m mypy . src

# Test with all supported Python versions
test: mypy
    for version in {{ SUPPORTED_VERSIONS }} { just test-with $version }

# Run the tests with specified Python version
test-with VERSION:
    just python {{ VERSION }} test_examples.py

# Remove compiled assets
clean:
    rm build dist scripthelper.egg-info --force --recursive --verbose

# Build the whole project, create a release
build: clean bootstrap test compile-readme
    just python {{ DEFAULT_VERSION }} -m build

# Upload the release to PyPi
upload:
    just python {{ DEFAULT_VERSION }} -m twine upload dist/*
