from datetime import datetime

import requests
from airflow.decorators import task, dag
from airflow.hooks.base import BaseHook
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.http.sensors.http import HttpSensor
from airflow.sensors.python import PythonSensor

from plugins.hooks.custom_hook import CustomHook


def check_site_avialable(**context):
    hook = CustomHook(conn_id='shibes')
    data = {}
    r = hook.interact(data=data)
    if r.status_code == 200:
        return_value = r.json()
        context["ti"].xcom_push(key="return_value", value=return_value)
        return True
    else:
        return_value = None
        return False


@dag(tags=['sensor'], start_date=datetime(2023,9,12), catchup=False)
def sensor_example():
    HttpSensor()
    check_site_sensor = PythonSensor(task_id='check_site_avialable', poke_interval=10, timeout=3600, python_callable=check_site_avialable)

    @task
    def print_json(json):
        print(json)

    print_json(check_site_sensor.output)