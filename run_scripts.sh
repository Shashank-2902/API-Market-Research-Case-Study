#!/bin/bash
# Collect data from the API, then build the tables and plots.
set -e

echo "Running Python script..."
python3 /app/main.py

echo "Running R script..."
Rscript /app/visualization.R

echo "All scripts executed successfully."
