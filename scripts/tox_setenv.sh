#!/bin/bash

VARIABLE_NAME=SSST_MYPY_QTS_ARGUMENTS
echo "    pyqt5: ${VARIABLE_NAME}="$(venv/bin/qts mypy args --wrapper pyqt5)
echo "    pyqt6: ${VARIABLE_NAME}="$(venv/bin/qts mypy args --wrapper pyqt6)
echo "    pyside2: ${VARIABLE_NAME}="$(venv/bin/qts mypy args --wrapper pyside2)
echo "    pyside6: ${VARIABLE_NAME}="$(venv/bin/qts mypy args --wrapper pyside6)
