#!/bin/bash
pep8 --ignore=E701,E302,E501 `find . -name \*.py`
pyflakes $(find . -name \*.py | grep -v __init__)
