from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

DEFAULT_ARGS = {"owner": "mahan", "retries": 1}

with DAG(
    dag_id="food_delivery_pipeline",
    default_args=DEFAULT_ARGS,
    description="Generate raw food delivery data and build dbt models in BigQuery",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["portfolio", "dbt", "bigquery"],
) as dag:

    generate_data = BashOperator(
        task_id="generate_data",
        bash_command="""
        set -e
        export GOOGLE_APPLICATION_CREDENTIALS=/opt/airflow/service_account.json
        cd /opt/airflow/project
        python data_simulator/generate_data.py
        """,
    )

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command="""
        set -e
	cd /opt/airflow/project/food_delivery && \
	export GOOGLE_APPLICATION_CREDENTIALS=/opt/airflow/service_account.json && \
	dbt build --profiles-dir /opt/airflow/dbt/profiles
        """,
    )

    generate_data >> dbt_build
