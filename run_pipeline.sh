#!/bin/bash

# Activate the virtual environment
source ~/retail_pipeline_project/venv/bin/activate

# Optional: Log file (to keep track of pipeline runs)
LOG_FILE=~/retail_pipeline_project/pipeline.log
echo "=== Pipeline Run: $(date) ===" >> "$LOG_FILE"

# Step 1: Clean and load data into SQLite
python ~/retail_pipeline_project/scripts/clean_and_load.py >> "$LOG_FILE" 2>&1

# Step 2: Update inventory quantities based on recent sales
python ~/retail_pipeline_project/scripts/update_inventory.py >> "$LOG_FILE" 2>&1

# Step 3: Analyze and generate plots
python ~/retail_pipeline_project/scripts/analyze_and_plot.py >> "$LOG_FILE" 2>&1

# Step 4: Check for low stock and export alert CSV
python ~/retail_pipeline_project/scripts/check_low_stock.py >> "$LOG_FILE" 2>&1

# Deactivate the virtual environment
deactivate

# Mark end of log
echo "=== Pipeline End ===" >> "$LOG_FILE"

