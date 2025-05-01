# Data Science Pipeline

## Project Structure:
- `scripts/`: Contains Python scripts for loading data, preprocessing, and feature engineering.
  - `database_operations/`: Contains scripts to import CSV data into the database.
- `pipeline.py`: Main script to run the entire data pipeline.
- `requirements.txt`: Lists the dependencies required for the project.

## How to Run:

### Rebuild the Database from CSV:
1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Run the script to import data into the database:
    ```bash
    python scripts/database_operations/import_csv_to_db.py
    ```

### Run the Data Pipeline:
1. After importing the data, run the main pipeline to process the data:
    ```bash
    python pipeline.py
    ```

This will execute the full data processing pipeline, including preprocessing and feature engineering.
