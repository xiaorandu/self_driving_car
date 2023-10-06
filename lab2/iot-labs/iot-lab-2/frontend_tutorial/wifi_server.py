import socket
import sys

#sys.path.insert(0, '../../../../lab1') # pwd of call to 'python3 wifi_server.py' is frontend_tutorial
sys.path.insert(0, './lab1') # pwd of call to 'python3 lab2/iot-labs/iot-lab-2/frontend_tutorial/wifi_server.py' is self_driving_car
from Picar import Picar

HOST = "192.168.0.144" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)


def drive_car(direction: str):
    print(f"Drive car str:\t{direction}")



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    
    car = Picar()

    try:
        while 1:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            if data != b"":
                print(str(data))
                
                drive_car(data)

                client.sendall(data) # Echo back to client
    except: 
        print("Closing socket")
        client.close()
        s.close()
