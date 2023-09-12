from airflow import DAG
from airflow.models import BaseOperator


class PlusOneOperator(BaseOperator):
    def __init__(self, value, **kwargs):
        super().__init__(**kwargs)
        self.value = value

    def execute(self, context):
        return self.value + 1


class SumOperator(BaseOperator):
    def __init__(self, values, **kwargs):
        super().__init__(**kwargs)
        self.values = values

    def execute(self, context):
        total = sum(self.values)
        print(f"Sum was {total}")
        return total


with DAG(dag_id='map_reduce') as dag:
    plus_one_task = PlusOneOperator.partial(task_id='plus_one').expand(value=[1,2,3,4,5])
    sum_task = SumOperator(task_id='reduce_task',values=plus_one_task.output)