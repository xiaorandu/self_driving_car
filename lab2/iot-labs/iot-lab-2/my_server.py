import socket
import threading
import time
from typing import Union
from Picar import Picar
import json

#HOST = "192.168.12.232" # IP address of your Raspberry PI
HOST = "192.168.0.144" # BR
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

last_received_time = time.time()  # Initialize with the current time

car = Picar()

return_data = {
    "direction": car.orientation
}

def drive_car(car: Picar, direction: str):
    print(f"Drive car str:\t{direction}")
    if direction == '87':
        print("Forward")
        car.forward(5)
    elif direction == '83':
        print("Backward")
        car.backward(5)
    elif direction == '65':
        print("Left")
        car.move_left(5)
    elif direction == '68':
        print("Right")
        car.move_right(5)


def monitor_last_received(car):
    global last_received_time
    while True:
        time_since_last_received = time.time() - last_received_time
        if time_since_last_received > 0.5: 
            #print("Data not received for a while, stopping car.")
            #car.stop()
            last_received_time = time.time()
        time.sleep(0.02)



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    
    state: Union[int, None] = None

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
                return_data["direction"] = car.orientation

                client.sendall(json.dumps(return_data).encode('utf-8'))


    except Exception as e:
        print(f"Exception:\t{e}") 
        print("Closing socket")
        client.close()
        s.close()