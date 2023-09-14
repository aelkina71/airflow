from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.operators.postgres import PostgresOperator


def ingest_iss(**context):
    http_hook = HttpHook('GET', 'ingest-iss')
    # endpoint = http_hook.get_connection('ingest-iss').extra['iss_endpoint']
    # response = http_hook.run(endpoint=endpoint)
    response = http_hook.run(endpoint='/iss-now.json')
    status_code = response.status_code
    if status_code != 200:
        raise ValueError('API returned code ', status_code)
    json_data = response.json()
    if json_data['message'] != 'success':
        raise ValueError('Response message ', json_data)
    context['ti'].xcom_push(key='timestamp', value=json_data['timestamp'])
    context['ti'].xcom_push(key='message', value=json_data['message'])
    context['ti'].xcom_push(key='latitude', value=json_data['iss_position']['latitude'])
    context['ti'].xcom_push(key='longitude', value=json_data['iss_position']['longitude'])
    return


with DAG(dag_id='branching_dag', start_date=datetime(2023,9,12)) as dag:
    ingest_iss_task = PythonOperator(task_id='ingest_iss', python_callable=ingest_iss, provide_context=True)
    save_postgres_task = PostgresOperator(task_id='save_postgres', postgres_conn_id='postres-save',
                                          database='etl_test', sql=
                                          """
                                          INSERT INTO iss_data(ts, latitude, longitude, message) VALUES(
                                          {{ ti.xcom_pull(key='timestamp') }},
                                          {{ ti.xcom_pull(key='latitude') }},
                                          {{ ti.xcom_pull(key='longitude') }},
                                          '{{ ti.xcom_pull(key='message') }}'
                                          )
                                          """)

if __name__ == '__main__':
    dag.test()
