from airflow.operators.python import PythonOperator
from scripts.loaders.merge_into_table import merge_data_from_stage

def get_merge_task(dag):
    return PythonOperator(
        task_id='merge_into_table',
        python_callable=merge_data_from_stage,
        dag=dag
    )
