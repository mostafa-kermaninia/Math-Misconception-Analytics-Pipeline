
# Mathematics Misconception Analysis Pipeline

![Build Status](https://img.shields.io/github/actions/workflow/status/mostafa-kermaninia/Misconceptions-in-mathematics/pipeline.yml?branch=main)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![Docker](https://img.shields.io/badge/docker-enabled-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 📋 Overview

**Mathematics Misconception Analysis Pipeline** is an end-to-end data engineering and analytics solution designed to process, store, and analyze educational datasets. The project focuses on identifying students' mathematical misconceptions to improve personalized learning systems.

This repository implements a robust **ETL (Extract, Transform, Load)** workflow that ingests raw data, manages it via a relational database (MySQL), and performs advanced feature engineering (including TF-IDF vectorization) to prepare datasets for **Machine Learning (ML)** and **Large Language Model (LLM)** training.

Designed with scalability and reproducibility in mind, the architecture leverages **Docker** for containerization, **Kubernetes** manifests for orchestration, and **GitHub Actions** for CI/CD automation.

## 🚀 Key Features

* **Automated ETL Pipeline:** Seamlessly imports CSV data into a structured MySQL database using SQLAlchemy.
* **Advanced Feature Engineering:**
    * **Text Analysis:** TF-IDF vectorization for processing textual misconception data.
    * **Categorical Encoding:** Label encoding for constructs and subjects.
    * **Data Cleaning:** Automated handling of missing values and normalization.
* **Containerized Environment:** Fully Dockerized application ensuring consistency across development, testing, and production environments.
* **Cloud-Ready Deployment:** Includes Kubernetes (`deployment.yaml`, `service.yaml`) configurations for scalable orchestration.
* **CI/CD Integration:** Automated workflows via GitHub Actions for code quality checks and build verification.

## 🛠 Tech Stack

* **Core:** Python 3.9+, Pandas, NumPy
* **Machine Learning:** Scikit-learn (TF-IDF, Preprocessing)
* **Database:** MySQL, SQLite, SQLAlchemy (ORM)
* **DevOps & Infrastructure:** Docker, Kubernetes (K8s), GitHub Actions
* **Version Control:** Git

## 📂 Project Structure

```bash
├── .github/workflows/    # CI/CD Pipeline configurations
├── scripts/              # Core logic and ETL scripts
│   ├── database_operations/  # DB connection & raw SQL queries
│   ├── feature_engineering.py # ML preprocessing logic
│   ├── load_data.py          # Data ingestion modules
│   ├── preprocess.py         # Cleaning & normalization
│   └── ...
├── Dockerfile            # Container configuration
├── deployment.yaml       # Kubernetes Deployment manifest
├── service.yaml          # Kubernetes Service manifest
├── pipeline.py           # Main entry point for the pipeline
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation

```

## ⚡ Getting Started

### Prerequisites

* Docker & Docker Compose (Recommended)
* Python 3.9+ (For manual execution)
* MySQL Server (If running locally without Docker)

### Option 1: Run with Docker (Recommended)

Build and run the containerized pipeline to ensure all dependencies and database connections are isolated.

```bash
# Build the Docker image
docker build -t math-misconception-pipeline .

# Run the container
docker run --env-file .env math-misconception-pipeline

```

### Option 2: Manual Installation

1. **Clone the repository:**
```bash
git clone [https://github.com/mostafa-kermaninia/Misconceptions-in-mathematics.git](https://github.com/mostafa-kermaninia/Misconceptions-in-mathematics.git)
cd Misconceptions-in-mathematics

```


2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

```


3. **Install dependencies:**
```bash
pip install -r requirements.txt

```


4. **Configuration:**
Create a `.env` file in the root directory to store your database credentials:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=DataScience_DB

```


5. **Run the pipeline:**
```bash
python pipeline.py

```



## 📊 Workflow Architecture

The pipeline follows a modular architecture:

1. **Ingestion:** Raw CSV files are read and validated.
2. **Storage:** Data is normalized and stored in the relational database.
3. **Processing:**
* `load_data.py`: Retrives fresh data from the DB.
* `preprocess.py`: Cleans text and handles null values.
* `feature_engineering.py`: Applies TF-IDF to the 'Misconception Analysis' text fields.


4. **Output:** Processed DataFrames ready for model training.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

---

**Author:** [Mostafa Kermaninia](https://github.com/mostafa-kermaninia)
