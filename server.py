import socket
import threading
import time
class TupleSpaceServer:
    def __init__(self, port):
        self.port = port
        self.tuple_space = {}


