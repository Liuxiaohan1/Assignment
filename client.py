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
            if (command == 'PUT' and len(parts) != 3) or (command in('READ' ,'Get')and len(parts) != 2):
                print(f"Invalid command: {line}")
                continue

            key = parts[1]
            value = parts[2] if len(parts) == 3 else ''

            if command == 'PUT':
                combined = f"P{key} {value}"
            elif command == 'READ':
                combined = f"R{key}"
            elif command == 'GET':
                combined = f"G{key}"
            else:
                print(f"Unknown command: {line}")
                continue

            message_length = len(combined)
            message = f"{message_length:03}{combined}"
            s.send(message.encode())
            
            


                

                


        
    
