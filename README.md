# 🏥 Real-Time Insurance Data Pipeline (Apache Airflow + Snowflake)

This project demonstrates a complete real-time data pipeline using:
- Python 3
- Flask API (mock insurance policy data)
- Snowflake (data warehouse with internal stage)
- Apache Airflow 2.6.2 (orchestration)
- Unit tests, logging, and modular DAGs

---

## ✅ Features

- Class-based Flask API to simulate policy data
- Upload JSONs to Snowflake internal stage
- Use `MERGE` to handle incremental loads
- Clean Airflow DAG (modular)
- Pytest unit tests for upload and merge logic
- `.env` and logging integrated

---

## 📁 Folder Structure

.
└── insurance_pipeline
    ├── README.md
    ├── __init__.py
    ├── airflow
    ├── dags
    │   ├── insurance_pipeline_dag.py
    │   └── tasks
    │       └── __pycache__
    ├── data
    │   └── json
    │       ├── insurance_20250619_100003_1.json
    │       ├── insurance_20250619_100003_2.json
    ├── requirements-airflow.txt
    ├── requirements-app.txt
    ├── scripts
    │   ├── api
    │   │   └── insurance_api.py
    │   ├── loaders
    │   │   ├── json_generator.py
    │   │   ├── merge_into_table.py
    │   │   └── upload_to_stage.py
    │   └── utils
    │       └── logger.py
    ├── setup.py
    ├── sql
    │   └── create_table.sql
    ├── tests
    │   ├── test_api.py
    │   ├── test_merge_into_table.py
    │   └── test_upload_to_stage.py
    └── venv
        
## 🧪 To Run the Project (in WSL)

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Run Flask API to generate mock data
python scripts/api/insurance_api.py

# 3. Upload JSON files to Snowflake stage
python scripts/loaders/upload_to_stage.py

# 4. Merge into target table
python scripts/loaders/merge_into_table.py

# 5. Or run it via Airflow
airflow scheduler
airflow webserver --port 8080
🔬 To Run Unit Tests
bash
Copy
Edit
pytest tests/
💼 Use Case
This project can be mentioned in your resume or GitHub portfolio under:

“Built a modular insurance data pipeline using Python, Snowflake, and Apache Airflow with automated JSON ingestion, deduplication via MERGE, and CI-level unit testing.”

✅ Contact: [Your Name]
📧 Email: shunmugapriya1901@gmail.com
🌐 GitHub: https://github.com/yourusername/insurance_pipeline
