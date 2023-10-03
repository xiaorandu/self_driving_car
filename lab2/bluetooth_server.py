from bluedot.btcomm import BluetoothServer
from signal import pause
import threading
import time


def data_received(data):
    """Sends received data to picar"""
    print(f"Received:\t{data}")
    s.send(data)

def send_status_update():
    while True:
        i = 1
        s.send("Ping..." + i + "\r\n")
        i += 1
        time.sleep(1)

s = BluetoothServer(data_received)

status_thread = threading.Thread(target=send_status_update)
status_thread.daemon = True
status_thread.start()

pause()