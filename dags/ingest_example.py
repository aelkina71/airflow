from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.hooks.http import HttpHook


def ingest_iss():
    http_hook = HttpHook('GET', 'ingest-iss')
    # endpoint = http_hook.get_connection('ingest-iss').extra['iss_endpoint']
    # response = http_hook.run(endpoint=endpoint)
    response = http_hook.run(endpoint='/iss-now.json')
    status_code = response.status_code
    if status_code != 200:
        raise ValueError('API returned code ', status_code)
    json_data = response.json()
    if json_data['message'] != 'successful':
        raise ValueError('Response message ', json_data)


with DAG(dag_id='branching_dag', start_date=datetime(2023,9,12)) as dag:
    PythonOperator()