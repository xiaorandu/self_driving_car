from bluedot.btcomm import BluetoothServer
from signal import pause
import threading
import time
import subprocess
import psutil

def get_voltage():
    voltage = subprocess.check_output("picar-4wd power-read | grep voltage | cut -d' ' -f3", shell=True, text=True)
    print(f"Voltage:\t{voltage}")
    return voltage

def get_cpu_usage():
    cpu_usage = f"{psutil.cpu_percent(5)/100:.2%}"
    print(f"cpu_usage:\t{cpu_usage}")
    return cpu_usage

def data_received(data):
    """Sends received data to picar"""
    print(f"Received:\t{data}")
    if data.strip() == 'v':
        s.send(get_voltage() + "\r\n")
    #s.send(data)

def send_status_update():
    i = get_cpu_usage()
    while True:
        s.send(f"CPU Usage: {i}\r\n")
        i = get_cpu_usage()
        time.sleep(1)

s = BluetoothServer(data_received)

#status_thread = threading.Thread(target=send_status_update)
#status_thread.daemon = True
#status_thread.start()

pause()