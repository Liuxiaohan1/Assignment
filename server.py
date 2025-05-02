import socket
import threading
import time
class TupleSpaceServer:
    def __init__(self, port):
        self.port = port
        self.tuple_space = {}
        self.lock = threading.Lock()
        self.total_operations = 0
        self.read_operations = 0
        self.get_operations = 0
        self.put_operations = 0
        self.errors = 0
        self.total_clients = 0
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', port))
        self.server_socket.listen(5)
        



