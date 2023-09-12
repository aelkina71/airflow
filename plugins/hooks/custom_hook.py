import requests
from airflow.hooks.base import BaseHook


class CustomHook(BaseHook):
    def __init__(self, conn_id):
        super().__init__()
        self.conn_id = conn_id
        self.connection = self.get_connection(conn_id)

    def interact(self, data):
        host = self.connection.host
        r = requests.post(data=data, url=host)
        return r
