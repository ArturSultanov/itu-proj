#!/bin/bash

cd backend

# Run Uvicorn with the correct module path to the app instance
uvicorn src.app:app --host 0.0.0.0 --reload

cd ..
