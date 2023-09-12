from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

default_args = {
    'num_tasks': 5
}

with DAG(dag_id='cycle_example', default_args=default_args) as dag:
    tasks = {}
    x = range(default_args['num_tasks'])
    for i in x:
        task_id = f"task_{i}"
        task = BashOperator(task_id=task_id, bash_command=f'echo "Executing task {i}"')
        dag >> task
        tasks[task_id] = task

    task_empty = EmptyOperator(task_id='empty_task')
    for (key, value) in tasks:
        value >> task_empty
