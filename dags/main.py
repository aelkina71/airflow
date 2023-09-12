from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


def greet(ds, name, **kwargs):
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        print(f"Error: {e}")
    print(f"Hello {name}")
    print(f"Exdcution date is {ds}")
    print(f"Parameters: {kwargs['my_param']}")


dag = DAG('first_dag')

task = BashOperator(task_id='hello_bash',
                    bash_command='echo "Current date is $(date)"',
                    dag=dag)


