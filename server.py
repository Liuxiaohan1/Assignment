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
        print(f"Server listening on port {port}")
        threading.Thread(target=self.print_statistics,daemon=True).start()
    def handle_client(self, client_socket):
        self.total_clients += 1
        try:
            while True:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                try:
                    message_size = int(data[:3])
                    command = data[3]
                    key_value = data[4:message_size].split(' ', 1)
                    key = key_value[0]
                    value = key_value[1] if len(key_value) > 1 else ''
                    



        


        



