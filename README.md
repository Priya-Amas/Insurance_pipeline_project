Real-Time Insurance Data Pipeline

— Designed and built an end-to-end pipeline using Python, Snowflake (internal stage), and Airflow 2.6.2. Implemented API ingestion, internal staging, MERGE-based deduplication, logging, unit testing, and modular DAG orchestration.

![ChatGPT Image Jun 21, 2025, 07_53_03 PM](https://github.com/user-attachments/assets/281d0563-e7bc-40c0-80e5-2c39a77a8ae3)



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

![image](https://github.com/user-attachments/assets/ab42f05b-9f1b-4e94-a20f-673a7ddb9e0b)
        
## 🧪 To Run the Project (in WSL)

--bash
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
pytest tests/

✅ Contact: Shunmuga Priya
📧 Email: shunmugapriya1901@gmail.com
🌐 GitHub: https://github.com/yourusername/insurance_pipeline
