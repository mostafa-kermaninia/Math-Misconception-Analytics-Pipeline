import subprocess

def run_pipeline():
    """Main pipeline to execute each step in the data science workflow."""
    
    print("Starting data pipeline...")

    # Load data
    subprocess.run(["python", "scripts/load_data.py"])
    
    # Preprocess data
    subprocess.run(["python", "scripts/preprocess.py"])
    
    # Perform feature engineering
    subprocess.run(["python", "scripts/feature_engineering.py"])
    
    print("Pipeline execution complete!")

if __name__ == "__main__":
    run_pipeline()
