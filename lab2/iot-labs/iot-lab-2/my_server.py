import socket
import threading
import time
from typing import Union
from Picar import Picar

HOST = "192.168.12.232" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

last_received_time = time.time()  # Initialize with the current time


def drive_car(car: Picar, direction: str):
    print(f"Drive car str:\t{direction}")
    if direction == '87':
        print("Forward")
        car.forward()
    elif direction == '83':
        print("Backward")
        car.backward()
    elif direction == '65':
        print("Left")
        car.move_left()
    elif direction == '68':
        print("Right")
        car.move_right()


def monitor_last_received(car):
    global last_received_time
    while True:
        time_since_last_received = time.time() - last_received_time
        if time_since_last_received > 0.1: 
            print("Data not received for a while, stopping car.")
            car.stop()
            last_received_time = time.time()
        time.sleep(0.02)



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    
    state: Union[int, None] = None
    car = Picar()

    monitor_thread = threading.Thread(target=monitor_last_received, args=(car,))
    monitor_thread.daemon = True
    monitor_thread.start()

    try:
        while 1:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)

            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            if data != b"":
                print(data)
                decoded_data =  data.decode('utf-8').strip()
                state = decoded_data
                
                drive_car(car, decoded_data)

                client.sendall(data)


    except Exception as e:
        print(f"Exception:\t{e}") 
        print("Closing socket")
        client.close()
        s.close()