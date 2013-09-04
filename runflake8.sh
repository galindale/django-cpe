#!/bin/bash

# Ignore E501: line too long
# Ignore E122: continuation line missing
# Ignore F401: import not used

flake8 --exclude=build,bootstrap.py --ignore=E501,E122,F401 .
