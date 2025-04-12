#!/bin/bash

# Run the Python script
echo "Running Python script..."
python3 /app/main.py

# Run the R script
echo "Running R script..."
Rscript /app/visualization.R

echo "All scripts executed successfully."