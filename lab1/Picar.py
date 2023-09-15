import picar_4wd as fc
from enum import Enum
from picar_4wd import servo
from obstacle_map import ObstacleMap
from astar import astar
import time

FORWARD_SPEED = 10
BACKWARD_SPEED = 10
TURNING_SPEED = 50
DIST_TO_OBSTACLE = 35
SERVO_OFFSET = 45 # customize to make the servo point straight forward at angle zero. If it is already, just set this to zero.

ANGLE_RANGE = 144
STEP = 18
#inital scan angle is set to 72
current_angle = 90
max_angle = ANGLE_RANGE/2
min_angle = -ANGLE_RANGE/2
scan_list = []
angle_to_dist = {}


class Picar:
    def __init__(self):
        servo.offset = SERVO_OFFSET
        servo.set_angle(0)
        self.servo_step = STEP

        self.forward_speed = FORWARD_SPEED
        self.backward_speed = BACKWARD_SPEED
        self.turning_speed = TURNING_SPEED

        self.obstacle_map = ObstacleMap()
        self.location = (int(self.obstacle_map.size / 2), 0) # (x, y)
        self.angle_to_dist = {}


    def forward(self) -> None:
        fc.forward(self.forward_speed)
    
    def backward(self) -> None:
        fc.backward(self.backward_speed)

    def turn_right(self) -> None:
        fc.turn_right(self.forward_speed)

    def turn_left(self) -> None:
        fc.turn_left(self.forward_speed)

    def stop(self) -> None:
        fc.stop()

    def turn_around(self):
        fc.turn_right(self.turning_speed)
        time.sleep(2.5)
        self.forward()
        
    def move_right(self):
        fc.turn_right(self.turning_speed)
        time.sleep(1)
        self.forward()
        
    def move_left(self):
        fc.turn_left(self.turning_speed)
        time.sleep(1)
        self.forward()
     
    def move_front_right(self):
        self.turn_right()
        time.sleep(1)
        self.forward()
    
    def move_front_left(self):
        self.turn_left()
        time.sleep(1)
        self.forward()
    
    def move_back_right(self):
        self.turn_around()
        self.move_front_left()
        
    def move_back_left(self):
        self.turn_around()
        self.move_front_right()
    
    def scan_env_and_map(self) -> None:
        self.angle_to_dist = {}
        cur_angle = min_angle
        while cur_angle <= max_angle:
            self.angle_to_dist[cur_angle] = fc.get_distance_at(cur_angle)
            cur_angle += self.servo_step

        self.obstacle_map.do_map(self.angle_to_dist)
    
    def find_path(self) -> list[tuple]:
        # TODO: find end destination
        path = astar(self.location[0], self.location[1], 100, 50, self.obstacle_map.get_map())
        print(f"Astar path:\t{path}")

        return path
    
    def get_direction(self, x_dest, y_dest) -> tuple:
        to_steer = (x_dest - self.location[0], y_dest - self.location[1])
        return to_steer
