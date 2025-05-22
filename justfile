set shell := ["nu", "-c"]

# Bootstrap with all supported Python versions
bootstrap:
    touch README.compiled.md
    uv lock --upgrade
    uv sync --all-groups
    uv run tox run --notest

# Compile README.md
compile-readme:
    just py compile-readme.py

# Run python command with the default Python version
py *ARGS:
    uv run python -X dev {{ ARGS }}

# Run every check against source code
check: check-format mypy test-all

# Check source code formatting in case I forgot to format them
check-format:
    just py -m black --check src *.py

# Format source code with black
format:
    just py -m black src *.py

# Check static typing
mypy:
    just py -m mypy src *.py

# Test with all supported Python versions
test-all:
    uv run tox run

# Run the tests default Python version
test *ARGS:
    just py test_examples.py {{ ARGS }}

# Remove compiled assets
clean:
    rm build dist scripthelper.egg-info --force --recursive --verbose

# Build the whole project, create a release
build: clean bootstrap check compile-readme
    uv build

# Upload the release to PyPi
upload:
    uv upload
