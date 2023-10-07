import socket
import threading
import time
from typing import Union
from Picar import Picar
import json
import base64
from picamera2 import Picamera2
import libcamera
from gpiozero import CPUTemperature
import subprocess
import psutil

#HOST = "192.168.12.232" # IP address of your Raspberry PI
# HOST = "192.168.0.144" # BR
HOST = "192.168.0.22" #XD
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

last_received_time = time.time()  # Initialize with the current time
total_dist = 0
car = Picar()

#get Raspberry CPU temperature from gpiozero package(pip install gpiozero)
def get_temperature():
    temperature =  '%.2f'%CPUTemperature().temperature
    print(f"Temperature:\t{temperature}")
    return temperature

def get_cpu_usage():
    cpu_usage = f"{psutil.cpu_percent(5)/100:.2%}"
    print(f"cpu_usage:\t{cpu_usage}")
    return cpu_usage

def get_voltage():
    voltage = subprocess.check_output("picar-4wd power-read | grep voltage | cut -d' ' -f3", shell=True, text=True)
    print(f"Voltage:\t{voltage}")
    return voltage
    
def take_picture():
    # newer method. Disable legacy camera support in raspi-config.
    picam = Picamera2()
    config = picam.create_preview_configuration(main={"size": (640, 480)})
    config["transform"] = libcamera.Transform(hflip=1, vflip=1)
    picam.configure(config)
    picam.start()
    time.sleep(2)
    picam.capture_file("test-python.jpg")
    picam.close()

    with open('test-python.jpg', 'rb') as f:
        image = base64.b64encode(f.read())
        image = image.decode('utf-8')
    return image

return_data = {
    "direction": car.orientation,
    "image": take_picture(),
    "temperature": get_temperature(),
    "voltage":get_voltage(),
    "distance": total_dist,
    "cpu_usage":get_cpu_usage()
}

def drive_car(car: Picar, direction: str):
    global total_dist
    print(f"Drive car str:\t{direction}")
    if direction == '87':
        print("Forward")
        car.forward(5)
        total_dist += 5
        
    elif direction == '83':
        print("Backward")
        car.backward(5)
        total_dist -= 5
        
    elif direction == '65':
        print("Left")
        car.move_left(5)
    elif direction == '68':
        print("Right")
        car.move_right(5)
        
    print(f"distace:\t{total_dist}")
    return_data["distance"] = total_dist
    if direction in ['87','83','65','68']:
        return_data["direction"] = car.orientation
        return_data["image"] = take_picture()

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
                # SEND DATA BACK TO ELECTRON CLIENT
                client.sendall(json.dumps(return_data).encode('utf-8'))
                client.close()

    except Exception as e:
        print(f"Exception:\t{e}") 
        print("Closing socket")
        client.close()
        s.close()
