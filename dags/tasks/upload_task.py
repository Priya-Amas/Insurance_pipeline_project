from airflow.operators.python import PythonOperator
from scripts.loaders.upload_to_stage import upload_to_internal_stage

def get_upload_task(dag):
    return PythonOperator(
        task_id='upload_to_stage',
        python_callable=upload_to_internal_stage,
        dag=dag
    )
