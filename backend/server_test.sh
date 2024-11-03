#!/bin/bash

# Run Uvicorn with the correct module path to the app instance
uvicorn main:app --host 0.0.0.0 --reload
