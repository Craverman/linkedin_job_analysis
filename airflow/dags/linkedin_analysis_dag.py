import os
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from google.cloud import storage
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
import pyarrow.csv as pv
import pyarrow.parquet as pq
import pandas as pd


PROJECT_ID = "linkedin-jobs-418420"
BUCKET = "linkedin_job_bucket"
dataset_path = "/workspaces/linkedin_job_analysis/airflow/"
dataset_file = "linkedin_job_postings.csv"
dataset_file2 = "job_skills.csv"
parquet_file = dataset_file.replace('.csv', '.parquet')
parquet_file2 = dataset_file2.replace('.csv', '.parquet')
BIGQUERY_DATASET = "BIGQUERY_DATASET", 'linkedin_data_all'


def upload_to_gcs(bucket, object_name, local_file):
    storage_client = storage.Client.from_service_account_json('/workspaces/linkedin_job_analysis/terraform/creds.json')
    bucket = storage_client.get_bucket(BUCKET)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)


def format_to_parquet(src_file):
    if not src_file.endswith('.csv'):
        logging.error("Can only accept source files in CSV format, for the moment")
        return
    df = pd.read_csv(src_file)
    df.to_parquet(src_file.replace('.csv', '.parquet'))

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="linkedin_analysis_dag",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['linkedin'],
) as dag:

    format_to_parquet_task1 = PythonOperator(
        task_id="format_to_parquet_task1",
        python_callable=format_to_parquet,
        op_kwargs={
            "src_file": f"{dataset_path}{dataset_file}",
        },
    )

    format_to_parquet_task2 = PythonOperator(
        task_id="format_to_parquet_task2",
        python_callable=format_to_parquet,
        op_kwargs={
            "src_file": f"{dataset_path}{dataset_file2}",
        },
    )


    local_to_gcs_task1 = PythonOperator(
        task_id="local_to_gcs_task",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket": BUCKET,
            "object_name": f"linkedin_dataset/{parquet_file}",
            "local_file": f"{dataset_path}{parquet_file}",
        },
    )

    local_to_gcs_task2 = PythonOperator(
        task_id="local_to_gcs_task2",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket": BUCKET,
            "object_name": f"linkedin_dataset/{parquet_file2}",
            "local_file": f"{dataset_path}{parquet_file2}",
        },
    )

    spark_transfrom_to_bigquery = BashOperator(
        task_id="spark_transfrom_to_bigquery",
        bash_command="python /workspaces/linkedin_job_analysis/scripts/spark_transfrom_to_bigquery.py",
        dag=dag
)

    # bigquery_external_table_task = GCSToBigQueryOperator(
    #     task_id="bigquery_external_table_task",
    #     bucket=BUCKET,
    #     source_objects="linkedin_dataset/job_skills.csv",
    #     destination_project_dataset_table = "linkedin_job_bq.job_skills",
    #     schema_fields=[
    #         {"name": "job_link", "type": "STRING", "mode": "NULLABLE"},
    #         {"name": "job_skills", "type": "STRING", "mode": "NULLABLE"},
    #     ]
    # )


format_to_parquet_task1 >> format_to_parquet_task2 >> local_to_gcs_task1 >> local_to_gcs_task2 >> spark_transfrom_to_bigquery