#!/bin/bash
# Abort script at first error, when a command exits with non-zero status (except in until or while loops, if-tests, list constructs)
set -e
# Causes a pipeline to return the exit status of the last command in the pipe that returned a non-zero return value.
set -o pipefail

echo "[INFO] Running pip install"
pip install -r requirements.txt

echo "[INFO] Running lint (for configuration: see setup.cfg)"
echo "[INFO] ... Running pep8 (for configuration: see setup.cfg)"
for init_file in `find . -name '__init__.py'`
do
    module=`dirname $init_file`
    echo "[INFO] ... ... pep8 $module"
    pep8 $module
done

echo "[INFO] ... Running pylint (for configuration: see .pylintrc)"
for init_file in `find . -name '__init__.py'`
do
    module=`dirname $init_file`
    echo "[INFO] ... ... pylint $module"
    pylint $module
done

echo "[INFO] Running tests"
python -m unittest
