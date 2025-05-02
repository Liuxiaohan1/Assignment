import socket
import sys
def client(hostname, port, filename):
    with open(filename,'r') as f:
        lines = f.readlines()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((hostname,port))
        for line in lines:
            line = line.strip()
            parts = line.split(maxsplit = 2)
            if not parts:
                continue
            command = parts[0]

        
    
