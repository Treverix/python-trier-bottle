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

echo "[INFO] Running tests and measuring code coverage"
coverage run -m unittest
coverage report | grep -v 100%
coverage html
count=`grep pc_cov coverage_html_report/index.html | grep -c "100%" || true`
if [ "x$count" != "x1" ]
then
    echo "[ERROR] Expecting 100% code coverage in the python code"
    exit 1
fi
