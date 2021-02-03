import streamlit as st
from http.client import HTTPSConnection
from json import loads
from json import dumps

class RestClient:
    domain = "api.wordlift.io"

    def __init__(self, WL_key):
        self.WL_key = WL_key

    def request(self, path, method, data=None):
        connection = HTTPSConnection(self.domain)
        try:
            headers = {'Authorization' : 'Key ' +  self.WL_key}
            connection.request(method, path, headers=headers, body=data)
            response = connection.getresponse()
            return loads(response.read().decode())
        finally:
            connection.close()

    def get(self, path):
        return self.request(path, 'GET')

    def post(self, path, data):
        if isinstance(data, str):
            data_str = data
        else:
            data_str = dumps(data)
        return self.request(path, 'POST', data_str)
