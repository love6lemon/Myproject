import os

Params = {
    'server': '127.0.0.1',
    'port': 8000,
    'url': '/login/report/',
    'request_timeout': 30,
}

PATH = os.path.join(os.path.dirname(os.getcwd()), 'log', 'cmdb.log')