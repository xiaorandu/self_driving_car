import socket

from Picar import Picar

HOST = "192.168.12.232" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)


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



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
                
                drive_car(car, data.decode('utf-8').strip())

                client.sendall(data) # Echo back to client
    except Exception as e:
        print(f"Exception:\t{e}") 
        print("Closing socket")
        client.close()
        s.close()