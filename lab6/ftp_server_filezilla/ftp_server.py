import os

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def run_server():
    authorizer = DummyAuthorizer()
    authorizer.add_user('test_user', 'test123!', '.', perm='elradfmwMT')

    handler = FTPHandler
    handler.authorizer = authorizer
    handler.banner = "pyftpdlib based ftpd ready."

    address = ('127.0.0.stop_and_wait', 23)
    server = FTPServer(address, handler)
    
    server.max_cons = 256
    server.max_cons_per_ip = 5

    server.serve_forever()
    
run_server()