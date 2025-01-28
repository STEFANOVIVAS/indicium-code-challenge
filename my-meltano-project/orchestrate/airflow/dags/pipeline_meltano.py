from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'start_date': datetime(2025, 1, 27),
    'retries': 3,
    'retry_delay': timedelta(minutes=3),
}

dag = DAG('northwind_meltano_pipeline', default_args=default_args, schedule_interval='@daily')

meltano_extract_from_csv_load_csv_step_1 = BashOperator(
    task_id='extract_from_csv_load_csv',
    bash_command='DATE=$(date +%Y-%m-%d) meltano run orders-details-csv-to-local',
    dag=dag
)

meltano_extract_from_postgres_load_csv_step_1 = BashOperator(
    task_id='extract_from_postgres_load_csv',
    bash_command='DATE=$(date +%Y-%m-%d) meltano run postgres-to-local',
    dag=dag
)

meltano_extract_from_csv_load_postgres_step_2 = BashOperator(
    task_id='extract_from_csv_load_postgres',
    bash_command='DATE=$(date +%Y-%m-%d) meltano run local-csv-to-postgres',
    dag=dag
)




[meltano_extract_from_csv_load_csv_step_1, meltano_extract_from_postgres_load_csv_step_1] >> meltano_extract_from_csv_load_postgres_step_2