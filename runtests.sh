#!/bin/bash

# py.test --cov djangocpe --cov-report=html ./src/djangocpe
cd tests
py.test --cov --create-db
