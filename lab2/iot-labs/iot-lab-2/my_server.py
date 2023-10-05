import socket

from Picar import Picar

HOST = "192.168.12.232" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)


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
                print(data)
                
                drive_car(car, data.decode('utf-8'))

                client.sendall(data) # Echo back to client
    except: 
        print("Closing socket")
        client.close()
        s.close()