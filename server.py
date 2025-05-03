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
                print(f"Received raw data: {data}")
                try:
                    message_size = int(data[:3])
                    command = data[3]
                    key_value = data[4:message_size].split(' ', 1)
                    key = key_value[0]
                    value = key_value[1] if len(key_value) > 1 else ''
                    print(f"Parsed command: {command}, key: {key}, value: {value}")
                except(ValueError, IndexError):
                    print("Error parsing request")
                    continue
                response = ""
                with self.lock:
                    self.total_operations+= 1
                    if command == 'R':
                        self.read_operations += 1
                        if key in self.tuple_space:
                            response = f"{len(f'OK ({key}, {self.tuple_space[key]}) read'):03} OK ({key}, {self.tuple_space[key]}) read"
                        else:
                            self.errors += 1
                            response = f"{len(f'ERR {key} does not exist'):03} ERR {key} does not exist"
                    elif command == 'G':
                        self.get_operations += 1
                        if key in self.tuple_space:
                            val = self.tuple_space.pop(key)
                            response = f"{len(f'OK ({key}, {val}) removed'):03} OK ({key}, {val}) removed"
                        else:
                            self.errors += 1
                            response = f"{len(f'ERR {key} does not exist'):03} ERR {key} does not exist"
                    elif command == 'P':
                        self.put_operations += 1
                        if key in self.tuple_space:
                            self.errors += 1
                            response = f"{len(f'ERR {key} already exists'):03} ERR {key} already exists"
                        else:
                            self.tuple_space[key] = value
                            response = f"{len(f'OK ({key}, {value}) added'):03} OK ({key}, {value}) added"
                print(f"Sending response: {response}")
                client_socket.send(response.encode())
        except Exception as e:
            print(f"Client error: {e}")
        finally:
            client_socket.close()
    def print_statistics(self):
        while True:
            time.sleep(10)
            with self.lock:
                num_tuples = len(self.tuple_space)
                if num_tuples == 0:
                    avg_tuple_size = avg_key_size = avg_value_size = 0
                else:
                    total_tuple_size = sum(len(k) + len(v) for k, v in self.tuple_space.items())
                    avg_tuple_size = total_tuple_size / num_tuples
                    avg_key_size = sum(len(k) for k in self.tuple_space.keys()) / num_tuples
                    avg_value_size = sum(len(v) for v in self.tuple_space.values()) / num_tuples
                print(f"Tuple space stats: {num_tuples} tuples, avg tuple size {avg_tuple_size:.2f}, "
                      f"avg key size {avg_key_size:.2f}, avg value size {avg_value_size:.2f}, "
                      f"total clients {self.total_clients}, total operations {self.total_operations}, "
                      f"READs {self.read_operations}, GETs {self.get_operations}, PUTs {self.put_operations}, "
                      f"errors {self.errors}")
    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)
    port = int(sys.argv[1])
    server = TupleSpaceServer(port)
    server.start()
    



                    
                    

                   
                    



        


        



