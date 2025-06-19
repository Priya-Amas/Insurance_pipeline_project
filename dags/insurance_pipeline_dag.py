import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from scripts.loaders.upload_to_stage import upload_to_internal_stage
from scripts.loaders.merge_into_table import merge_data_from_stage

default_args = {
    'owner': 'priya',
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    dag_id='insurance_pipeline_dag',
    default_args=default_args,
    start_date=datetime(2025, 6, 19),
    schedule_interval=None,
    catchup=False
) as dag:

    upload_task = PythonOperator(
        task_id='upload_to_stage',
        python_callable=upload_to_internal_stage
    )

    merge_task = PythonOperator(
        task_id='merge_into_table',
        python_callable=merge_data_from_stage
    )

    upload_task >> merge_task
