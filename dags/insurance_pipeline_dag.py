import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from dags.tasks.upload_task import get_upload_task
from dags.tasks.merge_task import get_merge_task
# insurance_pipeline/dags/insurance_pipeline_dag.py
# This DAG orchestrates the upload of JSON files to a Snowflake stage and merges them into
# a target table in Snowflake. It consists of two main tasks:
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

    upload_task = get_upload_task(dag)
    merge_task = get_merge_task(dag)
    upload_task >> merge_task
