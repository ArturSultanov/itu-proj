#!/bin/bash
find . -type d -name "__pycache__" -exec rm -rf {} +
export PYTHONPATH=$PWD
# Run Uvicorn with the correct module path to the app instance
uvicorn backend.main:app --host 0.0.0.0 --reload
