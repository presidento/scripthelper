@echo off

echo Delete build folders
pause
RMDIR /Q/S build
RMDIR /Q/S dist

echo Activate Python environment
pause
call .venv\Scripts\activate.bat

echo Install dependencies and build the release
pause
python -m pip install --upgrade setuptools wheel pip twine
python -m pip install --upgrade .
python setup.py sdist bdist_wheel

echo Uploading release to pypi
pause
python -m twine upload dist/*
